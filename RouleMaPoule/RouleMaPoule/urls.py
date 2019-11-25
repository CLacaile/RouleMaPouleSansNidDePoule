"""RouleMaPoule URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from rest_framework import routers
from input.views import PathViewSet, WaypointViewSet, AccelerationViewSet
from output.views import RoadGradeViewSet, TrustRateViewSet


router = routers.DefaultRouter()
router.register(r'api/v1.0/input/path', PathViewSet)
router.register(r'api/v1.0/input/waypoint', WaypointViewSet)
router.register(r'api/v1.0/input/acceleration', AccelerationViewSet)
router.register(r'api/v1.0/output/roadgrade', RoadGradeViewSet)
router.register(r'api/v1.0/output/trustrate', TrustRateViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
