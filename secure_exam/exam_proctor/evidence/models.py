from django.db import models

class Evidence(models.Model):
    type = models.CharField(max_length=50)
    file = models.FileField(upload_to="evidence/")
    created_at = models.DateTimeField(auto_now_add=True)

class ProctorEvidence(models.Model):
    candidate_id = models.CharField(max_length=50)
    evidence_type = models.CharField(max_length=50)
    file = models.FileField(upload_to="evidence/")
    created_at = models.DateTimeField(auto_now_add=True)
