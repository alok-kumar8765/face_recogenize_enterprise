from django.db import models

class Candidate(models.Model):
    registration_id = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=100)

    photo = models.ImageField(upload_to='photos/')
    face_encoding = models.BinaryField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.registration_id} - {self.full_name}"
