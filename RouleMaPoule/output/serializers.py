from .models import *
from rest_framework import serializers


class TrustRateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model: TrustRate
        fields: ['timestamp', 'rate']


class RoadGradeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model: RoadGrade
        fields: ['timestamp', 'grade']
