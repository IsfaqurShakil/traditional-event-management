# venues/forms.py
from django import forms
from .models import Venue

class VenueForm(forms.ModelForm):
    """Form for creating and updating venues"""
    class Meta:
        model = Venue
        fields = [
            'name', 'address', 'city', 'capacity', 'cost_per_day',
            'contact_person', 'contact_phone', 'contact_email',
            'description', 'image', 'is_available'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class VenueSearchForm(forms.Form):
    """Form for searching and filtering venues"""
    search = forms.CharField(required=False, label='Search',
                            widget=forms.TextInput(attrs={'placeholder': 'Search venues...'}))
    city = forms.CharField(required=False, label='City')
    min_capacity = forms.IntegerField(required=False, label='Min Capacity')
    max_cost = forms.DecimalField(required=False, label='Max Cost per Day')