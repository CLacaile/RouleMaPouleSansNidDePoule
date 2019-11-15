from django.db import models
from .path import Path


class Waypoint(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=False)
    longitude = models.FloatField()
    latitude = models.FloatField()
    path = models.ForeignKey(Path, on_delete=models.CASCADE)
