# events/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Event, EventType
from .forms import EventForm, EventSearchForm
from django.http import HttpResponse
from django.shortcuts import render

def event_list(request):
    """View for listing events with search and filter functionality"""
    form = EventSearchForm(request.GET)
    events = Event.objects.all().order_by('start_date')
    
    # Apply search and filters if form is valid
    if form.is_valid():
        search_query = form.cleaned_data.get('search')
        event_type = form.cleaned_data.get('event_type')
        start_date = form.cleaned_data.get('start_date')
        
        if search_query:
            events = events.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        if event_type:
            events = events.filter(event_type=event_type)
            
        if start_date:
            events = events.filter(start_date__gte=start_date)
    
    context = {
        'events': events,
        'form': form,
    }
    return render(request, 'events/event_list.html', context)

def event_detail(request, pk):
    """View for event details"""
    event = get_object_or_404(Event, pk=pk)
    
    # Get related events (same event type)
    related_events = Event.objects.filter(event_type=event.event_type).exclude(pk=event.pk)[:3]
    
    context = {
        'event': event,
        'related_events': related_events,
    }
    return render(request, 'events/event_detail.html', context)

@login_required
def event_create(request):
    """View for creating a new event"""
    if not request.user.is_organizer() and not request.user.is_admin():
        messages.error(request, "You don't have permission to create events.")
        return redirect('events:event_list')
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('events:event_detail', pk=event.pk)
    else:
        form = EventForm()
    
    context = {
        'form': form,
        'title': 'Create Event',
    }
    return render(request, 'events/event_form.html', context)

@login_required
def event_update(request, pk):
    """View for updating an event"""
    event = get_object_or_404(Event, pk=pk)
    
    # Check if user has permission to update the event
    if not request.user.is_admin() and request.user != event.organizer:
        messages.error(request, "You don't have permission to update this event.")
        return redirect('events:event_detail', pk=event.pk)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('events:event_detail',  'Event updated successfully!')
            return redirect('events:event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    
    context = {
        'form': form,
        'title': 'Update Event',
        'event': event,
    }
    return render(request, 'events/event_form.html', context)

@login_required
def event_delete(request, pk):
    """View for deleting an event"""
    event = get_object_or_404(Event, pk=pk)
    
    # Check if user has permission to delete the event
    if not request.user.is_admin() and request.user != event.organizer:
        messages.error(request, "You don't have permission to delete this event.")
        return redirect('events:event_detail', pk=event.pk)
    
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('events:event_list')
    
    context = {
        'event': event,
    }
    return render(request, 'events/event_confirm_delete.html', context)