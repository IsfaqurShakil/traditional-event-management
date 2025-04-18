# services/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Service, ServiceCategory, ServiceBooking
from .forms import ServiceForm, ServiceBookingForm

def service_list(request):
    """View for listing services"""
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    
    services = Service.objects.filter(is_available=True).order_by('name')
    categories = ServiceCategory.objects.all()
    
    if search_query:
        services = services.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if category_id:
        services = services.filter(category_id=category_id)
    
    context = {
        'services': services,
        'categories': categories,
        'search_query': search_query,
        'category_id': category_id,
    }
    return render(request, 'services/service_list.html', context)

def service_detail(request, pk):
    """View for service details"""
    service = get_object_or_404(Service, pk=pk)
    
    # Get related services (same category)
    related_services = Service.objects.filter(category=service.category, is_available=True).exclude(pk=service.pk)[:3]
    
    context = {
        'service': service,
        'related_services': related_services,
    }
    return render(request, 'services/service_detail.html', context)

@login_required
def service_create(request):
    """View for creating a new service"""
    if not request.user.is_organizer() and not request.user.is_admin():
        messages.error(request, "You don't have permission to create services.")
        return redirect('services:service_list')
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.vendor = request.user
            service.save()
            messages.success(request, 'Service created successfully!')
            return redirect('services:service_detail', pk=service.pk)
    else:
        form = ServiceForm()
    
    context = {
        'form': form,
        'title': 'Create Service',
    }
    return render(request, 'services/service_form.html', context)

@login_required
def service_update(request, pk):
    """View for updating a service"""
    service = get_object_or_404(Service, pk=pk)
    
    # Check if user has permission to update the service
    if not request.user.is_admin() and request.user != service.vendor:
        messages.error(request, "You don't have permission to update this service.")
        return redirect('services:service_detail', pk=service.pk)
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully!')
            return redirect('services:service_detail', pk=service.pk)
    else:
        form = ServiceForm(instance=service)
    
    context = {
        'form': form,
        'title': 'Update Service',
        'service': service,
    }
    return render(request, 'services/service_form.html', context)

@login_required
def service_delete(request, pk):
    """View for deleting a service"""
    service = get_object_or_404(Service, pk=pk)
    
    # Check if user has permission to delete the service
    if not request.user.is_admin() and request.user != service.vendor:
        messages.error(request, "You don't have permission to delete this service.")
        return redirect('services:service_detail', pk=service.pk)
    
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted successfully!')
        return redirect('services:service_list')
    
    context = {
        'service': service,
    }
    return render(request, 'services/service_confirm_delete.html', context)

@login_required
def service_booking(request, pk):
    """View for booking a service"""
    service = get_object_or_404(Service, pk=pk)
    
    if not service.is_available:
        messages.error(request, "This service is not available for booking.")
        return redirect('services:service_detail', pk=service.pk)
    
    if request.method == 'POST':
        form = ServiceBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service = service
            booking.save()
            messages.success(request, 'Service booked successfully!')
            return redirect('services:booking_detail', pk=booking.pk)
    else:
        form = ServiceBookingForm()
    
    context = {
        'form': form,
        'service': service,
    }
    return render(request, 'services/service_booking_form.html', context)

@login_required
def booking_detail(request, pk):
    """View for service booking details"""
    booking = get_object_or_404(ServiceBooking, pk=pk)
    
    # Check if user has permission to view the booking
    if not request.user.is_admin() and request.user != booking.user and request.user != booking.service.vendor:
        messages.error(request, "You don't have permission to view this booking.")
        return redirect('services:service_list')
    
    context = {
        'booking': booking,
    }
    return render(request, 'services/booking_detail.html', context)

@login_required
def booking_cancel(request, pk):
    """View for cancelling a service booking"""
    booking = get_object_or_404(ServiceBooking, pk=pk)
    
    # Check if user has permission to cancel the booking
    if not request.user.is_admin() and request.user != booking.user:
        messages.error(request, "You don't have permission to cancel this booking.")
        return redirect('services:booking_detail', pk=booking.pk)
    
    # Check if booking can be cancelled
    if booking.status != 'pending':
        messages.error(request, "Only pending bookings can be cancelled.")
        return redirect('services:booking_detail', pk=booking.pk)
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully!')
        return redirect('dashboard')
    
    context = {
        'booking': booking,
    }
    return render(request, 'services/booking_cancel.html', context)