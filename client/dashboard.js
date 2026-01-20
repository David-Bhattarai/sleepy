document.addEventListener('DOMContentLoaded', async () => {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const sendBtn = document.getElementById('send-btn');
    const emotionStatus = document.getElementById('emotion-status');
    const video = document.getElementById('video');
    const token = localStorage.getItem('token');

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
    } else {
        window.location.href = '/signin.html';
    }
});
