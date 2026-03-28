import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rms_project.settings')
django.setup()

from restaurant.models import Inventory

print("Refilling inventory...")
count = 0
for item in Inventory.objects.all():
    item.quantity = 1000.00
    item.save()
    count += 1

print(f"Inventory Refilled Successfully! Boosted {count} items to 1000 units.")
