from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Registration

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'location', 'organizer', 'created_at']

class RegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event_details = EventSerializer(source='event', read_only=True)

    class Meta:
        model = Registration
        fields = ['id', 'user', 'event', 'event_details', 'registration_date', 'status']
