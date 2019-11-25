from django.shortcuts import render
from .models import Path, Waypoint, Acceleration
from rest_framework.exceptions import ParseError
from input.serializers import PathSerializer, WaypointSerializer, AccelerationSerializer
from rest_framework import viewsets
from rest_framework import views
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

class PathViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Path to be viewed or edited    
    """
    queryset = Path.objects.all()
    serializer_class = PathSerializer

class WaypointViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Waypoint to be viewed or edited    
    """
    queryset = Waypoint.objects.all()
    serializer_class = WaypointSerializer

class AccelerationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Acceleration to be viewed or edited    
    """
    queryset = Acceleration.objects.all()
    serializer_class = AccelerationSerializer

class CSVFileUploadParser(FileUploadParser):
    media_type = 'text/csv'

class FileUploadView(views.APIView):
    parser_classes = [CSVFileUploadParser]

    def put(self, request, filename, format=None):
        if 'file' not in request.data:
            raise ParseError("Empty content")
        csv_file = request.data['file']



        return Response(status=204)