import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rms_project.settings')
django.setup()

from restaurant.models import MenuItem

try:
    item = MenuItem.objects.get(name='Paneer Butter Masala')
    item.image_url = 'paneer.jpg'
    item.save()
    print('✅ Database Updated! Paneer Butter Masala now points to paneer.jpg')
except Exception as e:
    print('Error:', e)
