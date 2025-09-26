"""
Smart Menu Recommender - Hackathon Edition
Streamlined but impressive recommendation system for medium restaurants
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)

from .hybrid import recommend as base_recommend
from .contextual import Context
from .utils import print_df, season_of


class SmartRecommender:
    """Smart recommendation system with impressive but realistic features"""
    
    def __init__(self):
        self.user_preferences = {}  # Cache user preferences
        self.recommendation_cache = {}  # Simple in-memory cache
        self.feedback_data = []  # Store user feedback
        self.impression_count = 0
        
    def get_recommendations(self, user_id: int, top_k: int = 10, 
                          context: Context = None, user_query: str = None,
                          include_explanation: bool = False) -> Dict[str, Any]:
        """Get smart recommendations with impressive features"""
        
        start_time = datetime.now()
        
        # Check cache first
        cache_key = f"{user_id}_{context.time_of_day if context else 'default'}_{context.budget_level if context else 'default'}"
        if cache_key in self.recommendation_cache:
            cached_result = self.recommendation_cache[cache_key]
            cached_result['metadata']['from_cache'] = True
            cached_result['metadata']['processing_time_seconds'] = 0.001
            return cached_result
        
        # Generate context if not provided
        if not context:
            context = Context(user_id=user_id, now=datetime.now()).ensure()
        
        # Process user query for smart filtering
        search_filters = self._process_user_query(user_query) if user_query else {}
        
        # Get base recommendations
        base_recs = base_recommend(user_id, top_k * 2, context)
        
        if base_recs.empty:
            return self._format_response(pd.DataFrame(), context, False, 0.001)
        
        # Apply smart filters
        filtered_recs = self._apply_smart_filters(base_recs, search_filters)
        
        # Apply personalization boost
        personalized_recs = self._apply_personalization_boost(filtered_recs, user_id)
        
        # Apply diversity enhancement
        diverse_recs = self._apply_diversity_enhancement(personalized_recs, top_k)
        
        # Add smart scoring
        smart_recs = self._add_smart_scoring(diverse_recs, context)
        
        # Sort and get top-k
        final_recs = smart_recs.sort_values('smart_score', ascending=False).head(top_k)
        
        # Cache results
        processing_time = (datetime.now() - start_time).total_seconds()
        result = self._format_response(final_recs, context, include_explanation, processing_time)
        self.recommendation_cache[cache_key] = result.copy()
        
        # Track impressions
        self.impression_count += 1
        
        return result
    
    def _process_user_query(self, query: str) -> Dict[str, Any]:
        """Process natural language query for smart filtering"""
        if not query:
            return {}
        
        query_lower = query.lower()
        filters = {}
        
        # Extract dietary preferences
        if any(word in query_lower for word in ['vegetarian', 'veggie']):
            filters['dietary'] = 'vegetarian'
        elif any(word in query_lower for word in ['vegan']):
            filters['dietary'] = 'vegan'
        elif any(word in query_lower for word in ['gluten free', 'gluten-free']):
            filters['dietary'] = 'gluten_free'
        
        # Extract price preferences
        if any(word in query_lower for word in ['cheap', 'affordable', 'budget']):
            filters['price'] = 'low'
        elif any(word in query_lower for word in ['expensive', 'premium', 'luxury']):
            filters['price'] = 'high'
        
        # Extract health preferences
        if any(word in query_lower for word in ['healthy', 'light', 'fresh']):
            filters['health'] = 'healthy'
        elif any(word in query_lower for word in ['comfort', 'indulgent', 'rich']):
            filters['health'] = 'comfort'
        
        # Extract mood/occasion
        if any(word in query_lower for word in ['romantic', 'date', 'anniversary']):
            filters['mood'] = 'romantic'
        elif any(word in query_lower for word in ['quick', 'fast', 'grab']):
            filters['mood'] = 'quick'
        elif any(word in query_lower for word in ['celebration', 'party', 'birthday']):
            filters['mood'] = 'celebration'
        
        return filters
    
    def _apply_smart_filters(self, recommendations: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """Apply smart filters based on user query"""
        if not filters:
            return recommendations
        
        filtered = recommendations.copy()
        
        # Dietary filters
        if 'dietary' in filters:
            dietary = filters['dietary']
            if dietary == 'vegetarian':
                filtered = filtered[~filtered['dietary_tags'].apply(
                    lambda x: 'meat' in x if isinstance(x, list) else False
                )]
            elif dietary == 'vegan':
                filtered = filtered[~filtered['dietary_tags'].apply(
                    lambda x: any(tag in ['meat', 'dairy', 'cheese'] for tag in x) if isinstance(x, list) else False
                )]
            elif dietary == 'gluten_free':
                filtered = filtered[~filtered['dietary_tags'].apply(
                    lambda x: 'gluten' in x if isinstance(x, list) else False
                )]
        
        # Price filters
        if 'price' in filters:
            price = filters['price']
            if price == 'low':
                filtered = filtered[filtered['budget_category'] == 'low']
            elif price == 'high':
                filtered = filtered[filtered['budget_category'] == 'high']
        
        # Health filters (based on category and name)
        if 'health' in filters:
            health = filters['health']
            if health == 'healthy':
                healthy_categories = ['salad', 'soup', 'juice', 'smoothie']
                filtered = filtered[filtered['category'].isin(healthy_categories)]
            elif health == 'comfort':
                comfort_categories = ['pizza', 'burger', 'pasta', 'dessert']
                filtered = filtered[filtered['category'].isin(comfort_categories)]
        
        return filtered
    
    def _apply_personalization_boost(self, recommendations: pd.DataFrame, user_id: int) -> pd.DataFrame:
        """Apply personalization based on user preferences and feedback"""
        if user_id not in self.user_preferences:
            return recommendations
        
        user_prefs = self.user_preferences[user_id]
        boosted = recommendations.copy()
        
        # Boost based on favorite categories
        if 'favorite_categories' in user_prefs:
            for category in user_prefs['favorite_categories']:
                mask = boosted['category'] == category
                boosted.loc[mask, 'score'] *= 1.2
        
        # Boost based on dietary preferences
        if 'diet' in user_prefs:
            diet = user_prefs['diet']
            if diet == 'vegetarian':
                mask = boosted['dietary_tags'].apply(
                    lambda x: 'vegetarian' in x if isinstance(x, list) else False
                )
                boosted.loc[mask, 'score'] *= 1.15
            elif diet == 'vegan':
                mask = boosted['dietary_tags'].apply(
                    lambda x: 'vegan' in x if isinstance(x, list) else False
                )
                boosted.loc[mask, 'score'] *= 1.15
        
        # Boost based on time preferences
        if 'time_preferences' in user_prefs:
            current_time = datetime.now().hour
            if 6 <= current_time < 11:  # Morning
                time_pref = 'morning'
            elif 11 <= current_time < 15:  # Lunch
                time_pref = 'lunch'
            elif 15 <= current_time < 18:  # Afternoon
                time_pref = 'afternoon'
            else:  # Evening
                time_pref = 'dinner'
            
            if time_pref in user_prefs['time_preferences']:
                mask = boosted['time_preference'].fillna('any').isin([time_pref, 'any', 'all'])
                boosted.loc[mask, 'score'] *= 1.1
        
        return boosted
    
    def _apply_diversity_enhancement(self, recommendations: pd.DataFrame, top_k: int) -> pd.DataFrame:
        """Apply diversity enhancement to ensure variety"""
        if recommendations.empty:
            return recommendations
        
        diversified = []
        category_counts = {}
        max_per_category = max(1, top_k // 3)  # Max 1/3 of recommendations per category
        
        for _, row in recommendations.iterrows():
            category = row.get('category', 'unknown')
            count = category_counts.get(category, 0)
            
            if count < max_per_category:
                diversified.append(row)
                category_counts[category] = count + 1
            elif len(diversified) < top_k:  # Allow some overflow
                diversified.append(row)
        
        return pd.DataFrame(diversified) if diversified else recommendations.head(top_k)
    
    def _add_smart_scoring(self, recommendations: pd.DataFrame, context: Context) -> pd.DataFrame:
        """Add smart scoring based on multiple factors"""
        if recommendations.empty:
            return recommendations
        
        scored = recommendations.copy()
        
        # Base score from original algorithm
        scored['smart_score'] = scored['score'].fillna(0.5)
        
        # Time-based boost
        time_boost = scored['time_preference'].fillna('any').apply(
            lambda t: 1.2 if t == context.time_of_day else (1.05 if t in ['any', 'all'] else 1.0)
        )
        scored['smart_score'] *= time_boost
        
        # Seasonality boost
        current_season = season_of(context.now)
        if 'seasonal' in scored.columns:
            season_boost = scored['seasonal'].fillna('all').apply(
                lambda s: 1.15 if s == current_season or s in ['all', 'any'] else 1.0
            )
            scored['smart_score'] *= season_boost
        
        # Price alignment boost
        budget = context.budget_level or 'mid'
        price_boost = scored['budget_category'].fillna('mid').apply(
            lambda p: 1.2 if p == budget else (1.0 if p == 'mid' else 0.9)
        )
        scored['smart_score'] *= price_boost
        
        # Popularity boost (if available)
        if 'popularity_score' in scored.columns:
            pop_boost = scored['popularity_score'].fillna(0.5) * 0.1 + 1.0
            scored['smart_score'] *= pop_boost
        
        return scored
    
    def _format_response(self, recommendations: pd.DataFrame, context: Context,
                        include_explanation: bool, processing_time: float) -> Dict[str, Any]:
        """Format response with metadata and explanation"""
        
        response = {
            'recommendations': recommendations.to_dict(orient='records'),
            'metadata': {
                'user_id': context.user_id,
                'time_of_day': context.time_of_day,
                'budget_level': context.budget_level,
                'total_recommendations': len(recommendations),
                'from_cache': False,
                'processing_time_seconds': processing_time,
                'timestamp': datetime.now().isoformat(),
                'system_version': '2.0.0'
            }
        }
        
        # Add explanation if requested
        if include_explanation and not recommendations.empty:
            top_item = recommendations.iloc[0]
            explanation = self._generate_explanation(top_item, context)
            response['explanation'] = explanation
        
        return response
    
    def _generate_explanation(self, item: pd.Series, context: Context) -> str:
        """Generate smart explanation for recommendation"""
        explanations = []
        
        # Time-based explanation
        if item.get('time_preference') == context.time_of_day:
            explanations.append(f"perfect for {context.time_of_day}")
        elif item.get('time_preference') in ['any', 'all']:
            explanations.append(f"great for {context.time_of_day}")
        
        # Budget explanation
        if item.get('budget_category') == context.budget_level:
            explanations.append(f"fits your {context.budget_level} budget")
        
        # Category explanation
        if item.get('category'):
            explanations.append(f"from our popular {item['category']} selection")
        
        # Dietary explanation
        if item.get('dietary_tags') and isinstance(item['dietary_tags'], list):
            if 'vegetarian' in item['dietary_tags']:
                explanations.append("vegetarian-friendly")
            if 'vegan' in item['dietary_tags']:
                explanations.append("vegan option")
        
        if explanations:
            return f"I recommend {item['name']} because it's {' and '.join(explanations)}!"
        else:
            return f"I recommend {item['name']} - it's a great choice from our menu!"
    
    def set_user_preferences(self, user_id: int, preferences: Dict[str, Any]):
        """Set user preferences for personalization"""
        self.user_preferences[user_id] = preferences
        logger.info(f"Updated preferences for user {user_id}")
    
    def record_feedback(self, user_id: int, item_id: int, rating: float, feedback_type: str = 'rating'):
        """Record user feedback for learning"""
        feedback = {
            'user_id': user_id,
            'item_id': item_id,
            'rating': rating,
            'feedback_type': feedback_type,
            'timestamp': datetime.now()
        }
        self.feedback_data.append(feedback)
        logger.info(f"Recorded {feedback_type} feedback for user {user_id}, item {item_id}")
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        return {
            'total_impressions': self.impression_count,
            'cached_recommendations': len(self.recommendation_cache),
            'users_with_preferences': len(self.user_preferences),
            'total_feedback': len(self.feedback_data),
            'system_version': '2.0.0'
        }


# Global instance
_smart_recommender = None

def get_smart_recommender() -> SmartRecommender:
    """Get global smart recommender instance"""
    global _smart_recommender
    if _smart_recommender is None:
        _smart_recommender = SmartRecommender()
    return _smart_recommender

