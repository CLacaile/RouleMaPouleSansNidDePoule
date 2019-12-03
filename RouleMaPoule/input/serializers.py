from .models import Path, Waypoint, Acceleration
from rest_framework import serializers


class PathSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Path
        fields = ['id', 'id_sensor']


class WaypointSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Waypoint
        fields = ['id', 'longitude', 'latitude', 'path']


class AccelerationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Acceleration
        fields = ['id', 'timestamp', 'accelx', 'accely', 'accelz', 'waypoint']


