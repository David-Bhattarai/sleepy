// MindBridge - NCIT Final Year Project Chatbot JavaScript
class MindBridgeChatbot {
    constructor() {
        this.messageCount = 1; // Start with 1 for welcome message
        this.sessionStart = new Date();
        this.currentEmotion = 'neutral';
        this.intentSuggestions = [
            'I feel anxious',
            'I need someone to talk to',
            'I\'m feeling depressed',
            'Help with stress',
            'I can\'t sleep',
            'Relationship problems',
            'Work stress',
            'Self-care tips'
        ];
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.updateSessionDuration();
        this.loadIntentSuggestions();
        this.loadIntentCategories();
        
        // Update duration every minute
        setInterval(() => this.updateSessionDuration(), 60000);
    }
    
    setupEventListeners() {
        const chatInput = document.getElementById('chat-input');
        const sendBtn = document.getElementById('send-btn');
        
        // Send message on button click
        sendBtn.addEventListener('click', () => this.sendMessage());
        
        // Send message on Enter key
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        
        // Intent suggestion clicks
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('intent-chip')) {
                chatInput.value = e.target.textContent;
                this.sendMessage();
            }
        });
    }
    
    async sendMessage() {
        const chatInput = document.getElementById('chat-input');
        const message = chatInput.value.trim();
        
        if (!message) return;
        
        // Clear input
        chatInput.value = '';
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            // Send to server
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            // Add bot response
            this.addMessage(data.response, 'bot');
            
            // Update emotion if detected
            if (data.emotion) {
                this.updateEmotion(data.emotion);
            }
            
        } catch (error) {
            console.error('Error sending message:', error);
            this.hideTypingIndicator();
            this.addMessage('I apologize, but I\'m having trouble connecting right now. Please try again in a moment.', 'bot');
        }
    }
    
    addMessage(text, sender) {
        const chatMessages = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = 'message-bubble';
        
        if (sender === 'bot') {
            bubbleDiv.innerHTML = `
                <div class="flex items-center mb-2">
                    <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center mr-3">
                        <span class="text-white text-sm font-bold">AI</span>
                    </div>
                    <span class="text-gray-300 text-sm">MindBridge - NCIT Final Year Project Therapist</span>
                </div>
                <p>${text}</p>
            `;
        } else {
            bubbleDiv.innerHTML = `<p>${text}</p>`;
        }
        
        messageDiv.appendChild(bubbleDiv);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Update message count
        this.messageCount++;
        document.getElementById('message-count').textContent = this.messageCount;
    }
    
    showTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        typingIndicator.style.display = 'block';
        
        // Scroll to show typing indicator
        const chatMessages = document.getElementById('chat-messages');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        typingIndicator.style.display = 'none';
    }
    
    updateSessionDuration() {
        const now = new Date();
        const duration = Math.floor((now - this.sessionStart) / 60000); // minutes
        document.getElementById('session-duration').textContent = `${duration}m`;
    }
    
    updateEmotion(emotion) {
        this.currentEmotion = emotion;
        const emotionElement = document.getElementById('current-emotion');
        const emotionMap = {
            'happy': { class: 'emotion-happy', text: 'Happy' },
            'sad': { class: 'emotion-sad', text: 'Sad' },
            'angry': { class: 'emotion-angry', text: 'Angry' },
            'fear': { class: 'emotion-fear', text: 'Anxious' },
            'neutral': { class: 'emotion-neutral', text: 'Neutral' }
        };
        
        const emotionData = emotionMap[emotion] || emotionMap['neutral'];
        emotionElement.innerHTML = `
            <span class="emotion-indicator ${emotionData.class}"></span>${emotionData.text}
        `;
    }
    
    loadIntentSuggestions() {
        const suggestionsContainer = document.getElementById('intent-suggestions');
        suggestionsContainer.innerHTML = '';
        
        this.intentSuggestions.forEach(suggestion => {
            const chip = document.createElement('div');
            chip.className = 'intent-chip';
            chip.textContent = suggestion;
            suggestionsContainer.appendChild(chip);
        });
    }
    
    loadIntentCategories() {
        const categoriesContainer = document.getElementById('intent-categories');
        const categories = [
            'Anxiety & Stress',
            'Depression Support',
            'Relationship Issues',
            'Sleep Problems',
            'Self-Care & Wellness',
            'Crisis Support',
            'General Counseling'
        ];
        
        categoriesContainer.innerHTML = '';
        categories.forEach(category => {
            const categoryDiv = document.createElement('div');
            categoryDiv.className = 'text-gray-300 text-sm flex items-center';
            categoryDiv.innerHTML = `
                <svg class="w-3 h-3 mr-2 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
                </svg>
                ${category}
            `;
            categoriesContainer.appendChild(categoryDiv);
        });
    }
}

// Initialize chatbot when page loads
document.addEventListener('DOMContentLoaded', () => {
    new MindBridgeChatbot();
});