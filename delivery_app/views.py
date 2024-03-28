from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from geopy.distance import geodesic
from .models import Cargo, Vehicle, Location
from .serializers import CargoSerializer, VehicleSerializer, LocationSerializer, CargoUpdateSerializer, \
    VehicleUpdateSerializer


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 50

    def get_serializer_class(self):
        if self.action == 'update':
            return CargoUpdateSerializer
        return CargoSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        min_weight = request.query_params.get('min_weight')
        max_weight = request.query_params.get('max_weight')
        max_distance = request.query_params.get('max_distance')
        location_zip_code = request.query_params.get('location_zip_code')

        if min_weight:
            queryset = queryset.filter(weight__gte=min_weight)
        if max_weight:
            queryset = queryset.filter(weight__lte=max_weight)
        if location_zip_code and max_distance:
            vehicles = self.get_vehicles_handler(
                pick_up_location_id=str(location_zip_code),
                custom_distance=float(max_distance)
            )
            return Response(vehicles)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        list_view = [
            {
                'pk': cargo['pk'],
                'pick_up_location_zip_code': cargo['pick_up_location_zip_code'],
                'delivery_location_zip_code': cargo['delivery_location_zip_code'],
                'nearest_vehicles': self.get_vehicles_handler(
                    cargo['pick_up_location_zip_code'],
                    lower_than_450_miles=True
                )
            }
            for cargo in data
        ]

        return Response(list_view)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        retrieve_view = {
            'pk': data['pk'],
            'pick_up_location_zip_code': data['pick_up_location_zip_code'],
            'delivery_location_zip_code': data['delivery_location_zip_code'],
            'weight': data['weight'],
            'description': data['description'],
            'all_vehicles': self.get_vehicles_handler(data['pick_up_location_zip_code'], lower_than_450_miles=False)
        }

        return Response(retrieve_view)

    def get_vehicles_handler(self, pick_up_location_id, lower_than_450_miles: bool = None, custom_distance=None):
        pick_up_location = Location.objects.get(zip_code=pick_up_location_id)
        all_vehicles = Vehicle.objects.all()

        vehicles = []

        for vehicle in all_vehicles:
            distance_to_pick_up = geodesic((vehicle.current_location.latitude, vehicle.current_location.longitude),
                                           (pick_up_location.latitude, pick_up_location.longitude)).miles
            if lower_than_450_miles:
                if distance_to_pick_up <= 450:
                    vehicles.append({
                        'unique_number': vehicle.unique_number,
                        'distance_to_pick_up': distance_to_pick_up
                    })

            elif custom_distance:
                if distance_to_pick_up <= custom_distance:
                    vehicles.append({
                        'unique_number': vehicle.unique_number,
                        'distance_to_pick_up': distance_to_pick_up
                    })
            else:
                vehicles.append({
                    'unique_number': vehicle.unique_number,
                    'distance_to_pick_up': distance_to_pick_up
                })

        if lower_than_450_miles:
            return len(vehicles)
        else:
            return vehicles


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 50

    def get_serializer_class(self):
        if self.action == 'update':
            return VehicleUpdateSerializer
        return VehicleSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 50
