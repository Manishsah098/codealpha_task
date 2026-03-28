import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rms_project.settings')
django.setup()

from restaurant.models import MenuItem

image_map = {
    'Butter Chicken': 'https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=800&q=80',
    'Paneer Butter Masala': 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=800&q=80',
    'Chana Masala': 'https://images.unsplash.com/photo-1645177623547-8296fd2d4d42?w=800&q=80',
    'Dal Makhani': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800&q=80',
    'Biryani': 'https://images.unsplash.com/photo-1563379091339-03b21bc4a4f8?w=800&q=80',
    'Naan': 'https://images.unsplash.com/photo-1574894709920-11b28e7367e3?w=800&q=80',
    'Samosa (2pcs)': 'https://images.unsplash.com/photo-1601050690597-df056fbec701?w=800&q=80',
    'Tandoori Chicken': 'https://images.unsplash.com/photo-1626074353765-517a681e40be?w=800&q=80',
    'Palak Paneer': 'https://images.unsplash.com/photo-1610192244261-3f33de8f5f84?w=800&q=80',
    'Malai Kofta': 'https://images.unsplash.com/photo-1585937421612-7110e3bb17ad?w=800&q=80',
    'Gulab Jamun': 'https://images.unsplash.com/photo-1624462966581-20a212bbcc0d?w=800&q=80'
}

for name, url in image_map.items():
    MenuItem.objects.filter(name=name).update(image_url=url)
    print(f"Updated Image for {name}")

print("All Indian food images updated successfully.")
