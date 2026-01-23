#!/usr/bin/env python3
"""
Unlimited Gemini System
Rotates between multiple API keys for unlimited usage
"""

import os
import random
import time
from datetime import datetime, timedelta

class UnlimitedGeminiManager:
    """Manages multiple Gemini API keys for unlimited usage"""
    
    def __init__(self):
        # Add multiple API keys here
        self.api_keys = [
            'AIzaSyAhVtegrJ6sXOp2Ri0AkI5_yQDGAGWsJxk',  # Your current key
            # Add more keys here:
            # 'AIzaSy...',  # Key 2
            # 'AIzaSy...',  # Key 3
            # 'AIzaSy...',  # Key 4
        ]
        
        self.current_key_index = 0
        self.request_counts = {key: 0 for key in self.api_keys}
        self.last_reset = {key: datetime.now() for key in self.api_keys}
        self.daily_limit = 1500  # Per key
        self.minute_limit = 15   # Per key per minute
        self.minute_counts = {key: [] for key in self.api_keys}
        
        print(f"🔑 Unlimited Gemini Manager initialized with {len(self.api_keys)} API keys")
    
    def get_available_key(self):
        """Get an available API key that hasn't exceeded limits"""
        current_time = datetime.now()
        
        # Reset daily counts if needed
        for key in self.api_keys:
            if current_time - self.last_reset[key] > timedelta(days=1):
                self.request_counts[key] = 0
                self.last_reset[key] = current_time
                print(f"🔄 Daily quota reset for key {key[:10]}...")
        
        # Find available key
        for i, key in enumerate(self.api_keys):
            # Check daily limit
            if self.request_counts[key] >= self.daily_limit:
                continue
            
            # Check minute limit
            minute_ago = current_time - timedelta(minutes=1)
            recent_requests = [t for t in self.minute_counts[key] if t > minute_ago]
            self.minute_counts[key] = recent_requests
            
            if len(recent_requests) >= self.minute_limit:
                continue
            
            # This key is available
            self.current_key_index = i
            return key
        
        # All keys exhausted - return first key anyway (will handle error)
        print("⚠️ All API keys at limit - using first key")
        return self.api_keys[0]
    
    def record_request(self, key):
        """Record that a request was made with this key"""
        self.request_counts[key] += 1
        self.minute_counts[key].append(datetime.now())
        
        remaining = self.daily_limit - self.request_counts[key]
        print(f"📊 Key {key[:10]}... used: {self.request_counts[key]}/{self.daily_limit} (remaining: {remaining})")
    
    def get_status(self):
        """Get status of all API keys"""
        status = []
        for key in self.api_keys:
            remaining = self.daily_limit - self.request_counts[key]
            status.append({
                'key': key[:10] + '...',
                'used': self.request_counts[key],
                'remaining': remaining,
                'percentage': (self.request_counts[key] / self.daily_limit) * 100
            })
        return status

# Global manager instance
unlimited_manager = None

def get_unlimited_gemini_manager():
    """Get the unlimited Gemini manager instance"""
    global unlimited_manager
    if unlimited_manager is None:
        unlimited_manager = UnlimitedGeminiManager()
    return unlimited_manager

def configure_gemini_with_rotation():
    """Configure Gemini AI with key rotation"""
    try:
        import google.generativeai as genai
        
        manager = get_unlimited_gemini_manager()
        api_key = manager.get_available_key()
        
        genai.configure(api_key=api_key)
        
        return api_key
    except Exception as e:
        print(f"❌ Error configuring Gemini: {e}")
        return None

def make_gemini_request(prompt, is_vision=False, image_data=None):
    """Make a Gemini request with automatic key rotation"""
    try:
        import google.generativeai as genai
        
        manager = get_unlimited_gemini_manager()
        
        # Try up to 3 different keys
        for attempt in range(min(3, len(manager.api_keys))):
            try:
                api_key = manager.get_available_key()
                genai.configure(api_key=api_key)
                
                if is_vision and image_data:
                    # Vision request
                    model = genai.GenerativeModel('models/gemini-2.0-flash-exp')
                    response = model.generate_content([prompt, image_data])
                else:
                    # Text request
                    model = genai.GenerativeModel('models/gemini-2.0-flash-exp')
                    response = model.generate_content(prompt)
                
                # Success - record the request
                manager.record_request(api_key)
                
                return {
                    'success': True,
                    'response': response.text if response else '',
                    'api_key_used': api_key[:10] + '...'
                }
                
            except Exception as e:
                error_msg = str(e)
                if '429' in error_msg or 'quota' in error_msg.lower():
                    print(f"⚠️ Key {api_key[:10]}... quota exceeded, trying next key...")
                    # Mark this key as exhausted
                    manager.request_counts[api_key] = manager.daily_limit
                    continue
                else:
                    print(f"❌ Gemini request error: {e}")
                    break
        
        # All keys failed
        return {
            'success': False,
            'error': 'All API keys exhausted or failed',
            'api_key_used': None
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'api_key_used': None
        }

def add_new_api_key(new_key):
    """Add a new API key to the rotation"""
    manager = get_unlimited_gemini_manager()
    if new_key not in manager.api_keys:
        manager.api_keys.append(new_key)
        manager.request_counts[new_key] = 0
        manager.last_reset[new_key] = datetime.now()
        manager.minute_counts[new_key] = []
        print(f"✅ Added new API key: {new_key[:10]}...")
        return True
    else:
        print("⚠️ API key already exists")
        return False

def get_quota_status():
    """Get quota status for all keys"""
    manager = get_unlimited_gemini_manager()
    return manager.get_status()