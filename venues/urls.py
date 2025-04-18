# venues/urls.py
from django.urls import path
from . import views

app_name = 'venues'  # Add this line

urlpatterns = [
    path('', views.venue_list, name='venue_list'),
    path('<int:pk>/', views.venue_detail, name='venue_detail'),
    path('create/', views.venue_create, name='venue_create'),
    path('<int:pk>/update/', views.venue_update, name='venue_update'),
    path('<int:pk>/delete/', views.venue_delete, name='venue_delete'),
]