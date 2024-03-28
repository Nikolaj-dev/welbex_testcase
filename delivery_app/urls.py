from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CargoViewSet, VehicleViewSet, LocationViewSet


router = DefaultRouter()
router.register(r'cargos', CargoViewSet)
router.register(r'vehicles', VehicleViewSet)
router.register(r'locations', LocationViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
