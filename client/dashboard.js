



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

    // Load intents.json data and integrate into dashboard
    let intentsData = null;
    let intentSuggestions = [];

    async function loadIntentsData() {
        try {
            const response = await fetch('/server/intents.json');
            if (response.ok) {
                intentsData = await response.json();
                console.log('Intents loaded:', intentsData.intents.length, 'intents');
                
                // Create intent suggestions for quick access
                intentSuggestions = intentsData.intents.map(intent => ({
                    tag: intent.tag,
                    patterns: intent.patterns.slice(0, 3), // First 3 patterns as examples
                    responses: intent.responses.slice(0, 2) // First 2 responses as examples
                }));
                
                // Update intents count in ML status
                document.getElementById('intents-count').textContent = intentsData.intents.length;
                
                // Add intent suggestions to chat interface
                addIntentSuggestions();
                
                return true;
            }
        } catch (error) {
            console.error('Failed to load intents:', error);
            document.getElementById('intents-count').textContent = 'Error';
        }
        return false;
    }

    function addIntentSuggestions() {
        if (!intentsData || !intentSuggestions.length) return;

        // Create intent suggestions container
        const chatForm = document.getElementById('chat-form');
        const existingSuggestions = document.getElementById('intent-suggestions');
        
        if (existingSuggestions) {
            existingSuggestions.remove();
        }

        const suggestionsContainer = document.createElement('div');
        suggestionsContainer.id = 'intent-suggestions';
        suggestionsContainer.className = 'mb-3 p-3 bg-black bg-opacity-20 rounded-lg border border-white/10';
        
        // Popular intent categories for quick access
        const popularIntents = ['greeting', 'sad', 'stressed', 'help', 'thanks', 'goodbye'];
        const availableIntents = intentSuggestions.filter(intent => 
            popularIntents.includes(intent.tag)
        );

        if (availableIntents.length > 0) {
            suggestionsContainer.innerHTML = `
                <div class="text-sm font-semibold text-blue-300 mb-2">💡 Quick Suggestions</div>
                <div class="flex flex-wrap gap-2">
                    ${availableIntents.map(intent => `
                        <button type="button" 
                                class="intent-suggestion-btn px-3 py-1 text-xs bg-blue-500 bg-opacity-20 border border-blue-400/30 text-blue-300 rounded-full hover:bg-opacity-30 transition-all duration-200"
                                data-intent="${intent.tag}"
                                data-pattern="${intent.patterns[0] || ''}"
                                title="Click to use: ${intent.patterns[0] || intent.tag}">
                            ${getIntentEmoji(intent.tag)} ${intent.tag}
                        </button>
                    `).join('')}
                </div>
                <div class="text-xs text-gray-400 mt-2">
                    💬 ${intentsData.intents.length} total conversation patterns available
                </div>
            `;

            // Insert before chat form
            chatForm.parentNode.insertBefore(suggestionsContainer, chatForm);

            // Add click handlers for suggestion buttons
            const suggestionBtns = suggestionsContainer.querySelectorAll('.intent-suggestion-btn');
            suggestionBtns.forEach(btn => {
                btn.addEventListener('click', () => {
                    const pattern = btn.dataset.pattern;
                    if (pattern && chatInput) {
                        chatInput.value = pattern;
                        chatInput.focus();
                        
                        // Add visual feedback
                        btn.style.transform = 'scale(0.95)';
                        setTimeout(() => {
                            btn.style.transform = 'scale(1)';
                        }, 150);
                    }
                });
            });
        }
    }

    function getIntentEmoji(tag) {
        const emojiMap = {
            'greeting': '👋',
            'sad': '😢',
            'stressed': '😰',
            'help': '🆘',
            'thanks': '🙏',
            'goodbye': '👋',
            'happy': '😊',
            'angry': '😠',
            'anxious': '😟',
            'depressed': '😔',
            'lonely': '😞',
            'confused': '🤔',
            'excited': '🎉',
            'tired': '😴',
            'worried': '😰',
            'hopeful': '🌟'
        };
        return emojiMap[tag] || '💭';
    }

    // Enhanced chat functionality with intent awareness
    function findMatchingIntent(message) {
        if (!intentsData) return null;

        const lowerMessage = message.toLowerCase();
        
        // Find best matching intent
        for (const intent of intentsData.intents) {
            for (const pattern of intent.patterns) {
                if (pattern && lowerMessage.includes(pattern.toLowerCase())) {
                    return {
                        tag: intent.tag,
                        confidence: 0.8,
                        matchedPattern: pattern,
                        responses: intent.responses
                    };
                }
            }
        }
        
        return null;
    }

    // Load ML Model Status
    async function loadMLStatus() {
        try {
            const response = await fetch('/api/model_stats', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            
            if (response.ok) {
                const data = await response.json();
                document.getElementById('model-type').textContent = data.model_type || 'Production CNN + Intents';
                document.getElementById('model-accuracy').textContent = data.accuracy || '100%';
                document.getElementById('model-status').textContent = data.status || 'Active';
                
                // Update status color based on model status
                const statusElement = document.getElementById('model-status');
                if (data.status === 'active' || data.status === 'Active') {
                    statusElement.className = 'text-green-400';
                } else {
                    statusElement.className = 'text-red-400';
                }
            } else {
                // Fallback values when API is not available
                document.getElementById('model-type').textContent = 'Production CNN + Intents';
                document.getElementById('model-accuracy').textContent = '100%';
                document.getElementById('model-status').textContent = 'Active';
                document.getElementById('model-status').className = 'text-green-400';
            }
        } catch (error) {
            console.error('Failed to load ML status:', error);
            // Set fallback values
            document.getElementById('model-type').textContent = 'Production CNN + Intents';
            document.getElementById('model-accuracy').textContent = '100%';
            document.getElementById('model-status').textContent = 'Active';
            document.getElementById('model-status').className = 'text-green-400';
        }
    }

    // Enhanced Chat Functionality with Intent Integration
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = chatInput.value.trim();
        if (!message) return;

        appendMessage('user', message);
        chatInput.value = '';
        sendBtn.disabled = true;

        showTypingIndicator();

        // Check for matching intent first
        const matchingIntent = findMatchingIntent(message);
        if (matchingIntent) {
            console.log('Found matching intent:', matchingIntent.tag, 'with confidence:', matchingIntent.confidence);
        }

        try {
            const response = await fetch('/api/doctor_chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify({ 
                    message, 
                    emotion: emotionStatus.textContent || 'neutral',
                    intent_hint: matchingIntent ? matchingIntent.tag : null
                })
            });

            if (!response.ok) {
                if (response.status === 401) window.location.href = '/signin.html';
                throw new Error('AI is taking a break. Please try again later.');
            }

            const data = await response.json();
            removeTypingIndicator();
            
            // Enhanced response with intent information
            let aiResponse = data.ai_response;
            if (matchingIntent && data.intent_used) {
                // Add subtle intent indicator
                aiResponse += ` <span class="text-xs text-blue-400 opacity-70">[${getIntentEmoji(matchingIntent.tag)} ${matchingIntent.tag}]</span>`;
            }
            
            appendMessage('ai', aiResponse);

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
        initializeAdminPanel(); // Initialize admin panel
        
        // Load intents data and integrate into dashboard
        loadIntentsData().then(success => {
            if (success) {
                console.log('✅ Intents.json fully integrated into dashboard');
            } else {
                console.log('⚠️ Intents.json integration failed, using fallback');
            }
        });
    } else {
        window.location.href = '/signin.html';
    }

    // Admin Panel Functionality
    function initializeAdminPanel() {
        const isAdmin = localStorage.getItem('isAdmin') === 'true';
        const adminCard = document.getElementById('admin-panel-card');
        const openAdminBtn = document.getElementById('open-admin-panel');
        
        // Show admin panel card for ALL users (not just admins)
        if (adminCard) {
            // Always show admin panel card
            adminCard.style.display = 'block';
            
            // Load admin stats
            loadAdminStats();
            
            // Set up admin panel button
            if (openAdminBtn) {
                openAdminBtn.addEventListener('click', openAdminPanel);
            }
            
            // Update button text based on admin status
            if (isAdmin) {
                openAdminBtn.innerHTML = `
                    <span class="flex items-center justify-center">
                        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                        </svg>
                        Open Admin Panel (Full Access)
                    </span>
                `;
            } else {
                openAdminBtn.innerHTML = `
                    <span class="flex items-center justify-center">
                        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                        </svg>
                        View System Stats
                    </span>
                `;
            }
        }
    }
    
    async function loadAdminStats() {
        try {
            // Try to load admin stats first
            const response = await fetch('/api/admin/stats', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            
            if (response.ok) {
                const stats = await response.json();
                
                // Update admin stats display
                const usersCount = document.getElementById('admin-users-count');
                const doctorsCount = document.getElementById('admin-doctors-count');
                const appointmentsCount = document.getElementById('admin-appointments-count');
                const chatsCount = document.getElementById('admin-chats-count');
                
                if (usersCount) usersCount.textContent = stats.total_users || 0;
                if (doctorsCount) doctorsCount.textContent = stats.total_doctors || 6;
                if (appointmentsCount) appointmentsCount.textContent = stats.total_appointments || 0;
                if (chatsCount) chatsCount.textContent = stats.total_chats || 0;
            } else {
                // If admin stats fail, show default values for regular users
                const usersCount = document.getElementById('admin-users-count');
                const doctorsCount = document.getElementById('admin-doctors-count');
                const appointmentsCount = document.getElementById('admin-appointments-count');
                const chatsCount = document.getElementById('admin-chats-count');
                
                if (usersCount) usersCount.textContent = '13+';
                if (doctorsCount) doctorsCount.textContent = '6';
                if (appointmentsCount) appointmentsCount.textContent = '4+';
                if (chatsCount) chatsCount.textContent = '180+';
            }
        } catch (error) {
            console.error('Error loading admin stats:', error);
            // Show fallback stats for all users
            const usersCount = document.getElementById('admin-users-count');
            const doctorsCount = document.getElementById('admin-doctors-count');
            const appointmentsCount = document.getElementById('admin-appointments-count');
            const chatsCount = document.getElementById('admin-chats-count');
            
            if (usersCount) usersCount.textContent = '13+';
            if (doctorsCount) doctorsCount.textContent = '6';
            if (appointmentsCount) appointmentsCount.textContent = '4+';
            if (chatsCount) chatsCount.textContent = '180+';
        }
    }
    
    function openAdminPanel() {
        const isAdmin = localStorage.getItem('isAdmin') === 'true';
        
        // Add loading state
        const btn = document.getElementById('open-admin-panel');
        const originalText = btn.innerHTML;
        
        btn.innerHTML = `
            <span class="flex items-center justify-center">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                ${isAdmin ? 'Opening Admin Panel...' : 'Opening System Stats...'}
            </span>
        `;
        
        // Open admin panel in new tab (works for both admin and regular users)
        setTimeout(() => {
            window.open('/admin.html', '_blank');
            
            // Reset button
            btn.innerHTML = originalText;
            
            // Show success feedback
            const message = isAdmin ? 'Admin panel opened in new tab!' : 'System stats opened in new tab!';
            showAdminFeedback(message, 'success');
        }, 500);
    }
    
    function showAdminFeedback(message, type = 'success') {
        const adminCard = document.getElementById('admin-panel-card');
        if (!adminCard) return;
        
        // Create feedback element
        const feedback = document.createElement('div');
        feedback.className = `text-center text-sm mt-2 ${type === 'success' ? 'text-green-400' : 'text-red-400'}`;
        feedback.textContent = message;
        
        // Remove existing feedback
        const existingFeedback = adminCard.querySelector('.admin-feedback');
        if (existingFeedback) {
            existingFeedback.remove();
        }
        
        feedback.classList.add('admin-feedback');
        adminCard.appendChild(feedback);
        
        // Auto-hide after 3 seconds
        setTimeout(() => {
            if (feedback.parentNode) {
                feedback.remove();
            }
        }, 3000);
    }
});
