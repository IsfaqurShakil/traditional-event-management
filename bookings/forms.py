# bookings/forms.py
from django import forms
from .models import Booking
import uuid

class BookingForm(forms.ModelForm):
    """Form for creating and updating bookings"""
    class Meta:
        model = Booking
        fields = [
            'venue', 'booking_date', 'start_time', 'end_time',
            'num_guests', 'notes'
        ]
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        super().__init__(*args, **kwargs)
        
        if self.event:
            self.fields['venue'].initial = self.event.venue
            self.fields['venue'].widget.attrs['readonly'] = True
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.event:
            instance.event = self.event
        
        # Generate a unique booking reference
        if not instance.booking_reference:
            instance.booking_reference = f"BK-{uuid.uuid4().hex[:8].upper()}"
        
        # Calculate total amount based on venue cost or event price
        if instance.event:
            instance.total_amount = instance.event.price * instance.num_guests
        else:
            instance.total_amount = instance.venue.cost_per_day
        
        if commit:
            instance.save()
        
        return instance