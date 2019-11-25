from django.db import models


class TrustRate(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=False)
    rate = models.FloatField()
