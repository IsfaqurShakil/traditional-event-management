# events/admin.py
from django.contrib import admin
from .models import Event, EventType

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'start_date', 'venue', 'organizer', 'status', 'is_featured')
    list_filter = ('status', 'event_type', 'is_featured')
    search_fields = ('name', 'description')
    date_hierarchy = 'start_date'

admin.site.register(EventType)