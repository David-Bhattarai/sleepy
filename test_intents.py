import json
import random

# Load intents
with open('server/intents.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    INTENTS = data.get('intents', [])

def test_intent_matching(user_message):
    message = user_message.lower()
    best_tag = None
    best_score = 0
    
    print(f'Testing: "{user_message}"')
    
    for intent in INTENTS:
        patterns = intent.get('patterns', [])
        for pattern in patterns:
            p = pattern.lower().strip()
            if not p:
                continue
            score = 0
            if p in message:
                score = len(p)
                if score > best_score:
                    print(f'  Exact match: "{p}" (score: {score})')
            else:
                message_words = set(message.split())
                pattern_words = set(p.split())
                overlap = len(message_words & pattern_words)
                if overlap > 0:
                    score = overlap
            
            if score > best_score:
                best_score = score
                best_tag = intent.get('tag')
    
    print(f'Best: tag="{best_tag}", score={best_score}')
    
    # Get response
    if best_tag:
        for intent in INTENTS:
            if intent.get('tag') == best_tag:
                responses = intent.get('responses', [])
                if responses:
                    response = responses[0]  # First response for consistency
                    print(f'Response: "{response[:80]}..."')
                    return response
    
    print('No match - fallback')
    return None

# Test cases
test_intent_matching('I feel so anxious')
print('---')
test_intent_matching('Hello there')
print('---')
test_intent_matching('I want to kill myself')
print('---')
test_intent_matching('What is depression')
print('---')
test_intent_matching('random gibberish text')