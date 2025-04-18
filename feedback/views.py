# feedback/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Feedback
from .forms import FeedbackForm
from events.models import Event
from venues.models import Venue
from services.models import Service

@login_required
def add_feedback(request):
    """View for adding feedback"""
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            
            # Determine what the feedback is for
            event_id = request.POST.get('event_id')
            venue_id = request.POST.get('venue_id')
            service_id = request.POST.get('service_id')
            
            if event_id:
                event = get_object_or_404(Event, pk=event_id)
                feedback.event = event
                redirect_url = 'events:event_detail'
                redirect_id = event_id
            elif venue_id:
                venue = get_object_or_404(Venue, pk=venue_id)
                feedback.venue = venue
                redirect_url = 'venues:venue_detail'
                redirect_id = venue_id
            elif service_id:
                service = get_object_or_404(Service, pk=service_id)
                feedback.service = service
                redirect_url = 'services:service_detail'
                redirect_id = service_id
            else:
                messages.error(request, "Please specify what you're providing feedback for.")
                return redirect('home')
            
            feedback.save()
            messages.success(request, 'Your feedback has been submitted successfully!')
            return redirect(redirect_url, pk=redirect_id)
    else:
        form = FeedbackForm()
    
    context = {
        'form': form,
    }
    return render(request, 'feedback/feedback_form.html', context)