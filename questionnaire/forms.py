"""
Django forms for user questionnaire
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegistrationForm(UserCreationForm):
    """User registration form with basic info"""
    
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class DietaryPreferencesForm(forms.ModelForm):
    """Form for dietary preferences and restrictions"""
    
    class Meta:
        model = UserProfile
        fields = [
            'diet', 'budget_sensitivity', 'spice_tolerance',
            'has_nut_allergy', 'has_dairy_allergy', 'has_egg_allergy',
            'has_shellfish_allergy', 'has_soy_allergy', 'has_wheat_allergy'
        ]
        widgets = {
            'diet': forms.RadioSelect(),
            'budget_sensitivity': forms.RadioSelect(),
            'spice_tolerance': forms.RadioSelect(),
        }


class HealthGoalsForm(forms.ModelForm):
    """Form for health goals and preferences"""
    
    class Meta:
        model = UserProfile
        fields = [
            'wants_healthy_options', 'wants_low_calorie', 
            'wants_high_protein', 'wants_organic'
        ]
        widgets = {
            'wants_healthy_options': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'wants_low_calorie': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'wants_high_protein': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'wants_organic': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TimePreferencesForm(forms.ModelForm):
    """Form for meal time preferences"""
    
    class Meta:
        model = UserProfile
        fields = [
            'prefers_morning', 'prefers_lunch', 
            'prefers_afternoon', 'prefers_dinner'
        ]
        widgets = {
            'prefers_morning': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'prefers_lunch': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'prefers_afternoon': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'prefers_dinner': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CuisinePreferencesForm(forms.ModelForm):
    """Form for cuisine preferences"""
    
    class Meta:
        model = UserProfile
        fields = [
            'likes_italian', 'likes_mexican', 'likes_asian',
            'likes_indian', 'likes_american', 'likes_mediterranean'
        ]
        widgets = {
            'likes_italian': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'likes_mexican': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'likes_asian': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'likes_indian': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'likes_american': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'likes_mediterranean': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DislikesForm(forms.ModelForm):
    """Form for food dislikes"""
    
    class Meta:
        model = UserProfile
        fields = [
            'dislikes_spicy', 'dislikes_seafood', 
            'dislikes_mushrooms', 'dislikes_onions'
        ]
        widgets = {
            'dislikes_spicy': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dislikes_seafood': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dislikes_mushrooms': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dislikes_onions': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AdditionalInfoForm(forms.ModelForm):
    """Form for additional information"""
    
    class Meta:
        model = UserProfile
        fields = ['special_occasions']
        widgets = {
            'special_occasions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any special occasions, dietary notes, or preferences...'
            })
        }


class QuickPreferencesForm(forms.Form):
    """Quick preferences form for returning users"""
    
    diet = forms.ChoiceField(
        choices=UserProfile.DIET_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    budget = forms.ChoiceField(
        choices=UserProfile.BUDGET_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    mood = forms.ChoiceField(
        choices=[
            ('casual', 'Casual'),
            ('romantic', 'Romantic'),
            ('quick', 'Quick meal'),
            ('celebration', 'Celebration'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tell us what you\'re in the mood for...'
        })
    )

