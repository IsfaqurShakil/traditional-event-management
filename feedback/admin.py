# feedback/admin.py
from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_feedback_type', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'comment')
    date_hierarchy = 'created_at'
    
    def get_feedback_type(self, obj):
        if obj.event:
            return f"Event: {obj.event.name}"
        elif obj.venue:
            return f"Venue: {obj.venue.name}"
        elif obj.service:
            return f"Service: {obj.service.name}"
        return "Unknown"
    
    get_feedback_type.short_description = 'Feedback For'