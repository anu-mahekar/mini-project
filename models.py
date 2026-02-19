# birds/models.py
from django.db import models

# birds/models.py
from django.db import models

class Bird(models.Model):
    # Core ID fields (from your metadata import)
    genus = models.CharField(max_length=64)
    species = models.CharField(max_length=64)
    binomial = models.CharField(max_length=140, unique=True)  # "Genus species"
    english_cname = models.CharField(max_length=140, blank=True, default="")

    # Enrichment fields
    habitat = models.TextField(blank=True, default="")
    diet = models.TextField(blank=True, default="")
    notes = models.TextField(blank=True, default="")  # free-form summary/description

    # Optional images + credits/attribution
    image_url_1 = models.URLField(blank=True, default="")
    image_credit_1 = models.CharField(max_length=255, blank=True, default="")
    image_url_2 = models.URLField(blank=True, default="")
    image_credit_2 = models.CharField(max_length=255, blank=True, default="")
    image_url_3 = models.URLField(blank=True, default="")
    image_credit_3 = models.CharField(max_length=255, blank=True, default="")

    # Provenance
    wikipedia_title = models.CharField(max_length=255, blank=True, default="")
    wikipedia_url = models.URLField(blank=True, default="")
    wikidata_qid = models.CharField(max_length=32, blank=True, default="")

    class Meta:
        indexes = [
            models.Index(fields=["genus", "species"]),
            models.Index(fields=["binomial"]),
        ]

    def __str__(self):
        return f"{self.binomial} — {self.english_cname}"


class PredictionLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='predictions', null=True, blank=True)
    filename = models.CharField(max_length=255)
    predicted_label = models.CharField(max_length=140)
    confidence = models.FloatField()
    top_votes_json = models.JSONField(default=dict)
    matched_bird = models.ForeignKey(Bird, null=True, blank=True, on_delete=models.SET_NULL)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]
