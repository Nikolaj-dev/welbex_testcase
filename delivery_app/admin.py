from django.contrib import admin
from .models import Location, Cargo, Vehicle

admin.site.register(Location)


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pick_up_location', 'delivery_location', 'weight', 'description')


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('unique_number', 'current_location', 'capacity')
