from rest_framework import serializers
from .models import Location, Cargo, Vehicle


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    unique_number = serializers.CharField(read_only=True)
    current_location = serializers.CharField(read_only=True)

    class Meta:
        model = Vehicle
        fields = ['pk', 'unique_number', 'capacity', 'current_location']


class CargoSerializer(serializers.ModelSerializer):
    nearest_vehicles = VehicleSerializer(many=True, read_only=True)
    pick_up_location_zip_code = serializers.CharField(source='pick_up_location.zip_code', read_only=True)
    delivery_location_zip_code = serializers.CharField(source='delivery_location.zip_code', read_only=True)
    pick_up_zip = serializers.CharField(write_only=True)
    delivery_zip = serializers.CharField(write_only=True)

    class Meta:
        model = Cargo
        fields = [
            'pk',
            'pick_up_location_zip_code',
            'delivery_location_zip_code',
            'weight',
            'description',
            'nearest_vehicles',
            'pick_up_zip',
            'delivery_zip'
        ]

    def create(self, validated_data):
        # Extract pick_up_zip and delivery_zip from validated_data
        pick_up_zip = validated_data.pop('pick_up_zip', None)
        delivery_zip = validated_data.pop('delivery_zip', None)

        pick_up_location, _ = Location.objects.get_or_create(zip_code=pick_up_zip)
        delivery_location, _ = Location.objects.get_or_create(zip_code=delivery_zip)

        validated_data['pick_up_location'] = pick_up_location
        validated_data['delivery_location'] = delivery_location

        return super().create(validated_data)


class CargoUpdateSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cargo
        fields = [
            'pk',
            'weight',
            'description',
        ]

    def update(self, instance, validated_data):
        instance.weight = validated_data.get('weight', instance.weight)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        return instance


class VehicleUpdateSerializer(serializers.ModelSerializer):
    current_location_zip_code = serializers.CharField(write_only=True)
    pk = serializers.IntegerField(read_only=True)
    unique_number = serializers.CharField(read_only=True)
    capacity = serializers.CharField(read_only=True)
    current_location = serializers.CharField(read_only=True)

    class Meta:
        model = Vehicle
        fields = ['pk', 'unique_number', 'capacity', 'current_location', 'current_location_zip_code']

    def update(self, instance, validated_data):
        current_location_zip_code = validated_data.get('current_location_zip_code')

        if current_location_zip_code:
            try:
                location = Location.objects.get(zip_code=current_location_zip_code)
                instance.current_location = location
            except Location.DoesNotExist:
                raise serializers.ValidationError("Location does not exist.")

        instance.save()
        return instance
