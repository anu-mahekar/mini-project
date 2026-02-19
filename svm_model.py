# svm_model.py
# A clean, leakage-safe SVM baseline for birdsong classification.
# Run: python svm_model.py

from __future__ import annotations
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from pathlib import Path
import numpy as np
import pandas as pd
import librosa
from librosa import feature as lf

from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import pickle
import sys

# -------------------
# Config
# -------------------
DATA_ROOT = Path("./dataset")
AUDIO_DIR = DATA_ROOT / "songs"
META_CSV  = DATA_ROOT / "birdsong_metadata.csv"

TARGET_SR = 22_050       # resample all audio here
HOP = 512                # hop length (samples)
WIN_SAMPLES = 6_144      # window size in samples (approx 0.279 s @ 22.05 kHz)
N_MELS = 128             # mel bands for activity mask
TEST_SIZE = 0.20         # held-out fraction by files
RANDOM_STATE = 42

LABEL_LEVEL = "species"  # choose "species" or "genus"

# -------------------
# Utils
# -------------------
rng = np.random.default_rng(RANDOM_STATE)

def assert_paths():
    if not META_CSV.exists():
        sys.exit(f"[ERROR] Metadata CSV not found at: {META_CSV}")
    if not AUDIO_DIR.exists():
        sys.exit(f"[ERROR] Audio directory not found at: {AUDIO_DIR}")

def load_metadata() -> pd.DataFrame:
    df = pd.read_csv(META_CSV)
    required = {"file_id", "genus", "species"}
    missing = required - set(df.columns)
    if missing:
        sys.exit(f"[ERROR] Missing required columns in CSV: {missing}")
    # normalize types
    df["file_id"] = df["file_id"].astype(int)
    df["genus"] = df["genus"].astype(str)
    df["species"] = df["species"].astype(str)
    return df

def load_audio_masked(file_id: int) -> np.ndarray:
    """
    Load mono audio, resample to TARGET_SR, compute a mel-spectrogram mask to
    keep frames with energy >= 5% of the peak-mean frame, and return masked audio.
    """
    path = AUDIO_DIR / f"xc{int(file_id)}.flac"
    if not path.exists():
        sys.exit(f"[ERROR] Missing audio file: {path}")

    # Load & resample to TARGET_SR, force mono for simplicity
    y, sr = librosa.load(path, sr=TARGET_SR, mono=True)
    if y.size == 0:
        return y

    # Mel-spectrogram for activity detection
    sg = lf.melspectrogram(y=y, sr=TARGET_SR, hop_length=HOP, n_mels=N_MELS)
    # Frame with highest mean energy
    centerpoint = int(np.argmax(sg.mean(axis=0)))
    M = float(sg[:, centerpoint].mean())
    mask_frames = (sg.mean(axis=0) >= (M / 20.0))  # boolean per time frame

    # Expand frame mask (length ~ T) into sample mask (length ~ len(y))
    audio_mask = np.zeros_like(y, dtype=bool)
    for i, keep in enumerate(mask_frames):
        start = i * HOP
        stop = min((i + 1) * HOP, len(y))
        audio_mask[start:stop] = keep

    # If mask ends up empty (rare), fall back to raw audio
    return y[audio_mask] if audio_mask.any() else y

def window_signal(y: np.ndarray, W: int = WIN_SAMPLES) -> list[np.ndarray]:
    """Slice non-overlapping windows of size W from y."""
    if y is None or y.size < W:
        return []
    n = len(y) // W
    return [y[i*W:(i+1)*W] for i in range(n)]

def extract_features(window: np.ndarray, sr: int = TARGET_SR) -> dict[str, float]:
    """
    Compute robust, fixed-length features by summarizing frame-wise stats.
    """
    # Spectral centroid (1 x T)
    sc = lf.spectral_centroid(y=window, sr=sr, hop_length=HOP)
    scv = sc[0] if sc.ndim == 2 else sc

    # Chroma (12 x T)
    chroma = lf.chroma_stft(y=window, sr=sr, hop_length=HOP)

    feats = {
        "sc_mean": float(np.mean(scv)),
        "sc_std":  float(np.std(scv)),
        "sc_p10":  float(np.percentile(scv, 10)),
        "sc_p50":  float(np.percentile(scv, 50)),
        "sc_p90":  float(np.percentile(scv, 90)),
    }
    # Per-chroma bin mean/std
    for k in range(chroma.shape[0]):
        v = chroma[k]
        feats[f"ch{k}_mean"] = float(np.mean(v))
        feats[f"ch{k}_std"]  = float(np.std(v))
    return feats

def featurize_windows(windows: list[np.ndarray],
                      labels: list[str],
                      genuses: list[str]) -> pd.DataFrame:
    rows = []
    for w, sp, ge in zip(windows, labels, genuses):
        row = {"species": sp, "genus": ge}
        row.update(extract_features(w))
        rows.append(row)
    return pd.DataFrame(rows)

