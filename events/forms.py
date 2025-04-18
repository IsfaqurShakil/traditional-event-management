# events/forms.py
from django import forms
from .models import Event, EventType

class EventForm(forms.ModelForm):
    """Form for creating and updating events"""
    class Meta:
        model = Event
        fields = [
            'name', 'event_type', 'description', 'start_date', 'end_date',
            'start_time', 'end_time', 'venue', 'capacity', 'price', 'image'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class EventSearchForm(forms.Form):
    """Form for searching and filtering events"""
    search = forms.CharField(required=False, label='Search',
                            widget=forms.TextInput(attrs={'placeholder': 'Search events...'}))
    event_type = forms.ModelChoiceField(queryset=EventType.objects.all(), required=False, label='Event Type')
    start_date = forms.DateField(required=False, label='From Date',
                                widget=forms.DateInput(attrs={'type': 'date'}))