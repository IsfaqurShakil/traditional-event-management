import os
import django
import random
from datetime import datetime, timedelta

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_platform.settings')
django.setup()

from django.contrib.auth import get_user_model
from events.models import EventType, Event
from venues.models import Venue
from services.models import ServiceCategory, Service

User = get_user_model()

# Create admin user if it doesn't exist
if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123',
        role='admin'
    )
    print("Admin user created")

# Create organizer user if it doesn't exist
if not User.objects.filter(username='organizer').exists():
    organizer_user = User.objects.create_user(
        username='organizer',
        email='organizer@example.com',
        password='organizer123',
        role='organizer',
        first_name='John',
        last_name='Doe'
    )
    print("Organizer user created")

# Create regular user if it doesn't exist
if not User.objects.filter(username='user').exists():
    regular_user = User.objects.create_user(
        username='user',
        email='user@example.com',
        password='user123',
        role='user',
        first_name='Jane',
        last_name='Smith'
    )
    print("Regular user created")

# Create event types
event_types = [
    'Wedding',
    'Engagement',
    'Holud Ceremony',
    'Birthday Party',
    'Corporate Event',
    'Cultural Program',
    'Religious Ceremony',
    'Conference',
    'Exhibition',
    'Concert'
]

for event_type in event_types:
    EventType.objects.get_or_create(name=event_type)
print("Event types created")

# Create venues
venues_data = [
    {
        'name': 'Royal Palace Convention Center',
        'address': '123 Main Street',
        'city': 'Dhaka',
        'capacity': 500,
        'cost_per_day': 50000,
        'contact_person': 'Ahmed Khan',
        'contact_phone': '+880 1234 567890',
        'contact_email': 'royal@example.com',
        'description': 'A luxurious convention center for all your grand events.',
        'is_available': True
    },
    {
        'name': 'Green View Garden',
        'address': '456 Park Avenue',
        'city': 'Chittagong',
        'capacity': 300,
        'cost_per_day': 35000,
        'contact_person': 'Fatima Rahman',
        'contact_phone': '+880 1234 567891',
        'contact_email': 'greenview@example.com',
        'description': 'A beautiful garden venue perfect for outdoor events.',
        'is_available': True
    },
    {
        'name': 'Heritage Hall',
        'address': '789 Old Town Road',
        'city': 'Sylhet',
        'capacity': 200,
        'cost_per_day': 25000,
        'contact_person': 'Rahim Ali',
        'contact_phone': '+880 1234 567892',
        'contact_email': 'heritage@example.com',
        'description': 'A traditional venue with rich cultural heritage.',
        'is_available': True
    }
]

for venue_data in venues_data:
    Venue.objects.get_or_create(
        name=venue_data['name'],
        defaults=venue_data
    )
print("Venues created")

# Create events
events_data = [
    {
        'name': 'Grand Wedding Celebration',
        'description': 'A luxurious wedding celebration with traditional South Asian customs.',
        'start_date': datetime.now().date() + timedelta(days=30),
        'end_date': datetime.now().date() + timedelta(days=30),
        'start_time': '18:00',
        'end_time': '23:00',
        'capacity': 400,
        'price': 2000,
        'status': 'upcoming',
        'is_featured': True
    },
    {
        'name': 'Annual Cultural Festival',
        'description': 'Celebrate the rich cultural heritage of South Asia with music, dance, and food.',
        'start_date': datetime.now().date() + timedelta(days=45),
        'end_date': datetime.now().date() + timedelta(days=47),
        'start_time': '10:00',
        'end_time': '22:00',
        'capacity': 500,
        'price': 1500,
        'status': 'upcoming',
        'is_featured': True
    },
    {
        'name': 'Corporate Conference',
        'description': 'A professional conference for business leaders and entrepreneurs.',
        'start_date': datetime.now().date() + timedelta(days=15),
        'end_date': datetime.now().date() + timedelta(days=16),
        'start_time': '09:00',
        'end_time': '17:00',
        'capacity': 200,
        'price': 5000,
        'status': 'upcoming',
        'is_featured': False
    }
]

organizer = User.objects.get(username='organizer')
venues = list(Venue.objects.all())
event_types_list = list(EventType.objects.all())

for event_data in events_data:
    event_type = random.choice(event_types_list)
    venue = random.choice(venues)
    
    Event.objects.get_or_create(
        name=event_data['name'],
        defaults={
            **event_data,
            'event_type': event_type,
            'venue': venue,
            'organizer': organizer
        }
    )
print("Events created")

# Create service categories
service_categories = [
    'Catering',
    'Photography',
    'Decoration',
    'Music',
    'Transportation',
    'Makeup Artist',
    'Wedding Planning',
    'Clothing & Attire'
]

for category in service_categories:
    ServiceCategory.objects.get_or_create(name=category)
print("Service categories created")

# Create services
services_data = [
    {
        'name': 'Premium Catering Service',
        'description': 'Delicious South Asian cuisine for your special events.',
        'price': 15000,
        'is_available': True
    },
    {
        'name': 'Professional Photography',
        'description': 'Capture your precious moments with our professional photography service.',
        'price': 20000,
        'is_available': True
    },
    {
        'name': 'Elegant Decoration',
        'description': 'Transform your venue with our elegant decoration service.',
        'price': 25000,
        'is_available': True
    },
    {
        'name': 'Traditional Music Band',
        'description': 'Live traditional music performance for your events.',
        'price': 18000,
        'is_available': True
    }
]

categories = list(ServiceCategory.objects.all())

for service_data in services_data:
    category = random.choice(categories)
    
    Service.objects.get_or_create(
        name=service_data['name'],
        defaults={
            **service_data,
            'category': category,
            'vendor': organizer
        }
    )
print("Services created")

print("Initial data setup completed!")