# event_platform/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/', include('accounts.urls')),
    path('events/', include('events.urls')),  # Make sure this line is uncommented
    # path('venues/', include('venues.urls')),  # Uncomment when ready
    # path('services/', include('services.urls')),  # Uncomment when ready
    # path('bookings/', include('bookings.urls')),  # Uncomment when ready
    # path('payments/', include('payments.urls')),  # Uncomment when ready
    # path('feedback/', include('feedback.urls')),  # Uncomment when ready
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)