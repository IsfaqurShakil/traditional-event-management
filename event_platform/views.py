# event_platform/views.py
from django.shortcuts import render
from events.models import Event

def home(request):
    """View for the home page"""
    # Get featured events
    featured_events = Event.objects.filter(is_featured=True, status='upcoming')[:6]
    
    context = {
        'featured_events': featured_events,
    }
    return render(request, 'home.html', context)