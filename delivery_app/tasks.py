import random
from welbex.celery import app
from .models import Vehicle, Location


@app.task
def update_vehicles_3_minutes():
    vehicles = Vehicle.objects.all()
    all_locations = list(Location.objects.all())
    for vehicle in vehicles:
        new_location = random.choice(all_locations)

        vehicle.current_location = new_location
        vehicle.save()

