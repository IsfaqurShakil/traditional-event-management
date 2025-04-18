from django.db import models
from accounts.models import User
from events.models import Event
from venues.models import Venue
from services.models import Service

class Feedback(models.Model):
    """Model for user feedback"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='feedback', null=True, blank=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='feedback', null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='feedback', null=True, blank=True)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 rating
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        feedback_type = "Event" if self.event else "Venue" if self.venue else "Service"
        return f"{feedback_type} Feedback by {self.user.username} - {self.rating}/5"