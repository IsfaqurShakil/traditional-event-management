# venues/admin.py
from django.contrib import admin
from .models import Venue

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'capacity', 'cost_per_day', 'is_available')
    list_filter = ('city', 'is_available')
    search_fields = ('name', 'address', 'city')