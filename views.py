# birds/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, parsers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from django.db import transaction
from pathlib import Path
import uuid

from .predict_service import predict_audio_file
from .models import Bird, PredictionLog
from .serializers import BirdSerializer, UserSerializer, PredictionLogSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not username or not email or not password:
            return Response(
                {'detail': 'Username, email, and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(username=username).exists():
            return Response(
                {'detail': 'Username already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(email=email).exists():
            return Response(
                {'detail': 'Email already registered.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'detail': 'Username and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        
        if not user:
            return Response(
                {'detail': 'Invalid credentials.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        token, _ = Token.objects.get_or_create(user=user)
        login(request, user)
        
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            request.user.auth_token.delete()
        except:
            pass
        logout(request)
        return Response({'detail': 'Successfully logged out.'})

class UserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({
            'user': UserSerializer(request.user).data
        })

class PredictView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request, *args, **kwargs):
        """
        Accepts multipart/form-data with field 'audio' (file).
        Requires authentication.
        """
        f = request.FILES.get("audio")
        if not f:
            return Response({"detail": "No 'audio' file provided."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Save to a temp path under MEDIA_ROOT/predict/
        media_root = Path(settings.MEDIA_ROOT)
        predict_dir = media_root / "predict_uploads"
        predict_dir.mkdir(parents=True, exist_ok=True)
        temp_name = f"{uuid.uuid4().hex}_{f.name}"
        temp_path = predict_dir / temp_name
        with temp_path.open("wb") as out:
            for chunk in f.chunks():
                out.write(chunk)

        try:
            # Run prediction
            try:
                pred = predict_audio_file(temp_path)
            except FileNotFoundError as e:
                import traceback
                traceback.print_exc()
                return Response({
                    "detail": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                import traceback
                traceback.print_exc()
                return Response({
                    "detail": f"Prediction error: {str(e)}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            label = pred.get("pred_top")
            windows = pred.get("windows", 0)

            if not label:
                return Response({
                    "prediction": {
                        "label": None,
                        "confidence": 0.0,
                        "votes": {},
                        "windows": windows,
                    },
                    "bird": None,
                    "ambiguous": False,
                    "message": "Audio too short after masking to make a prediction."
                }, status=status.HTTP_200_OK)

            # Try to match DB record.
            matched = None
            binomial = None
            if " " in label:
                binomial = label.strip()
                matched = Bird.objects.filter(binomial__iexact=binomial).first()
            else:
                genus_hint = request.data.get("genus_hint", "").strip()
                if genus_hint:
                    binomial = f"{genus_hint} {label}"
                    matched = Bird.objects.filter(binomial__iexact=binomial).first()
                else:
                    candidates = Bird.objects.filter(species__iexact=label)
                    matched = candidates.first() if candidates.exists() else None

            with transaction.atomic():
                plog = PredictionLog.objects.create(
                    user=request.user,
                    filename=f.name,
                    predicted_label=label,
                    confidence=float(pred.get("confidence", 0.0)),
                    top_votes_json=pred.get("votes", {}),
                    matched_bird=matched,
                )

            payload = {
                "prediction": {
                    "label": label,
                    "confidence": pred["confidence"],
                    "votes": pred["votes"],
                    "windows": windows,
                },
                "bird": BirdSerializer(matched).data if matched else None,
                "ambiguous": (matched is None and " " not in label),
            }
            return Response(payload, status=status.HTTP_200_OK)

        finally:
            # Clean up the uploaded file
            try:
                temp_path.unlink(missing_ok=True)
            except Exception:
                pass

class HistoryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        predictions = PredictionLog.objects.filter(user=request.user)[:50]  # Last 50
        serializer = PredictionLogSerializer(predictions, many=True)
        return Response({
            'count': len(serializer.data),
            'results': serializer.data
        })
