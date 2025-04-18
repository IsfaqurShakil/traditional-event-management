# bookings/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from events.models import Event
from .forms import BookingForm

@login_required
def booking_list(request):
    """View for listing user's bookings"""
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'bookings': bookings,
    }
    return render(request, 'bookings/booking_list.html', context)

@login_required
def booking_detail(request, pk):
    """View for booking details"""
    booking = get_object_or_404(Booking, pk=pk)
    
    # Check if user has permission to view the booking
    if not request.user.is_admin() and request.user != booking.user:
        messages.error(request, "You don't have permission to view this booking.")
        return redirect('bookings:booking_list')
    
    context = {
        'booking': booking,
    }
    return render(request, 'bookings/booking_detail.html', context)

@login_required
def booking_create(request):
    """View for creating a new booking"""
    event_id = request.GET.get('event')
    event = None
    
    if event_id:
        event = get_object_or_404(Event, pk=event_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, event=event)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, 'Booking created successfully!')
            return redirect('bookings:booking_detail', pk=booking.pk)
    else:
        form = BookingForm(event=event)
    
    context = {
        'form': form,
        'event': event,
    }
    return render(request, 'bookings/booking_form.html', context)

@login_required
def booking_cancel(request, pk):
    """View for cancelling a booking"""
    booking = get_object_or_404(Booking, pk=pk)
    
    # Check if user has permission to cancel the booking
    if not request.user.is_admin() and request.user != booking.user:
        messages.error(request, "You don't have permission to cancel this booking.")
        return redirect('bookings:booking_list')
    
    # Check if booking can be cancelled
    if booking.status != 'pending':
        messages.error(request, "Only pending bookings can be cancelled.")
        return redirect('bookings:booking_detail', pk=booking.pk)
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully!')
        return redirect('bookings:booking_list')
    
    context = {
        'booking': booking,
    }
    return render(request, 'bookings/booking_cancel.html', context)