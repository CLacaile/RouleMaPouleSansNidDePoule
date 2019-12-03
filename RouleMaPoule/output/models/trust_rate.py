from django.db import models
from input.models import *


class TrustRate(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=False)
    rate = models.FloatField()
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
