from django.db import models

class Evidence(models.Model):
    type = models.CharField(max_length=50)
    file = models.FileField(upload_to="evidence/")
    created_at = models.DateTimeField(auto_now_add=True)
