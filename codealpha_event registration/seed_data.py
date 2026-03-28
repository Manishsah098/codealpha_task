import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_registration.settings')
django.setup()

from django.contrib.auth.models import User
from events.models import Event

def seed_data():
    # Ensure admin user exists
    admin, _ = User.objects.get_or_create(username='admin', defaults={'is_staff': True, 'is_superuser': True, 'email': 'admin@eventhub.com'})
    if _:
        admin.set_password('admin123')
        admin.save()
    
    events = [
        {
            'title': 'Tech Conference 2026',
            'description': 'A massive conference about the latest in AI, Quantum Computing, and Web 3.0. Join industry leaders for keynote speeches and hands-on workshops.',
            'date': timezone.now() + timedelta(days=30),
            'location': 'San Francisco, CA',
            'organizer': admin
        },
        {
            'title': 'Global Music Festival',
            'description': 'Experience three days of non-stop music from top international artists across five stages. Food trucks, art installations, and more.',
            'date': timezone.now() + timedelta(days=45),
            'location': 'Austin, TX',
            'organizer': admin
        },
        {
            'title': 'Startup Pitch Night',
            'description': 'Watch 10 curated early-stage startups pitch their revolutionary ideas to a panel of top-tier venture capitalists and angel investors.',
            'date': timezone.now() + timedelta(days=15),
            'location': 'New York, NY',
            'organizer': admin
        },
        {
            'title': 'Wellness & Yoga Retreat',
            'description': 'A weekend dedicated to mindfulness, yoga sessions with masters, and organic nutrition workshops in a serene mountain setting.',
            'date': timezone.now() + timedelta(days=60),
            'location': 'Asheville, NC',
            'organizer': admin
        },
        {
            'title': 'Future of Finance Summit',
            'description': 'Exploring the impact of DeFi, CBDCs, and AI on the global financial landscape. A must-attend for fintech enthusiasts and banking professionals.',
            'date': timezone.now() + timedelta(days=22),
            'location': 'London, UK',
            'organizer': admin
        },
        {
            'title': 'Art & Design Expo',
            'description': 'Showcasing contemporary art, digital installations, and industrial design from emerging creators around the world.',
            'date': timezone.now() + timedelta(days=40),
            'location': 'Berlin, Germany',
            'organizer': admin
        },
        {
            'title': 'Gourmet Food & Wine Expo',
            'description': 'Taste exquisite cuisines from Michelin-starred chefs and sample vintage wines from the world\'s finest vineyards.',
            'date': timezone.now() + timedelta(days=10),
            'location': 'Paris, France',
            'organizer': admin
        },
        {
            'title': 'Cyber Security Bootcamp',
            'description': 'Intensive 2-day workshop on ethical hacking, network defense, and the latest threat mitigation strategies.',
            'date': timezone.now() + timedelta(days=18),
            'location': 'Tel Aviv, Israel',
            'organizer': admin
        },
        {
            'title': 'Sustainable Living Fair',
            'description': 'Learn about eco-friendly technologies, zero-waste lifestyle tips, and urban farming techniques for a greener future.',
            'date': timezone.now() + timedelta(days=50),
            'location': 'Portland, OR',
            'organizer': admin
        },
        {
            'title': 'Blockchain & Crypto Expo',
            'description': 'The ultimate gathering for crypto enthusiasts, miners, and developers to discuss the next evolution of decentralized tech.',
            'date': timezone.now() + timedelta(days=35),
            'location': 'Dubai, UAE',
            'organizer': admin
        },
        {
            'title': 'Adventure Film Festival',
            'description': 'Screening the best independent films documenting mountain climbing, surfing, and extreme expeditions from across the globe.',
            'date': timezone.now() + timedelta(days=75),
            'location': 'Denver, CO',
            'organizer': admin
        },
        {
            'title': 'Gaming & Esports Arena',
            'description': 'Huge tournament featuring top competitive games, cosplay contests, and legendary developer Q&A sessions.',
            'date': timezone.now() + timedelta(days=12),
            'location': 'Seoul, South Korea',
            'organizer': admin
        },
        {
            'title': 'AI Ethics & Future Summit',
            'description': 'A deep dive into the societal impact of Artificial Intelligence, featuring philosophers, engineers, and policy makers.',
            'date': timezone.now() + timedelta(days=25),
            'location': 'Oxford, UK',
            'organizer': admin
        },
        {
            'title': 'Starlight Movie Night',
            'description': 'An outdoor cinematic experience showing classic films under the stars with gourmet snacks and cozy seating.',
            'date': timezone.now() + timedelta(days=5),
            'location': 'Los Angeles, CA',
            'organizer': admin
        }
    ]

    for event_data in events:
        obj, created = Event.objects.get_or_create(title=event_data['title'], defaults=event_data)
        if not created:
            # Update existing events to have more description
            for key, value in event_data.items():
                setattr(obj, key, value)
            obj.save()
    
    print(f"Successfully seeded {len(events)} events.")

if __name__ == '__main__':
    seed_data()
