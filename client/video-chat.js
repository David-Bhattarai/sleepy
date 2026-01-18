document.addEventListener('DOMContentLoaded', async () => {
    const authCheck = document.getElementById('auth-check');
    const videoChatUI = document.getElementById('video-chat-ui');
    const userVideo = document.getElementById('user-video');
    const userVideoContainer = document.getElementById('user-video-container');
    const emotionDisplay = document.getElementById('emotion-display');
    const chatWindow = document.getElementById('chat-window');
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const typingIndicatorContainer = document.getElementById('typing-indicator-container');

    // --- Draggable Video --- //
    let isDragging = false;
    let offset = { x: 0, y: 0 };

    userVideoContainer.addEventListener('mousedown', (e) => {
        isDragging = true;
        offset.x = e.clientX - userVideoContainer.offsetLeft;
        offset.y = e.clientY - userVideoContainer.offsetTop;
        userVideoContainer.style.cursor = 'grabbing';
    });

    document.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        userVideoContainer.style.left = `${e.clientX - offset.x}px`;
        userVideoContainer.style.top = `${e.clientY - offset.y}px`;
    });

    document.addEventListener('mouseup', () => {
        isDragging = false;
        userVideoContainer.style.cursor = 'move';
    });

    // --- Authentication and Camera Activation --- //
    try {
        const response = await fetch('/api/user_status');
        if (!response.ok) {
            window.location.href = 'signin.html';
            return;
        }

        const status = await response.json();
        if (!status.is_premium) {
            alert('This is a premium feature. Please subscribe to get access.');
            window.location.href = 'premium.html';
            return;
        }

        authCheck.classList.add('hidden');
        videoChatUI.classList.remove('hidden');

        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            userVideo.srcObject = stream;
            startEmotionDetection(stream);
        } else {
            addMessageToUI("Your browser does not support video streaming.", 'system');
        }

    } catch (error) {
        console.error('Auth check failed:', error);
        window.location.href = 'signin.html';
    }

    // --- Emotion Detection --- //
    const startEmotionDetection = (stream) => {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        const track = stream.getVideoTracks()[0];
        const imageCapture = new ImageCapture(track);

        setInterval(async () => {
            if (document.hidden) return;
            try {
                const imageBitmap = await imageCapture.grabFrame();
                canvas.width = imageBitmap.width;
                canvas.height = imageBitmap.height;
                context.drawImage(imageBitmap, 0, 0);
                const dataUrl = canvas.toDataURL('image/jpeg', 0.8);

                const response = await fetch('/api/detect_emotion', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image: dataUrl }),
                });

                if (response.ok) {
                    const data = await response.json();
                    if (data.emotion) {
                        emotionDisplay.textContent = `Emotion: ${data.emotion}`;
                    }
                } else {
                    emotionDisplay.textContent = "Emotion: Error";
                }
            } catch (error) {
                console.error('Emotion detection error:', error);
                emotionDisplay.textContent = "Emotion: Disconnected";
            }
        }, 4000); // Analyze frame every 4 seconds
    };

    // --- Chat Management --- //
    const showTypingIndicator = () => {
        typingIndicatorContainer.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
    };

    const hideTypingIndicator = () => {
        typingIndicatorContainer.innerHTML = '';
    };

    const sendMessage = async () => {
        const message = chatInput.value.trim();
        if (!message) return;

        addMessageToUI(message, 'user');
        chatInput.value = '';
        showTypingIndicator();

        try {
            const response = await fetch('/api/doctor_chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message }),
            });

            hideTypingIndicator();
            if (!response.ok) throw new Error('Network response was not ok.');

            const data = await response.json();
            addMessageToUI(data.ai_response, 'ai');

        } catch (error) {
            hideTypingIndicator();
            console.error('Chat error:', error);
            addMessageToUI("Sorry, I'm having trouble connecting. Please try again.", 'system');
        }
    };

    const addMessageToUI = (message, sender) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('mb-3', 'p-3', 'rounded-lg', 'max-w-xs', 'transition-opacity', 'duration-500');
        messageElement.style.opacity = 0;

        if (sender === 'user') {
            messageElement.classList.add('bg-blue-600', 'text-white', 'ml-auto');
        } else if (sender === 'ai') {
            messageElement.classList.add('bg-gray-700', 'text-gray-200', 'mr-auto');
        } else { // System messages
            messageElement.classList.add('bg-red-500', 'text-white', 'text-center', 'max-w-full');
        }
        
        messageElement.textContent = message;
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;
        setTimeout(() => messageElement.style.opacity = 1, 10);
    };

    sendButton.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});