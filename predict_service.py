# birds/predict_service.py
from __future__ import annotations
import os
import subprocess
import tempfile
from pathlib import Path
from collections import Counter
import numpy as np
import pandas as pd
import librosa
from librosa import feature as lf
import pickle
from django.conf import settings
from .audio_preprocess import preprocess_audio


# -- Must match training --
TARGET_SR   = 22_050
HOP         = 512
WIN_SAMPLES = 6_144
N_MELS      = 128

ARTIFACT_DIR = Path(getattr(settings, "ML_ARTIFACT_DIR", Path(".")))
MODEL_PATH = ARTIFACT_DIR / "svm.sav"
TRAIN_CSV  = ARTIFACT_DIR / "train.csv"

# Load model + schema at import time (fast for subsequent requests)
_MODEL = None
_TRAIN_DF = None
_FEATURE_COLS = None

def _ensure_model_loaded():
    """Lazy load model and training data to handle missing files gracefully"""
    global _MODEL, _TRAIN_DF, _FEATURE_COLS
    if _MODEL is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model file not found at {MODEL_PATH}. "
                f"Please ensure svm.sav exists in {ARTIFACT_DIR}"
            )
        if not TRAIN_CSV.exists():
            raise FileNotFoundError(
                f"Training CSV not found at {TRAIN_CSV}. "
                f"Please ensure train.csv exists in {ARTIFACT_DIR}"
            )
        with open(MODEL_PATH, "rb") as f:
            _MODEL = pickle.load(f)
        _TRAIN_DF = pd.read_csv(TRAIN_CSV)
        _FEATURE_COLS = [c for c in _TRAIN_DF.columns if c not in ("species", "genus", "binomial")]

# Load on import (will raise error if files don't exist)
try:
    _ensure_model_loaded()
except FileNotFoundError as e:
    import warnings
    warnings.warn(f"Model not loaded: {e}. Prediction will fail until model files are available.")

def _convert_audio_to_wav(input_path: Path) -> Path:
    """Convert audio file to WAV format using pydub/ffmpeg if needed."""
    # Check if file is already in a format librosa can handle directly
    ext = input_path.suffix.lower()
    if ext in ['.wav', '.flac']:
        return input_path
    
    # For webm, mp3, m4a, ogg and other formats, convert to wav
    output_path = input_path.with_suffix('.wav')
    
    try:
        # Try using pydub first (requires ffmpeg)
        from pydub import AudioSegment
        audio = AudioSegment.from_file(str(input_path))
        audio = audio.set_frame_rate(TARGET_SR)
        audio = audio.set_channels(1)  # mono
        audio.export(str(output_path), format="wav")
        return output_path
    except ImportError:
        # pydub not available, try direct ffmpeg
        try:
            subprocess.run(
                ['ffmpeg', '-i', str(input_path), '-y', '-ar', str(TARGET_SR), 
                 '-ac', '1', '-f', 'wav', str(output_path)],
                check=True,
                capture_output=True,
                timeout=30
            )
            return output_path
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
            raise RuntimeError(
                f"Could not convert audio file. Please install ffmpeg: "
                f"brew install ffmpeg (macOS) or apt-get install ffmpeg (Linux). "
                f"Error: {str(e)}"
            )
    except Exception as e:
        # pydub failed, try direct ffmpeg as fallback
        try:
            subprocess.run(
                ['ffmpeg', '-i', str(input_path), '-y', '-ar', str(TARGET_SR), 
                 '-ac', '1', '-f', 'wav', str(output_path)],
                check=True,
                capture_output=True,
                timeout=30
            )
            return output_path
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            raise RuntimeError(
                f"Could not convert audio file. Please install ffmpeg: "
                f"brew install ffmpeg (macOS) or apt-get install ffmpeg (Linux). "
                f"Original error: {str(e)}"
            )

