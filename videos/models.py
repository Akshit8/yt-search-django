from django.db import models

class VideoModel(models.Model):
    title = models.TextField()
    description = models.TextField()
    published_at = models.DateTimeField()
    thumbnail = models.CharField(max_length=200)
