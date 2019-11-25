from .models import Path, Waypoint, Acceleration
from rest_framework import serializers
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

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


class FileUploadView(views.APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        # ...
        # do some stuff with uploaded file
        # ...
        return Response(status=204)