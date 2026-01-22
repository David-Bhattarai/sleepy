/**
 * Advanced Emotion Detection System
 * Real-time face analysis with ML-powered recommendations
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const startCameraBtn = document.getElementById('start-camera');
    const captureEmotionBtn = document.getElementById('capture-emotion');
    const stopCameraBtn = document.getElementById('stop-camera');
    const detectionOverlay = document.getElementById('detection-overlay');
    const recommendationsSection = document.getElementById('recommendations-section');
    
    // Current emotion display elements
    const emotionIcon = document.getElementById('emotion-icon');
    const emotionName = document.getElementById('emotion-name');
    const confidenceCircle = document.getElementById('confidence-circle');
    const confidenceText = document.getElementById('confidence-text');
    const emotionBreakdown = document.getElementById('emotion-breakdown');
    
    // State variables
    let stream = null;
    let isDetecting = false;
    let emotionHistory = [];
    let currentUser = null;
    let emotionChart = null;
    
    // Emotion mappings
    const emotionEmojis = {
        'happy': '😊',
        'sad': '😢',
        'angry': '😠',
        'fear': '😨',
        'surprise': '😲',
        'disgust': '🤢',
        'neutral': '😐',
        'calm': '😌',
        'excited': '🤩',
        'confused': '😕',
        'tired': '😴',
        'stressed': '😰'
    };
    
    const emotionColors = {
        'happy': '#10B981',
        'sad': '#3B82F6',
        'angry': '#EF4444',
        'fear': '#8B5CF6',
        'surprise': '#F59E0B',
        'disgust': '#84CC16',
        'neutral': '#6B7280',
        'calm': '#06B6D4',
        'excited': '#EC4899',
        'confused': '#F97316',
        'tired': '#6366F1',
        'stressed': '#DC2626'
    };
    
    // Initialize the system
    initializeEmotionDetection();
    
    function initializeEmotionDetection() {
        console.log('Initializing Advanced Emotion Detection System...');
        
        // Check for user authentication
        const token = localStorage.getItem('token');
        if (!token) {
            window.location.href = '/signin.html';
            return;
        }
        
        // Get user info
        currentUser = {
            id: token,
            name: localStorage.getItem('userName') || 'User'
        };
        
        // Set up event listeners
        startCameraBtn.addEventListener('click', startCamera);
        captureEmotionBtn.addEventListener('click', captureAndAnalyze);
        stopCameraBtn.addEventListener('click', stopCamera);
        
        // Load emotion history
        loadEmotionHistory();
        
        // Initialize chart
        initializeEmotionChart();
        
        // Load analytics
        loadAdvancedAnalytics();
        
        console.log('Emotion Detection System Ready!');
    }
    
    async function startCamera() {
        try {
            console.log('Starting camera...');
            
            stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: 'user'
                },
                audio: false
            });
            
            video.srcObject = stream;
            
            // Update button states
            startCameraBtn.disabled = true;
            captureEmotionBtn.disabled = false;
            stopCameraBtn.disabled = false;
            
            console.log('Camera started successfully');
            
        } catch (error) {
            console.error('Error accessing camera:', error);
            alert('Could not access camera. Please check permissions.');
        }
    }
    
    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            stream = null;
        }
        
        video.srcObject = null;
        
        // Update button states
        startCameraBtn.disabled = false;
        captureEmotionBtn.disabled = true;
        stopCameraBtn.disabled = true;
        
        console.log('Camera stopped');
    }
    
    async function captureAndAnalyze() {
        if (isDetecting) return;
        
        isDetecting = true;
        detectionOverlay.classList.add('active');
        captureEmotionBtn.disabled = true;
        
        try {
            // Capture frame from video
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            ctx.drawImage(video, 0, 0);
            
            // Convert to base64
            const imageData = canvas.toDataURL('image/jpeg', 0.8);
            
            console.log('Analyzing emotion...');
            
            // Send to backend for analysis
            const response = await fetch('/api/emotion_detection_advanced', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${currentUser.id}`
                },
                body: JSON.stringify({
                    image: imageData,
                    timestamp: new Date().toISOString()
                })
            });
            
            if (!response.ok) {
                throw new Error('Failed to analyze emotion');
            }
            
            const result = await response.json();
            console.log('Emotion analysis result:', result);
            
            // Update UI with results
            updateEmotionDisplay(result);
            
            // Add to history
            emotionHistory.unshift(result);
            if (emotionHistory.length > 50) {
                emotionHistory.pop();
            }
            
            // Update chart and analytics
            updateEmotionChart();
            updateRecentDetections();
            loadPersonalizedRecommendations(result.dominant_emotion);
            
        } catch (error) {
            console.error('Error analyzing emotion:', error);
            alert('Failed to analyze emotion. Please try again.');
        } finally {
            isDetecting = false;
            detectionOverlay.classList.remove('active');
            captureEmotionBtn.disabled = false;
        }
    }
    
    function updateEmotionDisplay(result) {
        const dominantEmotion = result.dominant_emotion;
        const confidence = result.confidence;
        const emotions = result.emotions;
        
        // Update main emotion display
        emotionIcon.textContent = emotionEmojis[dominantEmotion] || '😐';
        emotionName.textContent = dominantEmotion.charAt(0).toUpperCase() + dominantEmotion.slice(1);
        
        // Update confidence circle
        const circumference = 2 * Math.PI * 52;
        const offset = circumference - (confidence / 100) * circumference;
        confidenceCircle.style.strokeDashoffset = offset;
        confidenceText.textContent = `${Math.round(confidence)}%`;
        
        // Update emotion breakdown
        updateEmotionBreakdown(emotions);
    }
    
    function updateEmotionBreakdown(emotions) {
        emotionBreakdown.innerHTML = '<h4 class="text-lg font-semibold text-white mb-4">Emotion Analysis</h4>';
        
        Object.entries(emotions).forEach(([emotion, percentage]) => {
            const color = emotionColors[emotion] || '#6B7280';
            const emoji = emotionEmojis[emotion] || '😐';
            
            const emotionBar = document.createElement('div');
            emotionBar.className = 'flex items-center space-x-3';
            emotionBar.innerHTML = `
                <span class="text-xl">${emoji}</span>
                <span class="text-white font-medium w-20">${emotion}</span>
                <div class="flex-1 bg-gray-700 rounded-full h-2">
                    <div class="h-2 rounded-full transition-all duration-500" 
                         style="width: ${percentage}%; background-color: ${color}"></div>
                </div>
                <span class="text-gray-300 text-sm w-12">${Math.round(percentage)}%</span>
            `;
            
            emotionBreakdown.appendChild(emotionBar);
        });
    }
    
    async function loadPersonalizedRecommendations(emotion) {
        try {
            const response = await fetch(`/api/emotion_recommendations/${emotion}`, {
                headers: {
                    'Authorization': `Bearer ${currentUser.id}`
                }
            });
            
            if (!response.ok) {
                throw new Error('Failed to load recommendations');
            }
            
            const recommendations = await response.json();
            displayRecommendations(recommendations);
            
        } catch (error) {
            console.error('Error loading recommendations:', error);
            displayDefaultRecommendations(emotion);
        }
    }
    
    function displayRecommendations(recommendations) {
        const grid = document.getElementById('recommendations-grid');
        grid.innerHTML = '';
        
        recommendations.forEach(rec => {
            const card = document.createElement('div');
            card.className = 'recommendation-card p-6 rounded-xl';
            card.innerHTML = `
                <div class="text-center mb-4">
                    <div class="w-16 h-16 bg-gradient-to-br ${rec.gradient} rounded-full mx-auto mb-3 flex items-center justify-center">
                        <span class="text-2xl">${rec.icon}</span>
                    </div>
                    <h3 class="text-xl font-bold text-white mb-2">${rec.title}</h3>
                </div>
                <p class="text-gray-300 text-sm mb-4">${rec.description}</p>
                <div class="space-y-2">
                    ${rec.actions.map(action => `
                        <button class="w-full py-2 px-4 bg-white bg-opacity-10 hover:bg-opacity-20 text-white rounded-lg transition-colors text-sm">
                            ${action}
                        </button>
                    `).join('')}
                </div>
            `;
            
            grid.appendChild(card);
        });
        
        recommendationsSection.classList.remove('hidden');
    }
    
    function displayDefaultRecommendations(emotion) {
        const defaultRecs = getDefaultRecommendations(emotion);
        displayRecommendations(defaultRecs);
    }
    
    function getDefaultRecommendations(emotion) {
        const recommendations = {
            'happy': [
                {
                    title: 'Maintain Positivity',
                    description: 'Keep this positive energy flowing with activities that bring you joy.',
                    icon: '🌟',
                    gradient: 'from-yellow-500 to-orange-500',
                    actions: ['Share your happiness', 'Practice gratitude', 'Help others']
                },
                {
                    title: 'Social Connection',
                    description: 'Connect with friends and family to spread the positive vibes.',
                    icon: '👥',
                    gradient: 'from-green-500 to-blue-500',
                    actions: ['Call a friend', 'Plan social activities', 'Join communities']
                }
            ],
            'sad': [
                {
                    title: 'Self-Care Activities',
                    description: 'Take time for yourself with gentle, nurturing activities.',
                    icon: '🛁',
                    gradient: 'from-blue-500 to-purple-500',
                    actions: ['Take a warm bath', 'Listen to music', 'Practice self-compassion']
                },
                {
                    title: 'Professional Support',
                    description: 'Consider reaching out to a mental health professional.',
                    icon: '🩺',
                    gradient: 'from-purple-500 to-pink-500',
                    actions: ['Book consultation', 'Join support groups', 'Talk to counselor']
                }
            ],
            'angry': [
                {
                    title: 'Anger Management',
                    description: 'Channel your anger into productive activities and coping strategies.',
                    icon: '🧘',
                    gradient: 'from-red-500 to-orange-500',
                    actions: ['Deep breathing', 'Physical exercise', 'Journaling']
                },
                {
                    title: 'Stress Relief',
                    description: 'Use proven techniques to reduce stress and calm your mind.',
                    icon: '🌿',
                    gradient: 'from-green-500 to-teal-500',
                    actions: ['Meditation', 'Nature walk', 'Progressive relaxation']
                }
            ],
            'fear': [
                {
                    title: 'Anxiety Support',
                    description: 'Techniques to help manage fear and anxiety effectively.',
                    icon: '🛡️',
                    gradient: 'from-purple-500 to-blue-500',
                    actions: ['Grounding exercises', 'Breathing techniques', 'Mindfulness']
                },
                {
                    title: 'Professional Help',
                    description: 'Consider professional support for managing persistent fears.',
                    icon: '💪',
                    gradient: 'from-blue-500 to-green-500',
                    actions: ['Therapy sessions', 'Support groups', 'Counseling']
                }
            ],
            'neutral': [
                {
                    title: 'Emotional Awareness',
                    description: 'Explore your emotions and develop greater self-awareness.',
                    icon: '🎯',
                    gradient: 'from-gray-500 to-blue-500',
                    actions: ['Mood journaling', 'Mindfulness practice', 'Self-reflection']
                },
                {
                    title: 'Wellness Activities',
                    description: 'Engage in activities that promote overall mental wellness.',
                    icon: '🌱',
                    gradient: 'from-green-500 to-blue-500',
                    actions: ['Exercise routine', 'Healthy eating', 'Sleep hygiene']
                }
            ]
        };
        
        return recommendations[emotion] || recommendations['neutral'];
    }
    
    async function loadEmotionHistory() {
        try {
            const response = await fetch('/api/emotion_history', {
                headers: {
                    'Authorization': `Bearer ${currentUser.id}`
                }
            });
            
            if (response.ok) {
                const history = await response.json();
                emotionHistory = history.slice(0, 50); // Keep last 50 entries
                updateEmotionChart();
                updateRecentDetections();
            }
        } catch (error) {
            console.error('Error loading emotion history:', error);
        }
    }
    
    function initializeEmotionChart() {
        const ctx = document.getElementById('emotion-chart').getContext('2d');
        
        emotionChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Dominant Emotion Confidence',
                    data: [],
                    borderColor: '#3B82F6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#ffffff'
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: '#9CA3AF'
                        },
                        grid: {
                            color: 'rgba(156, 163, 175, 0.2)'
                        }
                    },
                    y: {
                        ticks: {
                            color: '#9CA3AF'
                        },
                        grid: {
                            color: 'rgba(156, 163, 175, 0.2)'
                        },
                        min: 0,
                        max: 100
                    }
                }
            }
        });
    }
    
    function updateEmotionChart() {
        if (!emotionChart || emotionHistory.length === 0) return;
        
        const last20 = emotionHistory.slice(0, 20).reverse();
        const labels = last20.map((_, index) => `${index + 1}`);
        const data = last20.map(entry => entry.confidence || 0);
        
        emotionChart.data.labels = labels;
        emotionChart.data.datasets[0].data = data;
        emotionChart.update();
    }
    
    function updateRecentDetections() {
        const container = document.getElementById('recent-detections');
        container.innerHTML = '';
        
        const recent = emotionHistory.slice(0, 8);
        
        recent.forEach(detection => {
            const card = document.createElement('div');
            card.className = 'bg-white bg-opacity-10 rounded-lg p-4 text-center';
            card.innerHTML = `
                <div class="text-3xl mb-2">${emotionEmojis[detection.dominant_emotion] || '😐'}</div>
                <div class="text-white font-semibold text-sm">${detection.dominant_emotion}</div>
                <div class="text-gray-300 text-xs">${Math.round(detection.confidence)}%</div>
                <div class="text-gray-400 text-xs mt-1">${formatTime(detection.timestamp)}</div>
            `;
            container.appendChild(card);
        });
    }
    
    async function loadAdvancedAnalytics() {
        try {
            const response = await fetch('/api/emotion_analytics', {
                headers: {
                    'Authorization': `Bearer ${currentUser.id}`
                }
            });
            
            if (response.ok) {
                const analytics = await response.json();
                updateAnalyticsDisplay(analytics);
            }
        } catch (error) {
            console.error('Error loading analytics:', error);
        }
    }
    
    function updateAnalyticsDisplay(analytics) {
        // Update dominant emotion
        document.getElementById('dominant-emotion-icon').textContent = 
            emotionEmojis[analytics.dominant_emotion] || '😐';
        document.getElementById('dominant-emotion-name').textContent = 
            analytics.dominant_emotion || 'Neutral';
        document.getElementById('dominant-emotion-percentage').textContent = 
            `${analytics.dominant_percentage || 0}%`;
        
        // Update stability score
        document.getElementById('stability-score').textContent = 
            analytics.stability_score || '0.0';
        document.getElementById('stability-description').textContent = 
            analytics.stability_description || 'Unknown';
        
        // Update session counts
        document.getElementById('total-sessions').textContent = 
            analytics.total_sessions || '0';
        document.getElementById('sessions-this-week').textContent = 
            `${analytics.sessions_this_week || 0} this week`;
    }
    
    function formatTime(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }
    
    console.log('Advanced Emotion Detection System Loaded!');
});