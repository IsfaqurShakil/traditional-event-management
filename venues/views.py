# venues/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Venue
from .forms import VenueForm, VenueSearchForm

def venue_list(request):
    """View for listing venues with search and filter functionality"""
    form = VenueSearchForm(request.GET)
    venues = Venue.objects.all().order_by('name')
    
    # Apply search and filters if form is valid
    if form.is_valid():
        search_query = form.cleaned_data.get('search')
        city = form.cleaned_data.get('city')
        min_capacity = form.cleaned_data.get('min_capacity')
        max_cost = form.cleaned_data.get('max_cost')
        
        if search_query:
            venues = venues.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        if city:
            venues = venues.filter(city__icontains=city)
            
        if min_capacity:
            venues = venues.filter(capacity__gte=min_capacity)
            
        if max_cost:
            venues = venues.filter(cost_per_day__lte=max_cost)
    
    context = {
        'venues': venues,
        'form': form,
    }
    return render(request, 'venues/venue_list.html', context)

def venue_detail(request, pk):
    """View for venue details"""
    venue = get_object_or_404(Venue, pk=pk)
    context = {
        'venue': venue,
    }
    return render(request, 'venues/venue_detail.html', context)

@login_required
def venue_create(request):
    """View for creating a new venue"""
    if not request.user.is_admin():
        messages.error(request, "You don't have permission to create venues.")
        return redirect('venues:venue_list')
    
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save()
            messages.success(request, 'Venue created successfully!')
            return redirect('venues:venue_detail', pk=venue.pk)
    else:
        form = VenueForm()
    
    context = {
        'form': form,
        'title': 'Create Venue',
    }
    return render(request, 'venues/venue_form.html', context)

@login_required
def venue_update(request, pk):
    """View for updating a venue"""
    venue = get_object_or_404(Venue, pk=pk)
    
    # Check if user has permission to update the venue
    if not request.user.is_admin():
        messages.error(request, "You don't have permission to update venues.")
        return redirect('venues:venue_detail', pk=venue.pk)
    
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES, instance=venue)
        if form.is_valid():
            form.save()
            messages.success(request, 'Venue updated successfully!')
            return redirect('venues:venue_detail', pk=venue.pk)
    else:
        form = VenueForm(instance=venue)
    
    context = {
        'form': form,
        'title': 'Update Venue',
        'venue': venue,
    }
    return render(request, 'venues/venue_form.html', context)

@login_required
def venue_delete(request, pk):
    """View for deleting a venue"""
    venue = get_object_or_404(Venue, pk=pk)
    
    # Check if user has permission to delete the venue
    if not request.user.is_admin():
        messages.error(request, "You don't have permission to delete venues.")
        return redirect('venues:venue_detail', pk=venue.pk)
    
    if request.method == 'POST':
        venue.delete()
        messages.success(request, 'Venue deleted successfully!')
        return redirect('venues:venue_list')
    
    context = {
        'venue': venue,
    }
    return render(request, 'venues/venue_confirm_delete.html', context)