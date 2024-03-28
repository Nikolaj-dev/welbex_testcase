import random
import string
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Location(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.city}, {self.state}, {self.zip_code}"


class Cargo(models.Model):
    pick_up_location = models.ForeignKey(Location, related_name='pick_up_cargo', on_delete=models.CASCADE)
    delivery_location = models.ForeignKey(Location, related_name='delivery_cargo', on_delete=models.CASCADE)
    weight = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(1000)])
    description = models.TextField()

    def __str__(self):
        return f"Cargo from {self.pick_up_location} to {self.delivery_location}"


class Vehicle(models.Model):
    current_location = models.ForeignKey(Location, related_name='vehicles', on_delete=models.CASCADE, blank=True)
    capacity = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(1000)])
    unique_number = models.CharField(max_length=5, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            all_locations = Location.objects.all()
            if all_locations.exists():
                self.current_location = random.choice(all_locations)

            random_number = random.randint(1000, 9999)
            random_letter = random.choice(string.ascii_uppercase)
            self.unique_number = f"{random_number}{random_letter}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Vehicle {self.unique_number} at {self.current_location}"
