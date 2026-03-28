import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rms_project.settings')
django.setup()

from restaurant.models import MenuItem

images = {
    "Classic Angus Burger": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&q=80",
    "Truffle Mushroom Burger": "https://images.unsplash.com/photo-1550547660-d9450f859349?w=500&q=80",
    "Double Trouble": "https://images.unsplash.com/photo-1586190848861-99aa4a171e90?w=500&q=80",
    "Butter Chicken": "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=500&q=80",
    "Chicken Tikka Masala": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=500&q=80",
    "Paneer Butter Masala": "https://images.unsplash.com/photo-1631452180519-c014fe946bc0?w=500&q=80",
    "Samosa (2 pcs)": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500&q=80",
    "Chicken Biryani": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=500&q=80",
    "Chana Masala": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=500&q=80"
}

default_indian = "https://images.unsplash.com/photo-1617692855027-33b14f061079?w=500&q=80"

for item in MenuItem.objects.all():
    if item.name in images:
        item.image_url = images[item.name]
    elif item.restaurant_name == 'Spice of India':
        item.image_url = default_indian
    item.save()

print("Images Updated Correctly!")