def _load_audio_masked(audio_path: Path) -> np.ndarray:
    # Convert to wav if needed
    try:
        converted_path = _convert_audio_to_wav(audio_path)
        should_cleanup = converted_path != audio_path
    except RuntimeError:
        # If conversion fails, try loading directly (might work for some formats)
        converted_path = audio_path
        should_cleanup = False
    
    try:
            # NEW: clean up the raw audio
        y, sr = librosa.load(converted_path, sr=TARGET_SR, mono=True)
    finally:
        # Clean up converted file if we created one
        if should_cleanup and converted_path.exists():
            try:
                converted_path.unlink()
            except:
                pass
    
    if y.size == 0:
        return y
    # y = preprocess_audio(y, TARGET_SR)
    sg = lf.melspectrogram(y=y, sr=TARGET_SR, hop_length=HOP, n_mels=N_MELS)
    centerpoint = int(np.argmax(sg.mean(axis=0)))
    M = float(sg[:, centerpoint].mean())
    mask_frames = sg.mean(axis=0) >= (M / 20.0)
    audio_mask = np.zeros_like(y, dtype=bool)
    for i, keep in enumerate(mask_frames):
        s = i * HOP
        e = min((i + 1) * HOP, len(y))
        audio_mask[s:e] = keep
    return y[audio_mask] if audio_mask.any() else y

def _window_signal(y: np.ndarray, W: int = WIN_SAMPLES) -> list[np.ndarray]:
    if y is None or y.size < W:
        return []
    n = len(y) // W
    return [y[i*W:(i+1)*W] for i in range(n)]

def _extract_features(window: np.ndarray) -> dict:
    sc = lf.spectral_centroid(y=window, sr=TARGET_SR, hop_length=HOP)
    scv = sc[0] if sc.ndim == 2 else sc
    chroma = lf.chroma_stft(y=window, sr=TARGET_SR, hop_length=HOP)
    feats = {
        "sc_mean": float(np.mean(scv)),
        "sc_std":  float(np.std(scv)),
        "sc_p10":  float(np.percentile(scv, 10)),
        "sc_p50":  float(np.percentile(scv, 50)),
        "sc_p90":  float(np.percentile(scv, 90)),
    }
    for k in range(chroma.shape[0]):
        v = chroma[k]
        feats[f"ch{k}_mean"] = float(np.mean(v))
        feats[f"ch{k}_std"]  = float(np.std(v))
    return feats

def _featurize_windows(windows: list[np.ndarray]) -> pd.DataFrame:
    if _FEATURE_COLS is None:
        raise RuntimeError("Model not loaded. Feature columns are not available.")
    rows = [_extract_features(w) for w in windows]
    df = pd.DataFrame(rows)
    for c in _FEATURE_COLS:
        if c not in df.columns:
            df[c] = 0.0
    return df[_FEATURE_COLS]

def predict_audio_file(audio_path: Path) -> dict:
    """
    Returns:
      {
        "windows": int,
        "pred_top": str | None,
        "confidence": float,
        "votes": dict[str, int]
      }
    """
    # Ensure model is loaded
    try:
        _ensure_model_loaded()
    except FileNotFoundError as e:
        raise RuntimeError(f"Model files not found: {e}")
    
    if _MODEL is None or _FEATURE_COLS is None:
        raise RuntimeError("Model not loaded. Please ensure svm.sav and train.csv exist.")
    
    try:
        y = _load_audio_masked(audio_path)
        chunks = _window_signal(y, WIN_SAMPLES)
        if not chunks:
            return {"windows": 0, "pred_top": None, "confidence": 0.0, "votes": {}}
        X = _featurize_windows(chunks).values
        preds = _MODEL.predict(X)
        counts = Counter(preds)
        if not counts:
            return {"windows": len(chunks), "pred_top": None, "confidence": 0.0, "votes": {}}
        pred_top, votes = counts.most_common(1)[0]
        return {
            "windows": len(chunks),
            "pred_top": str(pred_top),
            "confidence": votes / len(preds),
            "votes": dict(sorted(counts.items(), key=lambda x: -x[1])[:5]),
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise RuntimeError(f"Error during prediction: {str(e)}")
