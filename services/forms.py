# services/forms.py
from django import forms
from .models import Service, ServiceBooking
import uuid

class ServiceForm(forms.ModelForm):
    """Form for creating and updating services"""
    class Meta:
        model = Service
        fields = [
            'name', 'category', 'description', 'price',
            'image', 'is_available'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ServiceBookingForm(forms.ModelForm):
    """Form for booking services"""
    class Meta:
        model = ServiceBooking
        fields = ['booking_date', 'notes']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Generate a unique booking reference
        if not instance.booking_reference:
            instance.booking_reference = f"SB-{uuid.uuid4().hex[:8].upper()}"
        
        # Calculate total amount based on service price
        instance.total_amount = instance.service.price
        
        if commit:
            instance.save()
        
        return instance