 
# feedback/urls.py
from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('add/', views.add_feedback, name='add_feedback'),
]