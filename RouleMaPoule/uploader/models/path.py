from django.db import models


class Path(models.Model):
    id = models.AutoField(primary_key=True)
    id_sensor = models.IntegerField()
