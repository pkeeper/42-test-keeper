from django.db import models


class RequestEntry(models.Model):
    """
    Model for Request Log entry
    """
    PRIORITIES = []
    for i in range(1, 11):
        PRIORITIES.append((i, i))
    created_at = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=6)
    params = models.TextField(blank=True)
    headers = models.TextField()
    priority = models.IntegerField(default=1, choices=PRIORITIES)

    def __unicode__(self):
        return self.path
