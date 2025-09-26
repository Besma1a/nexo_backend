"""
Django views for questionnaire and recommendations
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import time

from .forms import (
    UserRegistrationForm, DietaryPreferencesForm, HealthGoalsForm,
    TimePreferencesForm, CuisinePreferencesForm, DislikesForm,
    AdditionalInfoForm, QuickPreferencesForm
)
from .models import UserProfile, UserFeedback
from ..src.smart_recommender import get_smart_recommender
from ..src.smart_query_processor import get_query_processor
from ..src.contextual import Context


def home(request):
    """Home page with quick access to questionnaire"""
    return render(request, 'questionnaire/home.html')


def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Please complete your preferences.')
            return redirect('questionnaire:dietary_preferences')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'questionnaire/register.html', {'form': form})


@login_required
def dietary_preferences(request):
    """Dietary preferences step"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = DietaryPreferencesForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dietary preferences saved!')
            return redirect('questionnaire:health_goals')
    else:
        form = DietaryPreferencesForm(instance=profile)
    
    return render(request, 'questionnaire/dietary_preferences.html', {'form': form})


@login_required
def health_goals(request):
    """Health goals step"""
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        form = HealthGoalsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Health goals saved!')
            return redirect('questionnaire:time_preferences')
    else:
        form = HealthGoalsForm(instance=profile)
    
    return render(request, 'questionnaire/health_goals.html', {'form': form})


@login_required
def time_preferences(request):
    """Time preferences step"""
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        form = TimePreferencesForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Time preferences saved!')
            return redirect('questionnaire:cuisine_preferences')
    else:
        form = TimePreferencesForm(instance=profile)
    
    return render(request, 'questionnaire/time_preferences.html', {'form': form})


@login_required
def cuisine_preferences(request):
    """Cuisine preferences step"""
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        form = CuisinePreferencesForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuisine preferences saved!')
            return redirect('questionnaire:dislikes')
    else:
        form = CuisinePreferencesForm(instance=profile)
    
    return render(request, 'questionnaire/cuisine_preferences.html', {'form': form})


@login_required
def dislikes(request):
    """Food dislikes step"""
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        form = DislikesForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dislikes saved!')
            return redirect('questionnaire:additional_info')
    else:
        form = DislikesForm(instance=profile)
    
    return render(request, 'questionnaire/dislikes.html', {'form': form})


@login_required
def additional_info(request):
    """Additional information step"""
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        form = AdditionalInfoForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile completed! You can now get personalized recommendations.')
            return redirect('questionnaire:recommendations')
    else:
        form = AdditionalInfoForm(instance=profile)
    
    return render(request, 'questionnaire/additional_info.html', {'form': form})


@login_required
def recommendations(request):
    """Main recommendations page"""
    profile = get_object_or_404(UserProfile, user=request.user)
    
    # Convert profile to recommendation format
    user_preferences = {
        'diet': profile.diet,
        'budget_sensitivity': profile.budget_sensitivity,
        'favorite_categories': profile.get_favorite_categories(),
        'time_preferences': profile.get_time_preferences(),
        'allergies': profile.get_allergies(),
        'dislikes': profile.get_dislikes(),
        'health_goals': []
    }
    
    if profile.wants_healthy_options:
        user_preferences['health_goals'].append('healthy')
    if profile.wants_low_calorie:
        user_preferences['health_goals'].append('low_calorie')
    if profile.wants_high_protein:
        user_preferences['health_goals'].append('high_protein')
    
    # Set user preferences in recommender
    recommender = get_smart_recommender()
    recommender.set_user_preferences(request.user.id, user_preferences)
    
    # Get current context
    context = Context(
        user_id=request.user.id,
        now=timezone.now(),
        budget_level=profile.budget_sensitivity
    )
    
    # Get recommendations
    recommendations = recommender.get_recommendations(
        user_id=request.user.id,
        top_k=10,
        context=context,
        include_explanation=True
    )
    
    return render(request, 'questionnaire/recommendations.html', {
        'recommendations': recommendations['recommendations'],
        'explanation': recommendations.get('explanation', ''),
        'metadata': recommendations['metadata']
    })


@login_required
def quick_recommendations(request):
    """Quick recommendations with form"""
    if request.method == 'POST':
        form = QuickPreferencesForm(request.POST)
        if form.is_valid():
            # Get user profile
            profile = get_object_or_404(UserProfile, user=request.user)
            
            # Update profile with quick preferences
            profile.diet = form.cleaned_data['diet']
            profile.budget_sensitivity = form.cleaned_data['budget']
            profile.save()
            
            # Process query if provided
            query = form.cleaned_data.get('query', '')
            mood = form.cleaned_data.get('mood', 'casual')
            
            # Get recommendations
            recommender = get_smart_recommender()
            context = Context(
                user_id=request.user.id,
                now=timezone.now(),
                budget_level=profile.budget_sensitivity
            )
            
            recommendations = recommender.get_recommendations(
                user_id=request.user.id,
                top_k=8,
                context=context,
                user_query=query,
                include_explanation=True
            )
            
            return render(request, 'questionnaire/quick_recommendations.html', {
                'recommendations': recommendations['recommendations'],
                'explanation': recommendations.get('explanation', ''),
                'query': query,
                'mood': mood
            })
    else:
        form = QuickPreferencesForm()
    
    return render(request, 'questionnaire/quick_form.html', {'form': form})


@csrf_exempt
@login_required
def record_feedback(request):
    """Record user feedback via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            feedback = UserFeedback.objects.create(
                user=request.user,
                item_id=data['item_id'],
                feedback_type=data['feedback_type'],
                value=data['value'],
                metadata=data.get('metadata', {})
            )
            
            # Also record in recommender
            recommender = get_smart_recommender()
            recommender.record_feedback(
                user_id=request.user.id,
                item_id=data['item_id'],
                rating=data['value'],
                feedback_type=data['feedback_type']
            )
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@login_required
def profile(request):
    """User profile page"""
    profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'questionnaire/profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    """Edit user profile"""
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        # Handle different form types based on step
        step = request.POST.get('step', 'dietary')
        
        if step == 'dietary':
            form = DietaryPreferencesForm(request.POST, instance=profile)
        elif step == 'health':
            form = HealthGoalsForm(request.POST, instance=profile)
        elif step == 'time':
            form = TimePreferencesForm(request.POST, instance=profile)
        elif step == 'cuisine':
            form = CuisinePreferencesForm(request.POST, instance=profile)
        elif step == 'dislikes':
            form = DislikesForm(request.POST, instance=profile)
        else:
            form = AdditionalInfoForm(request.POST, instance=profile)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('questionnaire:profile')
    else:
        form = DietaryPreferencesForm(instance=profile)
        step = 'dietary'
    
    return render(request, 'questionnaire/edit_profile.html', {
        'form': form,
        'step': step,
        'profile': profile
    })


def api_recommendations(request):
    """API endpoint for recommendations"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        # Get parameters
        user_id = request.user.id
        top_k = int(request.GET.get('top', 10))
        query = request.GET.get('query', '')
        
        # Get user profile
        profile = get_object_or_404(UserProfile, user=request.user)
        
        # Set up context
        context = Context(
            user_id=user_id,
            now=timezone.now(),
            budget_level=profile.budget_sensitivity
        )
        
        # Get recommendations
        recommender = get_smart_recommender()
        result = recommender.get_recommendations(
            user_id=user_id,
            top_k=top_k,
            context=context,
            user_query=query,
            include_explanation=True
        )
        
        return JsonResponse(result)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