def stratified_split_with_rare(files_df: pd.DataFrame,
                               label_col: str,
                               test_size: float,
                               random_state: int):
    """
    Split file_ids into train/test at the file level to avoid leakage.
    - Classes with >=2 files are stratified.
    - Classes with 1 file go entirely to train.
    - If test_size too small for stratification, it is bumped minimally.
    Returns (train_ids, test_ids, err) where err is None on success.
    """
    counts = files_df[label_col].value_counts()
    ok_classes = counts[counts >= 2].index
    files_ok = files_df[files_df[label_col].isin(ok_classes)].copy()
    files_rare = files_df[~files_df[label_col].isin(ok_classes)].copy()  # singletons

    if files_ok.empty:
        return None, None, "no_ok_classes"

    n_classes = files_ok[label_col].nunique()
    n_test = int(np.ceil(len(files_ok) * test_size))
    if n_test < n_classes:
        # increase test_size minimally so we can allocate >=1 per class
        test_size_adj = (n_classes / len(files_ok)) + 1e-9
    else:
        test_size_adj = test_size

    tr_ids, te_ids = train_test_split(
        files_ok["file_id"],
        test_size=test_size_adj,
        random_state=random_state,
        stratify=files_ok[label_col]
    )

    # ✅ Make both sides plain Python lists of int before combining
    tr_ids = list(map(int, tr_ids)) + files_rare["file_id"].astype(int).tolist()
    te_ids = list(map(int, te_ids))

    return tr_ids, te_ids, None


def main():
    print("[Info] Starting birdsong SVM training pipeline...")
    assert_paths()
    df = load_metadata()

    # -------- Load audio and compute masked lengths --------
    print("[Info] Loading & masking audio (this can take a bit)...")
    waves = {}
    lengths = []
    for fid in df["file_id"]:
        y_masked = load_audio_masked(int(fid))
        waves[int(fid)] = y_masked
        lengths.append(len(y_masked))
    df["length"] = lengths
    df["windows"] = (df["length"] // WIN_SAMPLES).astype(int)

    # -------- Build per-file table --------
    files = (
        df[["file_id", "genus", "species"]]
        .drop_duplicates(subset=["file_id"])
        .reset_index(drop=True)
    )

    # -------- Split by files (no leakage) --------
    print(f"[Info] Splitting by files with label level: {LABEL_LEVEL}")
    train_ids, test_ids, err = stratified_split_with_rare(
        files, label_col=LABEL_LEVEL, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    if err is not None:
        # fallback to genus if species failed
        if LABEL_LEVEL == "species":
            print("[Warn] Species-level stratification failed; falling back to genus...")
            train_ids, test_ids, err2 = stratified_split_with_rare(
                files, label_col="genus", test_size=TEST_SIZE, random_state=RANDOM_STATE
            )
            if err2 is not None:
                print("[Warn] Genus-level stratification failed; using unstratified split.")
                train_ids, test_ids = train_test_split(
                    files["file_id"], test_size=TEST_SIZE, random_state=RANDOM_STATE, shuffle=True
                )
                train_ids = list(pd.Index(train_ids).astype(int))
                test_ids = list(pd.Index(test_ids).astype(int))
        else:
            print("[Warn] Label-level stratification failed; using unstratified split.")
            train_ids, test_ids = train_test_split(
                files["file_id"], test_size=TEST_SIZE, random_state=RANDOM_STATE, shuffle=True
            )
            train_ids = list(pd.Index(train_ids).astype(int))
            test_ids = list(pd.Index(test_ids).astype(int))

    print(f"[Info] #train files: {len(train_ids)}, #test files: {len(test_ids)}")

    # -------- Build windows for train/test --------
    def windows_from_ids(id_list):
        Xw, y_labels, g_labels = [], [], []
        for fid in id_list:
            w = waves[int(fid)]
            chunks = window_signal(w, WIN_SAMPLES)
            if not chunks:
                continue
            genus = df.loc[df["file_id"] == fid, "genus"].values[0]
            species = df.loc[df["file_id"] == fid, "species"].values[0]
            for seg in chunks:
                Xw.append(seg)
                y_labels.append(species)
                g_labels.append(genus)
        return Xw, y_labels, g_labels

    print("[Info] Windowing audio...")
    Xw_train, y_train, g_train = windows_from_ids(train_ids)
    Xw_test,  y_test,  g_test  = windows_from_ids(test_ids)

    if not Xw_train or not Xw_test:
        sys.exit("[ERROR] Not enough windowed data. Check audio lengths, WIN_SAMPLES, and masking.")

    # -------- Feature extraction --------
    print("[Info] Extracting features...")
    train_df = featurize_windows(Xw_train, y_train, g_train)
    test_df  = featurize_windows(Xw_test,  y_test,  g_test)

    # Choose label column
    label_col = LABEL_LEVEL  # "species" or "genus"
    feature_cols = [c for c in train_df.columns if c not in ("species", "genus")]
    X_train = train_df[feature_cols].values
    y_train_lab = train_df[label_col].values
    X_test  = test_df[feature_cols].values
    y_test_lab  = test_df[label_col].values

    # -------- Model: Standardize + Linear SVM --------
    print("[Info] Training SVM...")
    clf = make_pipeline(
        StandardScaler(with_mean=True),
        SVC(kernel="linear", probability=False, random_state=RANDOM_STATE, class_weight=None)
        # If classes are very imbalanced, try class_weight="balanced"
    )
    clf.fit(X_train, y_train_lab)

    print("[Info] Evaluating...")
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test_lab, y_pred)
    print(f"\nAccuracy ({label_col}): {acc:.4f}\n")
    print(classification_report(y_test_lab, y_pred, zero_division=0))

    # -------- Save artifacts --------
    print("[Info] Saving artifacts: train.csv, test.csv, svm.sav")
    train_df.to_csv("train.csv", index=False)
    test_df.to_csv("test.csv", index=False)
    with open("svm.sav", "wb") as f:
        pickle.dump(clf, f)

    print("[Done] Training completed and artifacts saved.")

if __name__ == "__main__":
    main()
