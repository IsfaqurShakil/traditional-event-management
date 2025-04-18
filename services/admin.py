# services/admin.py
from django.contrib import admin
from .models import Service, ServiceCategory, ServiceBooking

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'vendor', 'price', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description', 'vendor__username')

@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'user', 'service', 'booking_date', 'status', 'total_amount')
    list_filter = ('status', 'booking_date')
    search_fields = ('booking_reference', 'user__username', 'service__name')
    date_hierarchy = 'booking_date'

admin.site.register(ServiceCategory)