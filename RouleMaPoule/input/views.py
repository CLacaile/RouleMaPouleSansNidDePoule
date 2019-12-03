from django.shortcuts import render
from .models import Path, Waypoint, Acceleration
from rest_framework.exceptions import ParseError
from input.serializers import PathSerializer, WaypointSerializer, AccelerationSerializer
from rest_framework import viewsets
from rest_framework import views
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .processing import csv_upload as CSV
from rest_framework.permissions import IsAuthenticated


class PathViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    """
    API endpoint that allows Path to be viewed or edited    
    """
    queryset = Path.objects.all()
    serializer_class = PathSerializer

class WaypointViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    """
    API endpoint that allows Waypoint to be viewed or edited    
    """
    queryset = Waypoint.objects.all()
    serializer_class = WaypointSerializer

class AccelerationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    """
    API endpoint that allows Acceleration to be viewed or edited    
    """
    queryset = Acceleration.objects.all()
    serializer_class = AccelerationSerializer



class FileUploadView(views.APIView):
    permission_classes = (IsAuthenticated,)

    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        if 'file' not in request.data:
            raise ParseError("Empty content")
        CSV.csv_upload(request.data['file'].read().decode("utf-8")	)
        return Response(status=204)