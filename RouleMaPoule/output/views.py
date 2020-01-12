from .models.road_grade import RoadGrade
from .models.trust_rate import TrustRate
from rest_framework import viewsets
from output.serializers import TrustRateSerializer, RoadGradeSerializer
from rest_framework.permissions import IsAuthenticated


class TrustRateViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    """
    API endpoint that allows Trustrates to be viewed or edited    
    """
    queryset = TrustRate.objects.all()
    serializer_class = TrustRateSerializer
    pagination_class = None


class RoadGradeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    """
    API endpoint that allows Roadgrades to be viewed or edited    
    """
    queryset = RoadGrade.objects.all()
    serializer_class = RoadGradeSerializer
    pagination_class = None
