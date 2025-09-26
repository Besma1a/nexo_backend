"""
Django models for user questionnaire and preferences
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(models.Model):
    """Extended user profile with dietary preferences and restrictions"""
    
    DIET_CHOICES = [
        ('none', 'No restrictions'),
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('keto', 'Keto'),
        ('paleo', 'Paleo'),
        ('halal', 'Halal'),
        ('kosher', 'Kosher'),
        ('gluten_free', 'Gluten Free'),
    ]
    
    BUDGET_CHOICES = [
        ('low', 'Budget-friendly ($5-15)'),
        ('mid', 'Moderate ($15-30)'),
        ('high', 'Premium ($30+)'),
    ]
    
    SPICE_LEVEL_CHOICES = [
        ('mild', 'Mild'),
        ('medium', 'Medium'),
        ('hot', 'Hot'),
        ('very_hot', 'Very Hot'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Basic preferences
    diet = models.CharField(max_length=20, choices=DIET_CHOICES, default='none')
    budget_sensitivity = models.CharField(max_length=10, choices=BUDGET_CHOICES, default='mid')
    spice_tolerance = models.CharField(max_length=10, choices=SPICE_LEVEL_CHOICES, default='medium')
    
    # Allergies and restrictions
    has_nut_allergy = models.BooleanField(default=False)
    has_dairy_allergy = models.BooleanField(default=False)
    has_egg_allergy = models.BooleanField(default=False)
    has_shellfish_allergy = models.BooleanField(default=False)
    has_soy_allergy = models.BooleanField(default=False)
    has_wheat_allergy = models.BooleanField(default=False)
    
    # Health goals
    wants_healthy_options = models.BooleanField(default=False)
    wants_low_calorie = models.BooleanField(default=False)
    wants_high_protein = models.BooleanField(default=False)
    wants_organic = models.BooleanField(default=False)
    
    # Time preferences
    prefers_morning = models.BooleanField(default=False)
    prefers_lunch = models.BooleanField(default=False)
    prefers_afternoon = models.BooleanField(default=False)
    prefers_dinner = models.BooleanField(default=False)
    
    # Cuisine preferences
    likes_italian = models.BooleanField(default=False)
    likes_mexican = models.BooleanField(default=False)
    likes_asian = models.BooleanField(default=False)
    likes_indian = models.BooleanField(default=False)
    likes_american = models.BooleanField(default=False)
    likes_mediterranean = models.BooleanField(default=False)
    
    # Dislikes
    dislikes_spicy = models.BooleanField(default=False)
    dislikes_seafood = models.BooleanField(default=False)
    dislikes_mushrooms = models.BooleanField(default=False)
    dislikes_onions = models.BooleanField(default=False)
    
    # Additional info
    special_occasions = models.TextField(blank=True, help_text="Any special occasions or notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_allergies(self):
        """Get list of allergies"""
        allergies = []
        if self.has_nut_allergy:
            allergies.append('nuts')
        if self.has_dairy_allergy:
            allergies.append('dairy')
        if self.has_egg_allergy:
            allergies.append('eggs')
        if self.has_shellfish_allergy:
            allergies.append('shellfish')
        if self.has_soy_allergy:
            allergies.append('soy')
        if self.has_wheat_allergy:
            allergies.append('wheat')
        return allergies
    
    def get_favorite_categories(self):
        """Get list of favorite cuisine categories"""
        categories = []
        if self.likes_italian:
            categories.append('italian')
        if self.likes_mexican:
            categories.append('mexican')
        if self.likes_asian:
            categories.append('asian')
        if self.likes_indian:
            categories.append('indian')
        if self.likes_american:
            categories.append('american')
        if self.likes_mediterranean:
            categories.append('mediterranean')
        return categories
    
    def get_time_preferences(self):
        """Get list of preferred meal times"""
        times = []
        if self.prefers_morning:
            times.append('morning')
        if self.prefers_lunch:
            times.append('lunch')
        if self.prefers_afternoon:
            times.append('afternoon')
        if self.prefers_dinner:
            times.append('dinner')
        return times
    
    def get_dislikes(self):
        """Get list of disliked ingredients"""
        dislikes = []
        if self.dislikes_spicy:
            dislikes.append('spicy')
        if self.dislikes_seafood:
            dislikes.append('seafood')
        if self.dislikes_mushrooms:
            dislikes.append('mushrooms')
        if self.dislikes_onions:
            dislikes.append('onions')
        return dislikes


class QuestionnaireResponse(models.Model):
    """Store questionnaire responses for analytics"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questionnaire_responses')
    question = models.CharField(max_length=200)
    answer = models.TextField()
    response_time = models.FloatField(help_text="Time taken to answer in seconds")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.question[:50]}"


class UserFeedback(models.Model):
    """Store user feedback on recommendations"""
    
    FEEDBACK_TYPES = [
        ('rating', 'Rating'),
        ('click', 'Click'),
        ('purchase', 'Purchase'),
        ('skip', 'Skip'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback')
    item_id = models.IntegerField()
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    value = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.feedback_type} - Item {self.item_id}"

