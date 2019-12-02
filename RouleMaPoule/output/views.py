from .models.road_grade import RoadGrade
from .models.trust_rate import TrustRate
from rest_framework import viewsets
from output.serializers import TrustRateSerializer, RoadGradeSerializer


class TrustRateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Trustrates to be viewed or edited    
    """
    queryset = TrustRate.objects.all()
    serializer_class = TrustRateSerializer


class RoadGradeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Roadgrades to be viewed or edited    
    """
    queryset = RoadGrade.objects.all()
    serializer_class = RoadGradeSerializer
