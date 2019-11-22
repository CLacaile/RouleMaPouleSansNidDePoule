from django.shortcuts import render
from rest_framework import viewsets
from .models import Path, Waypoint, Acceleration
from input.serializers import PathSerializer, WaypointSerializer, AccelerationSerializer

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