from django.db import models


class RoadGrade(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=False)
    grade = models.FloatField()