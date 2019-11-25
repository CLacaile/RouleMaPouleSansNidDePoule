from .models import TrustRate, RoadGrade
from rest_framework import serializers


class TrustRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrustRate
        fields = ['id', 'timestamp', 'rate', 'trust_waypoint']


class RoadGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadGrade
        fields = ['id', 'timestamp', 'grade', 'road_waypoint']
