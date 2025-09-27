"""
URL configuration for questionnaire app
"""

from django.urls import path
from . import views

app_name = 'questionnaire'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dietary-preferences/', views.dietary_preferences, name='dietary_preferences'),
    path('health-goals/', views.health_goals, name='health_goals'),
    path('time-preferences/', views.time_preferences, name='time_preferences'),
    path('cuisine-preferences/', views.cuisine_preferences, name='cuisine_preferences'),
    path('dislikes/', views.dislikes, name='dislikes'),
    path('additional-info/', views.additional_info, name='additional_info'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('quick/', views.quick_recommendations, name='quick_recommendations'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('api/recommendations/', views.api_recommendations, name='api_recommendations'),
    path('api/feedback/', views.record_feedback, name='record_feedback'),
]

