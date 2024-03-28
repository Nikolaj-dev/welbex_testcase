import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welbex.settings')
django.setup()

from delivery_app.models import Vehicle


def load_vehicle_data():
    Vehicle.objects.all().delete()
    for i in range(50, 1001, 50):
        Vehicle.objects.create(
            capacity=i
        )


if __name__ == '__main__':
    print("Началась выгрузка данных...")
    load_vehicle_data()
    print("Выгрузка данных завершена.")
