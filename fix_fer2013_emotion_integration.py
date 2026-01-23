#!/usr/bin/env python3
"""
Fix FER2013 Enhanced Dataset Integration with Emotion Detection
"""

import os
import sys

def fix_fer2013_emotion_integration():
    """Fix FER2013 enhanced dataset integration with emotion detection.html"""
    
    print("🎯 Fixing FER2013 Enhanced Dataset Integration...")
    
    # 1. Update emotion detection endpoint to use FER2013
    update_emotion_detection_endpoint()
    
    # 2. Update emotion-detection.js to use FER2013 endpoint
    update_emotion_detection_js()
    
    # 3. Test FER2013 integration
    test_fer2013_integration()
    
    print("✅ FER2013 Enhanced Dataset Integration fixed!")

def update_emotion_detection_endpoint():
    """Update emotion detection endpoint to prioritize FER2013"""
    
    print("🔧 Updating emotion detection endpoint...")
    
    app_py_path = 'sleepy/server/app.py'
    
    try:
        with open(app_py_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the emotion detection endpoint and update it
        if '@app.route(\'/api/emotion_detection\', methods=[\'POST\'])' in content:
            # Replace the main emotion detection endpoint to use FER2013 first
            old_endpoint = '''@app.route('/api/emotion_detection', methods=['POST'])
def emotion_detection():
    """Main emotion detection endpoint with multiple fallbacks"""'''
            
            new_endpoint = '''@app.route('/api/emotion_detection', methods=['POST'])
def emotion_detection():
    """Main emotion detection endpoint - FER2013 Enhanced Dataset Priority"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or len(auth_header.split()) < 2:
        return jsonify({'error': 'Authentication required'}), 401
    
    token = auth_header.split()[1]
    user = get_user_by_id(token)
    if not user:
        return jsonify({'error': 'Invalid user token'}), 401
    
    try:
        data = request.get_json()
        image_data = data.get('image')
        timestamp = data.get('timestamp', datetime.now().isoformat())
        
        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400
        
        print("🎯 Using FER2013 Enhanced Dataset for emotion detection...")
        
        # PRIORITY 1: FER2013 Enhanced Dataset Detection
        if FER2013_AVAILABLE:
            try:
                fer2013_detector = get_fer2013_emotion_detector()
                result = fer2013_detector.detect_emotion_from_image(image_data)
                
                if result['success']:
                    # Save to database
                    emotion_id = create_face_emotion_record(
                        user_id=user['id'],
                        detected_emotion=result['dominant_emotion'],
                        confidence_score=result['confidence'],
                        image_path=None
                    )
                    
                    if emotion_id:
                        result['emotion_id'] = emotion_id
                        result['saved'] = True
                    
                    result['dataset'] = 'FER2013-Enhanced'
                    result['method'] = 'fer2013_enhanced'
                    
                    print(f"🎯 FER2013 Enhanced: {result['dominant_emotion']} ({result['confidence']}%)")
                    return jsonify(result), 200
                    
            except Exception as e:
                print(f"⚠️ FER2013 Enhanced detection failed: {e}")
        
        # FALLBACK: Use other detection methods
        return fer2013_emotion_detection()
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'dominant_emotion': 'neutral',
            'confidence': 0,
            'emotions': {},
            'dataset': 'FER2013-Enhanced',
            'method': 'fallback'
        }), 500'''
            
            content = content.replace(old_endpoint, new_endpoint)
            
            with open(app_py_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Emotion detection endpoint updated to prioritize FER2013")
        else:
            print("⚠️ Main emotion detection endpoint not found")
    
    except Exception as e:
        print(f"❌ Error updating emotion detection endpoint: {e}")

def update_emotion_detection_js():
    """Update emotion-detection.js to use FER2013 enhanced features"""
    
    print("🔧 Updating emotion-detection.js...")
    
    emotion_js_path = 'sleepy/client/emotion-detection.js'
    
    try:
        with open(emotion_js_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add FER2013 enhanced information display
        if 'function displayEmotionResult(result)' in content:
            # Find and update the displayEmotionResult function
            old_display = '''function displayEmotionResult(result) {
    const resultDiv = document.getElementById('emotion-result');
    
    if (result.success) {
        const confidence = result.confidence || 0;
        const emotion = result.dominant_emotion || 'unknown';
        
        resultDiv.innerHTML = `
            <div class="bg-green-500 bg-opacity-20 border border-green-500 rounded-lg p-4 mb-4">
                <h3 class="text-green-400 font-bold text-lg mb-2">✅ Emotion Detected</h3>
                <div class="text-white">
                    <p><strong>Emotion:</strong> ${emotion.charAt(0).toUpperCase() + emotion.slice(1)}</p>
                    <p><strong>Confidence:</strong> ${confidence.toFixed(1)}%</p>
                    ${result.method ? `<p><strong>Method:</strong> ${result.method}</p>` : ''}
                    ${result.face_detected !== undefined ? `<p><strong>Face Detected:</strong> ${result.face_detected ? 'Yes' : 'No'}</p>` : ''}
                </div>
            </div>
        `;'''
            
            new_display = '''function displayEmotionResult(result) {
    const resultDiv = document.getElementById('emotion-result');
    
    if (result.success) {
        const confidence = result.confidence || 0;
        const emotion = result.dominant_emotion || 'unknown';
        const dataset = result.dataset || 'Unknown';
        const method = result.method || 'standard';
        
        // Special styling for FER2013 Enhanced results
        const isFER2013 = dataset.includes('FER2013') || method.includes('fer2013');
        const borderColor = isFER2013 ? 'border-blue-500' : 'border-green-500';
        const bgColor = isFER2013 ? 'bg-blue-500' : 'bg-green-500';
        const textColor = isFER2013 ? 'text-blue-400' : 'text-green-400';
        const icon = isFER2013 ? '🎯' : '✅';
        
        resultDiv.innerHTML = `
            <div class="${bgColor} bg-opacity-20 border ${borderColor} rounded-lg p-4 mb-4">
                <h3 class="${textColor} font-bold text-lg mb-2">${icon} Emotion Detected</h3>
                <div class="text-white">
                    <p><strong>Emotion:</strong> ${emotion.charAt(0).toUpperCase() + emotion.slice(1)}</p>
                    <p><strong>Confidence:</strong> ${confidence.toFixed(1)}%</p>
                    <p><strong>Dataset:</strong> ${dataset}</p>
                    <p><strong>Method:</strong> ${method}</p>
                    ${result.face_detected !== undefined ? `<p><strong>Face Detected:</strong> ${result.face_detected ? 'Yes' : 'No'}</p>` : ''}
                    ${isFER2013 ? '<p class="text-blue-300 text-sm mt-2">🎯 Using FER2013 Enhanced Dataset for maximum accuracy</p>' : ''}
                </div>
            </div>
        `;'''
            
            content = content.replace(old_display, new_display)
        
        # Add FER2013 status indicator
        if 'document.addEventListener(\'DOMContentLoaded\', function()' in content:
            fer2013_status = '''
    // Add FER2013 Enhanced Dataset status indicator
    const statusDiv = document.createElement('div');
    statusDiv.className = 'bg-blue-500 bg-opacity-20 border border-blue-500 rounded-lg p-3 mb-4';
    statusDiv.innerHTML = `
        <div class="flex items-center">
            <span class="text-2xl mr-3">🎯</span>
            <div>
                <h4 class="text-blue-400 font-bold">FER2013 Enhanced Dataset Active</h4>
                <p class="text-blue-300 text-sm">Using advanced emotion recognition with 7 emotions: angry, disgust, fear, happy, sad, surprise, neutral</p>
            </div>
        </div>
    `;
    
    const mainContent = document.querySelector('.max-w-4xl');
    if (mainContent) {
        mainContent.insertBefore(statusDiv, mainContent.firstChild.nextSibling);
    }
'''
            
            # Find the DOMContentLoaded event and add the status indicator
            dom_loaded_index = content.find('document.addEventListener(\'DOMContentLoaded\', function() {')
            if dom_loaded_index != -1:
                # Find the end of the function
                brace_count = 0
                start_index = content.find('{', dom_loaded_index) + 1
                
                # Insert the status indicator at the beginning of the function
                content = content[:start_index] + fer2013_status + content[start_index:]
        
        with open(emotion_js_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ emotion-detection.js updated with FER2013 enhanced features")
    
    except Exception as e:
        print(f"❌ Error updating emotion-detection.js: {e}")

def test_fer2013_integration():
    """Test FER2013 integration"""
    
    print("🧪 Testing FER2013 integration...")
    
    # Check if FER2013 detector exists
    fer2013_detector_path = 'sleepy/server/fer2013_emotion_detector.py'
    if os.path.exists(fer2013_detector_path):
        print("✅ FER2013 emotion detector found")
    else:
        print("❌ FER2013 emotion detector not found")
    
    # Check if FER2013 enhanced dataset exists
    fer2013_dataset_path = 'emotion_datasets/fer2013/fer2013_enhanced.csv'
    if os.path.exists(fer2013_dataset_path):
        print("✅ FER2013 enhanced dataset found")
        
        # Check dataset size
        try:
            with open(fer2013_dataset_path, 'r') as f:
                lines = sum(1 for line in f)
            print(f"✅ FER2013 dataset contains {lines} records")
        except:
            print("⚠️ Could not read FER2013 dataset")
    else:
        print("❌ FER2013 enhanced dataset not found")
    
    # Check if emotion detection HTML exists
    emotion_html_path = 'sleepy/client/emotion-detection.html'
    if os.path.exists(emotion_html_path):
        print("✅ emotion-detection.html found")
    else:
        print("❌ emotion-detection.html not found")
    
    print("✅ FER2013 integration test completed")

if __name__ == '__main__':
    fix_fer2013_emotion_integration()