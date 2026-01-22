document.addEventListener('DOMContentLoaded', async () => {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const sendBtn = document.getElementById('send-btn');
    const emotionStatus = document.getElementById('emotion-status');
    const video = document.getElementById('video');
    const token = localStorage.getItem('token');

    // Mood Tracking Variables
    let selectedMood = 3; // Default mood
    const moodButtons = document.querySelectorAll('.mood-btn-dash');
    const quickMoodNotes = document.getElementById('quick-mood-notes');
    const saveMoodBtn = document.getElementById('save-mood-btn');
    const dashMoodFeedback = document.getElementById('dash-mood-feedback');
    const simpleMoodChart = document.getElementById('simple-mood-chart');
    const viewMoreMoodsBtn = document.getElementById('view-more-moods');

    // Initialize Mood Tracking
    function initializeMoodTracking() {
        // Set up mood button selection
        moodButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                selectDashboardMood(parseInt(button.dataset.mood));
            });
        });

        // Set up save mood button
        if (saveMoodBtn) {
            saveMoodBtn.addEventListener('click', saveDashboardMood);
        }

        // Set up view more moods button
        if (viewMoreMoodsBtn) {
            viewMoreMoodsBtn.addEventListener('click', () => {
                window.open('/simple-mood-tracker.html', '_blank');
            });
        }

        // Load mood stats and chart
        loadDashboardMoodStats();
        loadSimpleMoodChart();
    }

    function selectDashboardMood(moodValue) {
        selectedMood = moodValue;
        
        // Update button selection
        moodButtons.forEach(btn => {
            btn.classList.remove('selected');
        });
        
        const selectedButton = document.querySelector(`[data-mood="${moodValue}"]`);
        if (selectedButton) {
            selectedButton.classList.add('selected');
        }
    }

    async function saveDashboardMood() {
        if (!token) return;

        const moodData = {
            mood_rating: selectedMood,
            mood_notes: quickMoodNotes ? quickMoodNotes.value.trim() : ''
        };

        try {
            saveMoodBtn.disabled = true;
            saveMoodBtn.textContent = 'Saving...';

            const response = await fetch('/api/mood_simple', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(moodData)
            });

            if (!response.ok) {
                throw new Error('Failed to save mood');
            }

            const result = await response.json();

            if (result.success) {
                // Show success feedback
                const moodInfo = result.mood_info;
                showDashboardMoodFeedback(`${moodInfo.emoji} Saved!`, 'success');
                
                // Clear notes
                if (quickMoodNotes) quickMoodNotes.value = '';
                
                // Reset to default mood
                selectDashboardMood(3);
                
                // Reload stats and chart with animation
                showDashboardMoodFeedback('📊 Updating chart...', 'info');
                await loadDashboardMoodStats();
                await loadSimpleMoodChart();
                
                // Show completion
                setTimeout(() => {
                    showDashboardMoodFeedback('✅ Chart updated!', 'success');
                }, 500);
                
            } else {
                throw new Error(result.message || 'Failed to save mood');
            }

        } catch (error) {
            console.error('Error saving mood:', error);
            showDashboardMoodFeedback('Error saving mood', 'error');
        } finally {
            saveMoodBtn.disabled = false;
            saveMoodBtn.textContent = 'Save Mood';
        }
    }

    async function loadDashboardMoodStats() {
        if (!token) return;

        try {
            const response = await fetch('/api/mood_simple/stats?days=30', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) return;

            const stats = await response.json();

            // Update dashboard stats
            const totalElement = document.getElementById('dash-total-entries');
            const avgElement = document.getElementById('dash-avg-mood');

            if (totalElement) totalElement.textContent = stats.total_entries || 0;
            if (avgElement) avgElement.textContent = stats.average_mood || '0';

        } catch (error) {
            console.error('Error loading mood stats:', error);
        }
    }

    async function loadSimpleMoodChart() {
        if (!token || !simpleMoodChart) return;

        try {
            const response = await fetch('/api/mood_simple/chart?days=7', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) return;

            const chartData = await response.json();

            // Update simple chart
            updateSimpleMoodChart(chartData);

        } catch (error) {
            console.error('Error loading mood chart:', error);
        }
    }

    function updateSimpleMoodChart(chartData) {
        if (!simpleMoodChart) return;

        const labels = chartData.labels || [];
        const data = chartData.data || [];

        if (data.length === 0) {
            simpleMoodChart.innerHTML = '<div class="text-center text-gray-400 py-8">Save some moods to see your chart!</div>';
            return;
        }

        // Create simple visual chart
        let chartHTML = '<div class="simple-chart">';
        
        for (let i = 0; i < Math.min(labels.length, 7); i++) {
            const mood = data[i];
            const label = labels[i];
            const height = (mood / 5) * 80; // Scale to max 80px height
            const isNewest = i === data.length - 1; // Check if this is the newest entry
            
            // Get emoji for mood
            const emojis = ['', '😭', '😟', '😐', '🙂', '😊'];
            const emoji = emojis[mood] || '😐';
            
            // Add special styling for newest entry
            const newClass = isNewest ? ' style="box-shadow: 0 0 10px rgba(59, 130, 246, 0.5); border: 2px solid #3b82f6;"' : '';
            
            chartHTML += `
                <div class="chart-bar">
                    <div class="chart-emoji">${emoji}</div>
                    <div class="chart-bar-fill mood-${mood}"${newClass} style="height: ${height}px;"></div>
                    <div class="chart-date">${label}</div>
                </div>
            `;
        }
        
        chartHTML += '</div>';
        
        // Add simple legend
        chartHTML += `
            <div class="flex justify-center mt-3 space-x-4 text-xs text-gray-400">
                <span>😭 Very Bad</span>
                <span>😟 Bad</span>
                <span>😐 Okay</span>
                <span>🙂 Good</span>
                <span>😊 Great</span>
            </div>
        `;
        
        // Add update indicator
        if (data.length > 0) {
            chartHTML += `
                <div class="text-center mt-2 text-xs text-blue-400">
                    📊 Last updated: ${new Date().toLocaleTimeString()}
                </div>
            `;
        }
        
        simpleMoodChart.innerHTML = chartHTML;

        // Generate recommendations based on chart data
        generateSimpleMoodRecommendations(data);
    }

    function generateSimpleMoodRecommendations(moodData) {
        const recommendationElement = document.getElementById('recommendation-text');
        if (!recommendationElement || moodData.length === 0) {
            return;
        }

        // Calculate simple statistics
        const avgMood = moodData.reduce((sum, mood) => sum + mood, 0) / moodData.length;
        const lastMood = moodData[moodData.length - 1];
        
        let recommendation = '';
        let emoji = '';

        // Simple recommendations based on average mood
        if (avgMood >= 4.5) {
            emoji = '🌟';
            recommendation = 'Wow! You\'re doing amazing! Keep spreading that positive energy!';
        } else if (avgMood >= 4.0) {
            emoji = '😊';
            recommendation = 'You\'re in a great mood! Keep doing what makes you happy!';
        } else if (avgMood >= 3.5) {
            emoji = '🙂';
            recommendation = 'You\'re doing well! Maybe try something fun today to boost your mood even more.';
        } else if (avgMood >= 2.5) {
            emoji = '😐';
            recommendation = 'Your mood is okay. Try listening to music, going for a walk, or calling a friend.';
        } else if (avgMood >= 2.0) {
            emoji = '😟';
            recommendation = 'You seem to be having some tough days. Take care of yourself and reach out if you need support.';
        } else {
            emoji = '💙';
            recommendation = 'It looks like you\'re going through a difficult time. Please talk to someone you trust.';
        }

        // Add trend info
        if (moodData.length >= 2) {
            const firstMood = moodData[0];
            if (lastMood > firstMood) {
                recommendation += ' Good news - your mood is getting better! 📈';
            } else if (lastMood < firstMood) {
                recommendation += ' Take extra care of yourself today. 💚';
            }
        }

        recommendationElement.innerHTML = `${emoji} ${recommendation}`;
    }

    function showDashboardMoodFeedback(message, type = 'success') {
        if (!dashMoodFeedback) return;

        const typeClasses = {
            success: 'text-green-400',
            error: 'text-red-400',
            warning: 'text-yellow-400'
        };

        dashMoodFeedback.className = `text-center text-sm mt-2 ${typeClasses[type] || typeClasses.success}`;
        dashMoodFeedback.textContent = message;

        // Auto-hide after 3 seconds
        setTimeout(() => {
            dashMoodFeedback.textContent = '';
        }, 3000);
    }

    // Load ML Model Status
    async function loadMLStatus() {
        try {
            const response = await fetch('/api/model_stats', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            
            if (response.ok) {
                const data = await response.json();
                document.getElementById('model-type').textContent = data.model_type || 'Unknown';
                document.getElementById('model-accuracy').textContent = data.accuracy || 'Unknown';
                document.getElementById('intents-count').textContent = data.intents_count || '0';
                document.getElementById('model-status').textContent = data.status || 'Unknown';
                
                // Update status color based on model status
                const statusElement = document.getElementById('model-status');
                if (data.status === 'active') {
                    statusElement.className = 'text-green-400';
                } else {
                    statusElement.className = 'text-red-400';
                }
            }
        } catch (error) {
            console.error('Failed to load ML status:', error);
            document.getElementById('model-type').textContent = 'Error';
            document.getElementById('model-accuracy').textContent = 'Error';
            document.getElementById('intents-count').textContent = 'Error';
            document.getElementById('model-status').textContent = 'Error';
        }
    }

    // Chat Functionality
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = chatInput.value.trim();
        if (!message) return;

        appendMessage('user', message);
        chatInput.value = '';
        sendBtn.disabled = true;

        showTypingIndicator();

        try {
            const response = await fetch('/api/doctor_chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify({ message, emotion: emotionStatus.textContent || 'neutral' })
            });

            if (!response.ok) {
                if (response.status === 401) window.location.href = '/signin.html';
                throw new Error('AI is taking a break. Please try again later.');
            }

            const data = await response.json();
            removeTypingIndicator();
            appendMessage('ai', data.ai_response);

        } catch (error) {
            removeTypingIndicator();
            appendMessage('ai', error.message);
        } finally {
            sendBtn.disabled = false;
        }
    });

    function appendMessage(sender, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `flex justify-${sender === 'user' ? 'end' : 'start'}`;
        msgDiv.innerHTML = `<div class="chat-message-${sender} max-w-lg p-4"><p>${text}</p></div>`;
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.id = 'typing-indicator';
        typingDiv.className = 'flex justify-start';
        typingDiv.innerHTML = `
            <div class="chat-message-ai max-w-lg p-4">
                <div class="typing-indicator">
                    <span></span><span></span><span></span>
                </div>
            </div>
        `;
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) indicator.remove();
    }

    // Emotion Detection
    async function startEmotionDetection() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
            emotionStatus.textContent = 'Analyzing...';

            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');

            setInterval(async () => {
                if (video.readyState < 2) return; 
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                const dataUrl = canvas.toDataURL('image/jpeg', 0.8);

                try {
                    const response = await fetch('/api/detect_emotion', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                        body: JSON.stringify({ image: dataUrl })
                    });
                    if (!response.ok) return;
                    const data = await response.json();
                    emotionStatus.textContent = data.emotion;
                } catch (e) { /* silent fail */ }
            }, 2500);

        } catch (error) {
            emotionStatus.innerHTML = 'Camera access denied. <br/> Please enable camera.';
            video.parentElement.style.display = 'none';
        }
    }

    if (token) {
        startEmotionDetection();
        loadMLStatus();
        initializeMoodTracking(); // Initialize mood tracking
    } else {
        window.location.href = '/signin.html';
    }
});
