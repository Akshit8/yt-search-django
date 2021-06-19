from django.db import models

class VideoModel(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    title = models.TextField()
    description = models.TextField()
    published_at = models.DateTimeField()
    thumbnail = models.CharField(max_length=200)
