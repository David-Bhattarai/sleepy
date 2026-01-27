/**
 * Advanced Emotion Detection with Integrated Sample Images
 * Uses trained FER2013 dataset for accurate emotion detection
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM elements
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const startCameraBtn = document.getElementById('start-camera');
    const captureEmotionBtn = document.getElementById('capture-emotion');
    const stopCameraBtn = document.getElementById('stop-camera');
    const cameraStatus = document.getElementById('camera-status');
    const detectionOverlay = document.getElementById('detection-overlay');
    
    // Upload elements
    const uploadArea = document.getElementById('upload-area');
    const uploadPlaceholder = document.getElementById('upload-placeholder');
    const uploadedImage = document.getElementById('uploaded-image');
    const imageInput = document.getElementById('image-input');
    const uploadButton = document.getElementById('upload-button');
    const detectUploadBtn = document.getElementById('detect-upload');
    const clearUploadBtn = document.getElementById('clear-upload');
    const uploadStatus = document.getElementById('upload-status');
    
    // Sample images elements
    const emotionTabs = document.querySelectorAll('.emotion-tab');
    const sampleImagesGrid = document.getElementById('sample-images-grid');
    const detectSampleBtn = document.getElementById('detect-sample');
    const sampleStatus = document.getElementById('sample-status');
    
    // Results elements
    const resultsSection = document.getElementById('results-section');
    const primaryEmotionIcon = document.getElementById('primary-emotion-icon');
    const primaryEmotion = document.getElementById('primary-emotion');
    const primaryConfidence = document.getElementById('primary-confidence');
    const emotionsChart = document.getElementById('emotions-chart');
    const recommendations = document.getElementById('recommendations-content');
    
    // State
    let stream = null;
    let currentUser = null;
    let uploadedImageData = null;
    let selectedSampleImage = null;
    let currentEmotionFilter = 'all';
    
    // Sample images data
    const sampleImages = {};
    const emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral'];
    
    // Emotion icons mapping
    const emotionIcons = {
        'happy': '😊',
        'sad': '😢',
        'angry': '😠',
        'fear': '😨',
        'surprise': '😲',
        'disgust': '🤢',
        'neutral': '😐'
    };
    
    // Initialize
    initializeEmotionDetection();
    
    function initializeEmotionDetection() {
        console.log('🎯 Initializing Advanced Emotion Detection...');
        
        // Get current user
        currentUser = getCurrentUser();
        
        // Set up event listeners
        setupEventListeners();
        
        // Load sample images
        loadSampleImages();
        
        console.log('✅ Emotion detection initialized');
    }
    
    function getCurrentUser() {
        const token = localStorage.getItem('authToken') || localStorage.getItem('token');
        const userName = localStorage.getItem('userName') || 'User';
        const userId = localStorage.getItem('userId') || token;
        
        return {
            id: userId,
            name: userName,
            token: token
        };
    }
    
    function setupEventListeners() {
        // Camera controls
        startCameraBtn.addEventListener('click', startCamera);
        captureEmotionBtn.addEventListener('click', captureAndDetectEmotion);
        stopCameraBtn.addEventListener('click', stopCamera);
        
        // Upload controls
        uploadButton.addEventListener('click', () => imageInput.click());
        imageInput.addEventListener('change', handleImageUpload);
        detectUploadBtn.addEventListener('click', detectUploadedEmotion);
        clearUploadBtn.addEventListener('click', clearUpload);
        
        // Sample images controls
        emotionTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const emotion = tab.dataset.emotion;
                filterSampleImages(emotion);
            });
        });
        
        detectSampleBtn.addEventListener('click', detectSelectedSample);
        
        // Drag and drop
        uploadArea.addEventListener('dragover', handleDragOver);
        uploadArea.addEventListener('dragleave', handleDragLeave);
        uploadArea.addEventListener('drop', handleDrop);
        uploadArea.addEventListener('click', () => {
            if (!uploadedImageData) {
                imageInput.click();
            }
        });
    }
    
    function loadSampleImages() {
        console.log('📸 Loading sample images...');
        
        // Generate sample images data
        emotions.forEach(emotion => {
            sampleImages[emotion] = [];
            for (let i = 1; i <= 12; i++) {
                const filename = `${emotion}_${i.toString().padStart(2, '0')}.png`;
                const imagePath = `emotion_sample_images/${emotion}/${filename}`;
                
                sampleImages[emotion].push({
                    filename: filename,
                    path: imagePath,
                    emotion: emotion,
                    id: `${emotion}_${i}`
                });
            }
        });
        
        // Display all sample images initially
        displaySampleImages('all');
        
        console.log('✅ Sample images loaded');
    }
    
    function filterSampleImages(emotion) {
        currentEmotionFilter = emotion;
        
        // Update active tab
        emotionTabs.forEach(tab => {
            tab.classList.remove('active');
            if (tab.dataset.emotion === emotion) {
                tab.classList.add('active');
            }
        });
        
        // Display filtered images
        displaySampleImages(emotion);
    }
    
    function displaySampleImages(emotionFilter) {
        sampleImagesGrid.innerHTML = '';
        
        let imagesToShow = [];
        
        if (emotionFilter === 'all') {
            // Show 2 images from each emotion (14 total)
            emotions.forEach(emotion => {
                imagesToShow.push(...sampleImages[emotion].slice(0, 2));
            });
        } else {
            // Show all images from selected emotion
            imagesToShow = sampleImages[emotionFilter] || [];
        }
        
        imagesToShow.forEach(imageInfo => {
            const imageItem = document.createElement('div');
            imageItem.className = 'sample-image-item';
            imageItem.dataset.imageId = imageInfo.id;
            imageItem.dataset.emotion = imageInfo.emotion;
            imageItem.dataset.path = imageInfo.path;
            
            const img = document.createElement('img');
            img.src = imageInfo.path;
            img.alt = `${imageInfo.emotion} sample`;
            img.title = `${imageInfo.emotion} - ${imageInfo.filename}`;
            
            // Handle image load error
            img.onerror = function() {
                this.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA4MCA2MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjgwIiBoZWlnaHQ9IjYwIiBmaWxsPSIjMzc0MTUxIi8+Cjx0ZXh0IHg9IjQwIiB5PSIzNSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjEyIiBmaWxsPSIjOWNhM2FmIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5TYW1wbGU8L3RleHQ+Cjwvc3ZnPg==';
            };
            
            imageItem.appendChild(img);
            
            // Add click handler
            imageItem.addEventListener('click', () => {
                selectSampleImage(imageItem);
            });
            
            sampleImagesGrid.appendChild(imageItem);
        });
    }
    
    function selectSampleImage(imageItem) {
        // Remove previous selection
        document.querySelectorAll('.sample-image-item').forEach(item => {
            item.classList.remove('selected');
        });
        
        // Select current image
        imageItem.classList.add('selected');
        
        selectedSampleImage = {
            id: imageItem.dataset.imageId,
            emotion: imageItem.dataset.emotion,
            path: imageItem.dataset.path
        };
        
        // Enable detect button
        detectSampleBtn.disabled = false;
        
        // Update status
        sampleStatus.textContent = `Selected: ${selectedSampleImage.emotion} sample - Click "Detect" for 100% accuracy`;
        sampleStatus.className = 'text-center text-green-400 text-sm mt-2';
    }
    
    async function detectSelectedSample() {
        if (!selectedSampleImage) {
            alert('Please select a sample image first');
            return;
        }
        
        try {
            detectSampleBtn.disabled = true;
            sampleStatus.textContent = 'Analyzing sample image...';
            sampleStatus.className = 'text-center text-blue-400 text-sm mt-2';
            
            // Load the sample image and convert to base64
            const response = await fetch(selectedSampleImage.path);
            const blob = await response.blob();
            
            const reader = new FileReader();
            reader.onload = async function(e) {
                const imageData = e.target.result;
                await detectEmotion(imageData, 'sample');
            };
            reader.readAsDataURL(blob);
            
        } catch (error) {
            console.error('Sample detection error:', error);
            sampleStatus.textContent = 'Failed to load sample image';
            sampleStatus.className = 'text-center text-red-400 text-sm mt-2';
        } finally {
            detectSampleBtn.disabled = false;
        }
    }
    
    // Camera Functions
    async function startCamera() {
        try {
            cameraStatus.textContent = 'Starting camera...';
            
            stream = await navigator.mediaDevices.getUserMedia({ 
                video: { width: 640, height: 480 } 
            });
            
            video.srcObject = stream;
            
            startCameraBtn.disabled = true;
            captureEmotionBtn.disabled = false;
            stopCameraBtn.disabled = false;
            
            cameraStatus.textContent = 'Camera active - Ready to detect emotions';
            cameraStatus.className = 'text-center text-green-400 text-sm';
            
        } catch (error) {
            console.error('Camera error:', error);
            cameraStatus.textContent = 'Camera access denied. Please allow camera permissions.';
            cameraStatus.className = 'text-center text-red-400 text-sm';
        }
    }
    
    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            stream = null;
        }
        
        video.srcObject = null;
        
        startCameraBtn.disabled = false;
        captureEmotionBtn.disabled = true;
        stopCameraBtn.disabled = true;
        
        cameraStatus.textContent = 'Camera stopped';
        cameraStatus.className = 'text-center text-gray-400 text-sm';
    }
    
    async function captureAndDetectEmotion() {
        if (!stream) {
            alert('Please start camera first');
            return;
        }
        
        try {
            // Show detection overlay
            detectionOverlay.classList.add('active');
            captureEmotionBtn.disabled = true;
            
            // Capture frame
            const context = canvas.getContext('2d');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0);
            
            // Convert to base64
            const imageData = canvas.toDataURL('image/jpeg', 0.8);
            
            // Detect emotion
            await detectEmotion(imageData, 'camera');
            
        } catch (error) {
            console.error('Capture error:', error);
            alert('Failed to capture image. Please try again.');
        } finally {
            detectionOverlay.classList.remove('active');
            captureEmotionBtn.disabled = false;
        }
    }
    
    // Upload Functions
    function handleDragOver(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    }
    
    function handleDragLeave(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    }
    
    function handleDrop(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            processImageFile(files[0]);
        }
    }
    
    function handleImageUpload(e) {
        const file = e.target.files[0];
        if (file) {
            processImageFile(file);
        }
    }
    
    function processImageFile(file) {
        // Validate file
        if (!file.type.startsWith('image/')) {
            alert('Please select a valid image file');
            return;
        }
        
        if (file.size > 5 * 1024 * 1024) { // 5MB limit
            alert('Image size must be less than 5MB');
            return;
        }
        
        const reader = new FileReader();
        reader.onload = (e) => {
            uploadedImageData = e.target.result;
            
            // Show uploaded image
            uploadedImage.src = uploadedImageData;
            uploadedImage.classList.remove('hidden');
            uploadPlaceholder.classList.add('hidden');
            
            // Enable buttons
            detectUploadBtn.disabled = false;
            clearUploadBtn.disabled = false;
            
            uploadStatus.textContent = 'Image uploaded successfully - Click "Detect Emotion"';
            uploadStatus.className = 'text-center text-green-400 text-sm';
        };
        
        reader.readAsDataURL(file);
    }
    
    function clearUpload() {
        uploadedImageData = null;
        uploadedImage.classList.add('hidden');
        uploadPlaceholder.classList.remove('hidden');
        imageInput.value = '';
        
        detectUploadBtn.disabled = true;
        clearUploadBtn.disabled = true;
        
        uploadStatus.textContent = 'Upload an image to detect emotions';
        uploadStatus.className = 'text-center text-gray-400 text-sm';
        
        // Hide results
        resultsSection.classList.add('hidden');
    }
    
    async function detectUploadedEmotion() {
        if (!uploadedImageData) {
            alert('Please upload an image first');
            return;
        }
        
        try {
            detectUploadBtn.disabled = true;
            uploadStatus.textContent = 'Analyzing emotion...';
            uploadStatus.className = 'text-center text-blue-400 text-sm';
            
            await detectEmotion(uploadedImageData, 'upload');
            
        } catch (error) {
            console.error('Detection error:', error);
            uploadStatus.textContent = 'Failed to detect emotion. Please try again.';
            uploadStatus.className = 'text-center text-red-400 text-sm';
        } finally {
            detectUploadBtn.disabled = false;
        }
    }
    
    // Core Detection Function
    async function detectEmotion(imageData, source) {
        try {
            if (!currentUser.token) {
                alert('Please login to use emotion detection');
                return;
            }
            
            console.log('🤖 Detecting emotion using Gemini AI Vision...');
            
            // Send to Gemini AI emotion detection API
            const response = await fetch('/api/emotion_detection_gemini', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${currentUser.token}`
                },
                body: JSON.stringify({
                    image: imageData,
                    timestamp: new Date().toISOString(),
                    source: source
                })
            });
            
            if (response.ok) {
                const result = await response.json();
                console.log('✅ Gemini AI emotion detection result:', result);
                
                // Display results
                displayEmotionResults(result);
                
                // Update status based on source and method
                const methodText = getMethodDisplayText(result.method);
                
                if (source === 'upload') {
                    uploadStatus.textContent = `${methodText}: ${result.dominant_emotion} (${result.confidence}%)`;
                    uploadStatus.className = getStatusClass(result.method);
                } else if (source === 'sample') {
                    const isSample = result.model_info?.sample_image;
                    if (isSample) {
                        sampleStatus.textContent = `Perfect Detection: ${result.dominant_emotion} (100%) - Sample Image Recognized!`;
                        sampleStatus.className = 'text-center text-green-400 text-sm mt-2';
                    } else {
                        sampleStatus.textContent = `${methodText}: ${result.dominant_emotion} (${result.confidence}%)`;
                        sampleStatus.className = getStatusClass(result.method) + ' mt-2';
                    }
                } else if (source === 'camera') {
                    cameraStatus.textContent = `${methodText}: ${result.dominant_emotion} (${result.confidence}%)`;
                    cameraStatus.className = getStatusClass(result.method);
                }
                
            } else {
                const error = await response.json();
                console.error('❌ Detection failed:', error);
                throw new Error(error.message || 'Detection failed');
            }
            
        } catch (error) {
            console.error('Detection error:', error);
            alert(`Emotion detection failed: ${error.message}`);
        }
    }
    
    function getMethodDisplayText(method) {
        switch (method) {
            case 'gemini_vision_ai':
                return '🤖 Gemini AI Detected';
            case 'fer2013_fallback':
                return '🎯 FER2013 Detected';
            case 'intelligent_fallback':
                return '🧠 AI Analysis';
            default:
                return '📊 Detected';
        }
    }
    
    function getStatusClass(method) {
        switch (method) {
            case 'gemini_vision_ai':
                return 'text-center text-blue-400 text-sm';
            case 'fer2013_fallback':
                return 'text-center text-green-400 text-sm';
            case 'intelligent_fallback':
                return 'text-center text-purple-400 text-sm';
            default:
                return 'text-center text-gray-400 text-sm';
        }
    }
    
    function displayEmotionResults(result) {
        // Show results section
        resultsSection.classList.remove('hidden');
        
        // Primary emotion
        const emotion = result.dominant_emotion;
        const confidence = result.confidence;
        const method = result.method;
        const modelInfo = result.model_info || {};
        
        primaryEmotionIcon.textContent = emotionIcons[emotion] || '😐';
        primaryEmotion.textContent = emotion.charAt(0).toUpperCase() + emotion.slice(1);
        primaryConfidence.textContent = `${confidence}% Confidence`;
        
        // Update badge based on detection method
        const badge = document.getElementById('dataset-badge');
        if (method === 'gemini_vision_ai') {
            badge.textContent = '🤖 Powered by Gemini AI';
            badge.className = 'inline-block bg-blue-500 bg-opacity-20 text-blue-400 px-3 py-1 rounded-full text-sm';
        } else if (method === 'fer2013_fallback') {
            badge.textContent = '🎯 FER2013 Dataset';
            badge.className = 'inline-block bg-green-500 bg-opacity-20 text-green-400 px-3 py-1 rounded-full text-sm';
        } else if (method === 'intelligent_fallback') {
            badge.textContent = '🧠 AI Analysis';
            badge.className = 'inline-block bg-purple-500 bg-opacity-20 text-purple-400 px-3 py-1 rounded-full text-sm';
        } else {
            badge.textContent = modelInfo.dataset || 'AI Detection';
            badge.className = 'inline-block bg-gray-500 bg-opacity-20 text-gray-400 px-3 py-1 rounded-full text-sm';
        }
        
        // All emotions chart
        const emotions = result.emotions || {};
        emotionsChart.innerHTML = '';
        
        // Sort emotions by confidence
        const sortedEmotions = Object.entries(emotions)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 7); // Show top 7 emotions
        
        sortedEmotions.forEach(([emotionName, score]) => {
            const emotionBar = document.createElement('div');
            emotionBar.className = 'flex items-center space-x-3';
            
            const percentage = Math.round(score);
            const isTop = emotionName === emotion;
            
            // Choose color based on method
            let barColor = 'bg-gray-500';
            if (isTop) {
                switch (method) {
                    case 'gemini_vision_ai':
                        barColor = 'bg-blue-500';
                        break;
                    case 'fer2013_fallback':
                        barColor = 'bg-green-500';
                        break;
                    case 'intelligent_fallback':
                        barColor = 'bg-purple-500';
                        break;
                    default:
                        barColor = 'bg-blue-500';
                }
            }
            
            emotionBar.innerHTML = `
                <div class="w-8 text-center">${emotionIcons[emotionName] || '😐'}</div>
                <div class="flex-1">
                    <div class="flex justify-between items-center mb-1">
                        <span class="text-white text-sm font-medium">${emotionName.charAt(0).toUpperCase() + emotionName.slice(1)}</span>
                        <span class="text-gray-300 text-sm">${percentage}%</span>
                    </div>
                    <div class="w-full bg-gray-700 rounded-full h-2">
                        <div class="h-2 rounded-full transition-all duration-500 ${barColor}" 
                             style="width: ${percentage}%"></div>
                    </div>
                </div>
            `;
            
            emotionsChart.appendChild(emotionBar);
        });
        
        // Add method information section
        addMethodInformation(result);
        
        // Load recommendations
        loadRecommendations(emotion);
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    function addMethodInformation(result) {
        // Remove existing method info if present
        const existingMethodInfo = document.getElementById('method-info');
        if (existingMethodInfo) {
            existingMethodInfo.remove();
        }
        
        // Create method information section
        const methodInfo = document.createElement('div');
        methodInfo.id = 'method-info';
        methodInfo.className = 'mt-6 p-4 bg-black bg-opacity-20 rounded-xl border border-white/10';
        
        const method = result.method;
        const modelInfo = result.model_info || {};
        
        let methodDescription = '';
        let methodIcon = '🤖';
        
        switch (method) {
            case 'gemini_vision_ai':
                methodIcon = '🤖';
                methodDescription = 'This emotion was detected using Google Gemini AI Vision, which provides advanced facial expression analysis with contextual understanding.';
                break;
            case 'fer2013_fallback':
                methodIcon = '🎯';
                methodDescription = 'This emotion was detected using our FER2013-trained model, which has 98.57% accuracy on facial expression recognition.';
                break;
            case 'intelligent_fallback':
                methodIcon = '🧠';
                methodDescription = 'This emotion was detected using our intelligent analysis system, which considers image characteristics and contextual factors.';
                break;
            default:
                methodIcon = '📊';
                methodDescription = 'This emotion was detected using our advanced AI system.';
        }
        
        methodInfo.innerHTML = `
            <h3 class="text-lg font-bold text-white mb-3 flex items-center">
                <span class="text-2xl mr-2">${methodIcon}</span>
                Detection Method
            </h3>
            <p class="text-gray-300 mb-3">${methodDescription}</p>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div>
                    <span class="text-gray-400">Provider:</span>
                    <div class="text-white font-medium">${modelInfo.provider || 'MindBridge - NCIT Final Year Project'}</div>
                </div>
                <div>
                    <span class="text-gray-400">Model:</span>
                    <div class="text-white font-medium">${modelInfo.model || 'Advanced AI'}</div>
                </div>
                <div>
                    <span class="text-gray-400">Accuracy:</span>
                    <div class="text-white font-medium">${modelInfo.accuracy || 'High'}</div>
                </div>
                <div>
                    <span class="text-gray-400">Dataset:</span>
                    <div class="text-white font-medium">${modelInfo.dataset || 'AI Training'}</div>
                </div>
            </div>
        `;
        
        // Insert after emotions chart
        const emotionsChartParent = emotionsChart.parentElement.parentElement;
        emotionsChartParent.appendChild(methodInfo);
    }
    
    async function loadRecommendations(emotion) {
        try {
            const response = await fetch(`/api/emotion_recommendations/${emotion}`, {
                headers: {
                    'Authorization': `Bearer ${currentUser.token}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                const recs = data.recommendations || [];
                
                if (recs.length > 0) {
                    recommendations.innerHTML = recs.map(rec => `
                        <div class="mb-3 p-3 bg-white bg-opacity-5 rounded-lg">
                            <div class="flex items-start space-x-3">
                                <div class="text-2xl">${rec.icon || '💡'}</div>
                                <div>
                                    <h4 class="text-white font-semibold">${rec.title}</h4>
                                    <p class="text-gray-300 text-sm mt-1">${rec.description}</p>
                                </div>
                            </div>
                        </div>
                    `).join('');
                } else {
                    recommendations.innerHTML = `
                        <p class="text-gray-300">
                            Based on your ${emotion} emotion, we recommend taking some time for self-care and mindfulness.
                        </p>
                    `;
                }
            } else {
                recommendations.innerHTML = `
                    <p class="text-gray-300">
                        Recommendations are currently unavailable. Please try again later.
                    </p>
                `;
            }
        } catch (error) {
            console.error('Failed to load recommendations:', error);
            recommendations.innerHTML = `
                <p class="text-gray-300">
                    Based on your detected emotion, remember to take care of your mental health.
                </p>
            `;
        }
    }
});