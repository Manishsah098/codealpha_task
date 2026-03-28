import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rms_project.settings')
django.setup()

from restaurant.models import MenuItem

non_veg_items = [
    "Classic Angus Burger",
    "Double Trouble",
    "Butter Chicken",
    "Chicken Tikka Masala",
    "Chicken Biryani"
]

print("Updating veg/non-veg status...")
for item in MenuItem.objects.all():
    if item.name in non_veg_items:
        item.is_veg = False
    else:
        item.is_veg = True
    item.save()

print("Status Updated Successfully!")
