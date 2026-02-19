# birds/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Bird, PredictionLog

class BirdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bird
        fields = (
            "genus", "species", "binomial", "english_cname",
            "habitat", "diet", "notes",
            "image_url_1", "image_credit_1",
            "image_url_2", "image_credit_2",
            "image_url_3", "image_credit_3",
            "wikipedia_title", "wikipedia_url", "wikidata_qid",
        )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)

class PredictionLogSerializer(serializers.ModelSerializer):
    bird = BirdSerializer(read_only=True)
    
    class Meta:
        model = PredictionLog
        fields = (
            'id', 'created_at', 'filename', 'predicted_label',
            'confidence', 'top_votes_json', 'bird'
        )
        read_only_fields = ('id', 'created_at')
