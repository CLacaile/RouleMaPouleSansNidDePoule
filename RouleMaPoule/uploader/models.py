from django.db import models

# Create your models here.


class Path(models.Model):
    id = models.AutoField(primary_key=True)
    id_sensor = models.IntegerField()