from .models import *
from rest_framework import viewsets
from output.serializers import *


# Create your views here.
class TrustRateViewSet(viewsets.ModelViewSet):
    queryset = TrustRate.objects.all()
    serializer_class = TrustRate


class RoadGradeViewSet(viewsets.ModelViewSet):
    queryset = RoadGrade.objects.all()
    serializer_class = RoadGrade
