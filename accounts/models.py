from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Extended User model with additional fields for roles"""
    USER_ROLES = (
        ('admin', 'Admin'),
        ('organizer', 'Organizer'),
        ('user', 'User'),
    )
    
    role = models.CharField(max_length=10, choices=USER_ROLES, default='user')
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_organizer(self):
        return self.role == 'organizer'
    
    def __str__(self):
        return self.username