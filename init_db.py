import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welbex.settings')
django.setup()

import csv
from delivery_app.models import Location, Vehicle


def load_data_from_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            location = Location.objects.create(
                city=row['city'],
                state=row['state_name'],
                zip_code=row['zip'],
                latitude=float(row['lat']),
                longitude=float(row['lng'])
            )
            location.save()


def load_vehicle_data():
    for i in range(50, 1001, 50):
        Vehicle.objects.create(
            capacity=i
        )


csv_file_path = 'uszips.csv'


if __name__ == '__main__':
    print("Началась выгрузка данных...")
    load_data_from_csv(csv_file_path)
    load_vehicle_data()
    print("Выгрузка данных завершена.")

