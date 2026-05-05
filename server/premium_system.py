"""
MindBridge Premium Subscription System
Income generation ko lagi freemium model
"""

import os
import json
from datetime import datetime, timedelta

# Free tier limits
FREE_TIER_LIMITS = {
    'daily_chat_messages': 20,
    'emotion_detections': 10,
    'video_consultations': 0,  # Premium only
    'mood_entries': 5
}

# Premium tier features
PREMIUM_FEATURES = {
    'unlimited_chat': True,
    'unlimited_emotion_detection': True,
    'video_consultations': True,
    'no_ads': True,
    'priority_support': True,
    'advanced_analytics': True
}

PREMIUM_PRICE_USD = 4.99  # per month


def check_user_limit(user_id: str, feature: str, db_helper) -> dict:
    """
    Check if free user has reached their daily limit
    Returns: {'allowed': bool, 'remaining': int, 'is_premium': bool}
    """
    try:
        user = db_helper.get_user_by_id(user_id)
        if not user:
            return {'allowed': False, 'remaining': 0, 'is_premium': False}
        
        # Premium users - no limits
        is_premium = getattr(user, 'is_premium', False) or user.get('is_premium', False)
        if is_premium:
            return {'allowed': True, 'remaining': 999, 'is_premium': True}
        
        # Free users - check daily limit
        limit = FREE_TIER_LIMITS.get(feature, 10)
        
        # TODO: Count today's usage from database
        # For now, allow all free users
        return {
            'allowed': True,
            'remaining': limit,
            'is_premium': False,
            'limit': limit,
            'upgrade_message': f'Free plan: {limit} {feature} per day. Upgrade to Premium for unlimited access!'
        }
        
    except Exception as e:
        print(f"Error checking user limit: {e}")
        return {'allowed': True, 'remaining': 10, 'is_premium': False}


def get_premium_info() -> dict:
    """Premium plan information return garne"""
    return {
        'price': PREMIUM_PRICE_USD,
        'currency': 'USD',
        'billing': 'monthly',
        'features': [
            '✅ Unlimited AI Chat Messages',
            '✅ Unlimited Emotion Detection',
            '✅ Video Doctor Consultations',
            '✅ No Advertisements',
            '✅ Priority Support',
            '✅ Advanced Analytics & Reports',
            '✅ Export Your Data'
        ],
        'free_features': [
            f'💬 {FREE_TIER_LIMITS["daily_chat_messages"]} AI messages/day',
            f'📸 {FREE_TIER_LIMITS["emotion_detections"]} emotion detections/day',
            '📊 Basic mood tracking',
            '🎮 Relaxation games',
            '⚠️ Ads supported'
        ]
    }
