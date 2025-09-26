"""
Smart Query Processor - Hackathon Edition
Intelligent natural language processing for restaurant recommendations
"""

import re
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from .contextual import Context


class SmartQueryProcessor:
    """Smart query processing with impressive but realistic features"""
    
    def __init__(self):
        # Predefined patterns for common queries
        self.patterns = {
            'dietary': {
                'vegetarian': ['vegetarian', 'veggie', 'plant-based', 'no meat'],
                'vegan': ['vegan', 'no dairy', 'no eggs', 'plant only'],
                'gluten_free': ['gluten free', 'gluten-free', 'no gluten', 'celiac'],
                'keto': ['keto', 'ketogenic', 'low carb', 'no carbs'],
                'halal': ['halal', 'islamic', 'muslim'],
                'kosher': ['kosher', 'jewish']
            },
            'price': {
                'low': ['cheap', 'affordable', 'budget', 'inexpensive', 'under 10', 'under $10'],
                'high': ['expensive', 'premium', 'luxury', 'upscale', 'fine dining', 'over 20', 'over $20'],
                'mid': ['moderate', 'mid-range', 'reasonable', 'average price']
            },
            'health': {
                'healthy': ['healthy', 'light', 'fresh', 'nutritious', 'low calorie', 'diet'],
                'comfort': ['comfort', 'indulgent', 'rich', 'hearty', 'filling', 'decadent'],
                'low_calorie': ['low calorie', 'light', 'diet', 'weight loss'],
                'protein_rich': ['protein', 'high protein', 'muscle', 'fitness']
            },
            'mood': {
                'romantic': ['romantic', 'date', 'anniversary', 'valentine', 'couple'],
                'quick': ['quick', 'fast', 'grab', 'on the go', 'rush', 'hurry'],
                'celebration': ['celebration', 'party', 'birthday', 'special', 'festive'],
                'casual': ['casual', 'relaxed', 'informal', 'chill'],
                'business': ['business', 'meeting', 'professional', 'formal']
            },
            'cuisine': {
                'italian': ['italian', 'pasta', 'pizza', 'risotto', 'tiramisu'],
                'mexican': ['mexican', 'taco', 'burrito', 'salsa', 'guacamole'],
                'asian': ['asian', 'chinese', 'japanese', 'thai', 'sushi', 'ramen'],
                'indian': ['indian', 'curry', 'spicy', 'tandoor', 'naan'],
                'american': ['american', 'burger', 'fries', 'steak', 'bbq'],
                'mediterranean': ['mediterranean', 'greek', 'olive', 'hummus', 'falafel']
            },
            'allergies': {
                'nuts': ['nuts', 'peanuts', 'almonds', 'walnuts', 'nut allergy'],
                'dairy': ['dairy', 'milk', 'cheese', 'lactose', 'dairy allergy'],
                'eggs': ['eggs', 'egg allergy'],
                'shellfish': ['shellfish', 'shrimp', 'crab', 'lobster', 'seafood allergy'],
                'soy': ['soy', 'soybean', 'soy allergy'],
                'wheat': ['wheat', 'gluten', 'wheat allergy']
            }
        }
    
    def process_query(self, query: str, user_id: int, current_time: datetime = None) -> Dict[str, Any]:
        """Process natural language query and return structured parameters"""
        if not query:
            return {'intent': 'browse', 'filters': {}, 'confidence': 0.0}
        
        current_time = current_time or datetime.now()
        base_context = Context(user_id=user_id, now=current_time)
        
        # Extract information from query
        extracted_info = self._extract_information(query)
        
        # Determine intent
        intent = self._determine_intent(query, extracted_info)
        
        # Build search filters
        filters = self._build_filters(extracted_info)
        
        # Calculate confidence
        confidence = self._calculate_confidence(extracted_info)
        
        return {
            'user_id': user_id,
            'original_query': query,
            'intent': intent,
            'filters': filters,
            'confidence': confidence,
            'context': base_context,
            'extracted_info': extracted_info
        }
    
    def _extract_information(self, query: str) -> Dict[str, Any]:
        """Extract structured information from query"""
        query_lower = query.lower()
        extracted = {
            'dietary_requirements': [],
            'price_preference': None,
            'health_goals': [],
            'mood': None,
            'cuisine_preference': [],
            'allergies': [],
            'keywords': []
        }
        
        # Extract dietary requirements
        for diet, patterns in self.patterns['dietary'].items():
            if any(pattern in query_lower for pattern in patterns):
                extracted['dietary_requirements'].append(diet)
        
        # Extract price preference
        for price, patterns in self.patterns['price'].items():
            if any(pattern in query_lower for pattern in patterns):
                extracted['price_preference'] = price
                break
        
        # Extract health goals
        for health, patterns in self.patterns['health'].items():
            if any(pattern in query_lower for pattern in patterns):
                extracted['health_goals'].append(health)
        
        # Extract mood
        for mood, patterns in self.patterns['mood'].items():
            if any(pattern in query_lower for pattern in patterns):
                extracted['mood'] = mood
                break
        
        # Extract cuisine preferences
        for cuisine, patterns in self.patterns['cuisine'].items():
            if any(pattern in query_lower for pattern in patterns):
                extracted['cuisine_preference'].append(cuisine)
        
        # Extract allergies
        for allergy, patterns in self.patterns['allergies'].items():
            if any(pattern in query_lower for pattern in patterns):
                extracted['allergies'].append(allergy)
        
        # Extract general keywords
        words = re.findall(r'\b\w+\b', query_lower)
        extracted['keywords'] = [word for word in words if len(word) > 3]
        
        return extracted
    
    def _determine_intent(self, query: str, extracted_info: Dict[str, Any]) -> str:
        """Determine user intent from query"""
        query_lower = query.lower()
        
        # Intent patterns
        if any(word in query_lower for word in ['find', 'search', 'looking for', 'show me']):
            return 'search'
        elif any(word in query_lower for word in ['recommend', 'suggest', 'what should']):
            return 'recommendation'
        elif any(word in query_lower for word in ['best', 'top', 'popular', 'favorite']):
            return 'discovery'
        elif any(word in query_lower for word in ['new', 'latest', 'recent']):
            return 'exploration'
        elif any(word in query_lower for word in ['similar to', 'like', 'alternative']):
            return 'similarity'
        elif extracted_info['dietary_requirements'] or extracted_info['allergies']:
            return 'dietary_restriction'
        elif extracted_info['price_preference']:
            return 'price_sensitive'
        elif extracted_info['mood']:
            return 'mood_based'
        else:
            return 'browse'
    
    def _build_filters(self, extracted_info: Dict[str, Any]) -> Dict[str, Any]:
        """Build search filters from extracted information"""
        filters = {}
        
        if extracted_info['dietary_requirements']:
            filters['dietary'] = extracted_info['dietary_requirements'][0]  # Take first match
        
        if extracted_info['price_preference']:
            filters['price'] = extracted_info['price_preference']
        
        if extracted_info['health_goals']:
            filters['health'] = extracted_info['health_goals'][0]
        
        if extracted_info['mood']:
            filters['mood'] = extracted_info['mood']
        
        if extracted_info['cuisine_preference']:
            filters['cuisine'] = extracted_info['cuisine_preference'][0]
        
        if extracted_info['allergies']:
            filters['allergies'] = extracted_info['allergies']
        
        return filters
    
    def _calculate_confidence(self, extracted_info: Dict[str, Any]) -> float:
        """Calculate confidence score for extraction"""
        total_fields = 6  # dietary, price, health, mood, cuisine, allergies
        filled_fields = sum(1 for field in [
            extracted_info['dietary_requirements'],
            [extracted_info['price_preference']] if extracted_info['price_preference'] else [],
            extracted_info['health_goals'],
            [extracted_info['mood']] if extracted_info['mood'] else [],
            extracted_info['cuisine_preference'],
            extracted_info['allergies']
        ] if field)
        
        return min(1.0, filled_fields / total_fields + 0.2)  # Base confidence of 0.2
    
    def generate_explanation(self, item: Dict[str, Any], query_info: Dict[str, Any]) -> str:
        """Generate explanation for recommendation based on query"""
        explanations = []
        
        # Item name
        item_name = item.get('name', 'this item')
        
        # Intent-based explanation
        intent = query_info.get('intent', 'browse')
        if intent == 'dietary_restriction':
            dietary = query_info.get('filters', {}).get('dietary')
            if dietary and dietary in item.get('dietary_tags', []):
                explanations.append(f"perfect for your {dietary} diet")
        elif intent == 'price_sensitive':
            price = query_info.get('filters', {}).get('price')
            if price and item.get('budget_category') == price:
                explanations.append(f"fits your {price} budget")
        elif intent == 'mood_based':
            mood = query_info.get('filters', {}).get('mood')
            if mood:
                explanations.append(f"great for a {mood} occasion")
        
        # General explanations
        if item.get('category'):
            explanations.append(f"from our {item['category']} selection")
        
        if item.get('time_preference'):
            explanations.append(f"perfect for {item['time_preference']}")
        
        if explanations:
            return f"I recommend {item_name} because it's {' and '.join(explanations)}!"
        else:
            return f"I recommend {item_name} - it's a great choice from our menu!"


# Global instance
_query_processor = None

def get_query_processor() -> SmartQueryProcessor:
    """Get global query processor instance"""
    global _query_processor
    if _query_processor is None:
        _query_processor = SmartQueryProcessor()
    return _query_processor

