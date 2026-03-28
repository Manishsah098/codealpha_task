import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rms_project.settings')
django.setup()

from restaurant.models import MenuItem
from decimal import Decimal
import math

print("Updating menu item prices to realistic INR values...")
for item in MenuItem.objects.all():
    # Only update if the price is still small (fake USD price)
    if float(item.price) < 100:
        # Multiply by roughly 25 to convert 14.99 to ~375
        real_price = math.ceil(float(item.price) * 25 / 10.0) * 10
        item.price = Decimal(str(real_price))
        item.save()
        print(f"Updated {item.name}: ₹{item.price}")

print("Prices updated to realistic INR!")
