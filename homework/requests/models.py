from django.db import models


class RequestEntry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=6)
    params = models.TextField()
    headers = models.TextField()
