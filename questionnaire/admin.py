"""
Django admin configuration for questionnaire app
"""

from django.contrib import admin
from .models import UserProfile, QuestionnaireResponse, UserFeedback


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'diet', 'budget_sensitivity', 'spice_tolerance', 'created_at']
    list_filter = ['diet', 'budget_sensitivity', 'spice_tolerance', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Info', {
            'fields': ('user',)
        }),
        ('Dietary Preferences', {
            'fields': ('diet', 'budget_sensitivity', 'spice_tolerance')
        }),
        ('Allergies', {
            'fields': ('has_nut_allergy', 'has_dairy_allergy', 'has_egg_allergy', 
                      'has_shellfish_allergy', 'has_soy_allergy', 'has_wheat_allergy')
        }),
        ('Health Goals', {
            'fields': ('wants_healthy_options', 'wants_low_calorie', 
                      'wants_high_protein', 'wants_organic')
        }),
        ('Time Preferences', {
            'fields': ('prefers_morning', 'prefers_lunch', 
                      'prefers_afternoon', 'prefers_dinner')
        }),
        ('Cuisine Preferences', {
            'fields': ('likes_italian', 'likes_mexican', 'likes_asian',
                      'likes_indian', 'likes_american', 'likes_mediterranean')
        }),
        ('Dislikes', {
            'fields': ('dislikes_spicy', 'dislikes_seafood', 
                      'dislikes_mushrooms', 'dislikes_onions')
        }),
        ('Additional Info', {
            'fields': ('special_occasions',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(QuestionnaireResponse)
class QuestionnaireResponseAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'answer', 'response_time', 'created_at']
    list_filter = ['created_at', 'response_time']
    search_fields = ['user__username', 'question', 'answer']
    readonly_fields = ['created_at']


@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'item_id', 'feedback_type', 'value', 'created_at']
    list_filter = ['feedback_type', 'created_at']
    search_fields = ['user__username', 'item_id']
    readonly_fields = ['created_at']

