from django.db import models
from input.models import *


class TrustRate(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=False)
    rate = models.FloatField()
    trust_waypoint = models.ForeignKey(Waypoint, on_delete=models.CASCADE, related_name="trustrate")
