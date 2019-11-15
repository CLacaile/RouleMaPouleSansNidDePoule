from django.db import models
from .waypoint import Waypoint


class Acceleration(models.Model):
    id = models.AutoField(primary_key=True)
    accelx = models.IntegerField()
    accely = models.IntegerField()
    accelz = models.IntegerField()
    waypoint = models.ForeignKey(Waypoint, on_delete=models.CASCADE)
