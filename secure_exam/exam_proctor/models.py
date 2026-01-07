from django.db import models
# exam_proctor/models.py

from django.contrib.auth.models import User

class ProctorViolation(models.Model):
    type = models.CharField(max_length=50)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type


class Institute(models.Model):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, unique=True)
    api_key = models.CharField(max_length=64, unique=True)

class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_id = models.CharField(max_length=50)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    face_encoding = models.BinaryField()
