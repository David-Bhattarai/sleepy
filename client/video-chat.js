/**
 * Video Chat System with Doctor Booking
 * Includes dummy AI doctors and booking functionality
 */

document.addEventListener('DOMContentLoaded', () => {
    // Get DOM elements
    const bookingSection = document.getElementById('booking-section');
    const videoChatSection = document.getElementById('video-chat-section');
    const doctorCards = document.querySelectorAll('.doctor-card');
    const timeSlots = document.getElementById('time-slots');
    const paymentSection = document.getElementById('payment-section');
    const timeSlotButtons = document.querySelectorAll('.time-slot');
    const processPaymentBtn = document.getElementById('process-payment');
    const endCallBtn = document.getElementById('end-call');
    const bookingInfo = document.getElementById('booking-info');
    
    // Payment elements
    const paymentDoctor = document.getElementById('payment-doctor');
    const paymentTime = document.getElementById('payment-time');
    const paymentAmount = document.getElementById('payment-amount');
    const cardPaymentBtn = document.getElementById('card-payment-btn');
    const esewaPaymentBtn = document.getElementById('esewa-payment-btn');
    const cardPaymentForm = document.getElementById('card-payment-form');
    const esewaPaymentForm = document.getElementById('esewa-payment-form');
    const cardNumber = document.getElementById('card-number');
    const cardExpiry = document.getElementById('card-expiry');
    const cardCvv = document.getElementById('card-cvv');
    const cardName = document.getElementById('card-name');
    
    // Video chat elements
    const doctorAvatar = document.getElementById('doctor-avatar');
    const doctorName = document.getElementById('doctor-name');
    const sessionTimer = document.getElementById('session-timer');
    const sessionCost = document.getElementById('session-cost');
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const sendMessageBtn = document.getElementById('send-message');
    const userVideo = document.getElementById('user-video');
    const toggleVideoBtn = document.getElementById('toggle-video');
    const toggleAudioBtn = document.getElementById('toggle-audio');
    
    // State variables
    let selectedDoctor = null;
    let selectedTime = null;
    let selectedPaymentMethod = 'card'; // 'card' or 'esewa'
    let sessionStartTime = null;
    let sessionDuration = 50 * 60; // 50 minutes in seconds
    let timerInterval = null;
    let videoEnabled = true;
    let audioEnabled = true;
    let userStream = null;
    
    // Doctor data with pricing
    const doctors = {
        'dr-smith': {
            name: 'Dr. Smith',
            avatar: '👨‍⚕️',
            specialty: 'Mental Health Specialist',
            price: 80,
            greeting: 'Hello! I\'m Dr. Smith. I specialize in helping people with anxiety and depression. How can I support you today?',
            responses: [
                'I understand how you\'re feeling. Can you tell me more about what\'s been troubling you?',
                'That sounds really challenging. You\'re brave for reaching out for help.',
                'Let\'s work through this together. What coping strategies have you tried before?',
                'It\'s completely normal to feel this way. Many people experience similar challenges.',
                'I want you to know that you\'re not alone in this. We can find ways to help you feel better.'
            ]
        },
        'dr-johnson': {
            name: 'Dr. Johnson',
            avatar: '👩‍⚕️',
            specialty: 'Licensed Counselor',
            price: 75,
            greeting: 'Hi there! I\'m Dr. Johnson, and I focus on stress management techniques. What\'s been causing you stress lately?',
            responses: [
                'Stress can really impact our daily lives. Let\'s identify some triggers together.',
                'Have you tried any relaxation techniques like deep breathing or meditation?',
                'It sounds like you\'re dealing with a lot. Let\'s break this down into manageable pieces.',
                'Stress is your body\'s way of responding to challenges. We can learn to manage it better.',
                'I\'d like to teach you some practical stress-reduction techniques. Are you interested?'
            ]
        },
        'dr-williams': {
            name: 'Dr. Williams',
            avatar: '👨‍⚕️',
            specialty: 'Psychiatrist',
            price: 90,
            greeting: 'Welcome! I\'m Dr. Williams. I help people understand and manage mood disorders. How has your mood been lately?',
            responses: [
                'Mood changes can be confusing and overwhelming. You\'re doing the right thing by seeking help.',
                'Can you describe the patterns you\'ve noticed in your mood changes?',
                'It\'s important to track these feelings. Have you been keeping a mood journal?',
                'Understanding your mood patterns is the first step toward feeling better.',
                'Remember, mood disorders are treatable. There\'s hope for feeling better.'
            ]
        },
        'dr-brown': {
            name: 'Dr. Brown',
            avatar: '👩‍⚕️',
            specialty: 'Trauma Specialist',
            price: 85,
            greeting: 'Hello, I\'m Dr. Brown. I work with people who have experienced trauma. This is a safe space for you to share.',
            responses: [
                'Thank you for trusting me with your story. That takes a lot of courage.',
                'Trauma affects everyone differently. Your feelings are completely valid.',
                'Healing from trauma is a journey, and it\'s okay to take it one step at a time.',
                'You\'ve survived something difficult, and that shows your incredible strength.',
                'We\'ll work together at your pace. You\'re in control of this process.'
            ]
        },
        'dr-davis': {
            name: 'Dr. Davis',
            avatar: '👨‍⚕️',
            specialty: 'Relationship Counselor',
            price: 70,
            greeting: 'Hi! I\'m Dr. Davis, and I help people navigate relationship challenges. What\'s been on your mind about your relationships?',
            responses: [
                'Relationships can be complex. It\'s great that you\'re working on improving them.',
                'Communication is often key in relationships. How do you typically express your feelings?',
                'It sounds like there are some important dynamics to explore here.',
                'Healthy relationships require work from everyone involved. You\'re taking a positive step.',
                'Let\'s talk about what healthy boundaries look like in your relationships.'
            ]
        },
        'dr-wilson': {
            name: 'Dr. Wilson',
            avatar: '👩‍⚕️',
            specialty: 'Addiction Specialist',
            price: 95,
            greeting: 'Hello, I\'m Dr. Wilson. I support people on their recovery journey. Recovery is possible, and I\'m here to help.',
            responses: [
                'Recovery is a brave journey, and every day you choose it is a victory.',
                'What does your support system look like right now?',
                'Addiction is a disease, not a moral failing. You deserve compassion and help.',
                'Let\'s talk about healthy coping strategies that can support your recovery.',
                'Relapses can be part of recovery. What matters is that you keep trying.'
            ]
        }
    };
    
    // Initialize the system
    initializeVideoChat();
    
    function initializeVideoChat() {
        console.log('🎥 Initializing Video Chat System...');
        
        // Set up doctor selection
        doctorCards.forEach(card => {
            card.addEventListener('click', () => selectDoctor(card.dataset.doctor));
        });
        
        // Set up time slot selection
        timeSlotButtons.forEach(button => {
            button.addEventListener('click', () => selectTimeSlot(button.dataset.time));
        });
        
        // Set up consultation start
        if (processPaymentBtn) {
            processPaymentBtn.addEventListener('click', processPayment);
        }
        
        // Set up payment method switching
        if (cardPaymentBtn) {
            cardPaymentBtn.addEventListener('click', () => switchPaymentMethod('card'));
        }
        
        if (esewaPaymentBtn) {
            esewaPaymentBtn.addEventListener('click', () => switchPaymentMethod('esewa'));
        }
        
        // Set up end call
        if (endCallBtn) {
            endCallBtn.addEventListener('click', endVideoCall);
        }
        
        // Set up chat
        if (sendMessageBtn) {
            sendMessageBtn.addEventListener('click', sendChatMessage);
        }
        
        if (chatInput) {
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    sendChatMessage();
                }
            });
        }
        
        // Set up quick response buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('quick-response')) {
                const message = e.target.dataset.message;
                if (message && selectedDoctor) {
                    // Add user message
                    addChatMessage('user', message);
                    
                    // Show typing indicator and send to Gemini AI
                    addTypingIndicator();
                    sendToGeminiAI(message);
                }
            }
        });
        
        // Set up video controls
        if (toggleVideoBtn) {
            toggleVideoBtn.addEventListener('click', toggleVideo);
        }
        
        if (toggleAudioBtn) {
            toggleAudioBtn.addEventListener('click', toggleAudio);
        }
    }
    
    function selectDoctor(doctorId) {
        console.log('🩺 Selecting doctor:', doctorId);
        
        // Remove previous selections
        doctorCards.forEach(card => {
            card.classList.remove('border-blue-400', 'bg-blue-500', 'bg-opacity-10');
        });
        
        // Highlight selected doctor
        const selectedCard = document.querySelector(`[data-doctor="${doctorId}"]`);
        if (selectedCard) {
            selectedCard.classList.add('border-blue-400', 'bg-blue-500', 'bg-opacity-10');
            console.log('✅ Doctor card highlighted');
        } else {
            console.error('❌ Doctor card not found');
        }
        
        selectedDoctor = doctorId;
        
        // Show time slots
        if (timeSlots) {
            timeSlots.classList.remove('hidden');
            console.log('✅ Time slots shown');
        } else {
            console.error('❌ Time slots element not found');
        }
        
        if (bookingInfo) {
            bookingInfo.textContent = `Selected: ${doctors[doctorId].name} - Choose a time slot`;
        }
        
        console.log(`✅ Selected doctor: ${doctors[doctorId].name}`);
    }
    
    function selectTimeSlot(time) {
        console.log('⏰ Selecting time slot:', time);
        
        // Remove previous selections
        timeSlotButtons.forEach(button => {
            button.classList.remove('bg-blue-500', 'bg-opacity-30');
        });
        
        // Highlight selected time
        const selectedButton = document.querySelector(`[data-time="${time}"]`);
        if (selectedButton) {
            selectedButton.classList.add('bg-blue-500', 'bg-opacity-30');
            console.log('✅ Time slot highlighted');
        } else {
            console.error('❌ Time slot button not found');
        }
        
        selectedTime = time;
        
        // Show payment section
        console.log('Showing payment section...');
        showPaymentSection();
        
        console.log(`✅ Selected time: ${time}`);
    }
    
    function showPaymentSection() {
        if (!selectedDoctor || !selectedTime) return;
        
        const doctor = doctors[selectedDoctor];
        
        // Update payment info
        if (paymentDoctor) paymentDoctor.textContent = doctor.name;
        if (paymentTime) paymentTime.textContent = selectedTime;
        if (paymentAmount) paymentAmount.textContent = `$${doctor.price}`;
        
        // Show payment section
        paymentSection.classList.remove('hidden');
        bookingInfo.textContent = 'Complete payment to start your session';
        
        // Add card formatting
        setupCardFormatting();
    }
    
    function setupCardFormatting() {
        // Format card number
        if (cardNumber) {
            cardNumber.addEventListener('input', (e) => {
                let value = e.target.value.replace(/\s/g, '').replace(/[^0-9]/gi, '');
                let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
                e.target.value = formattedValue;
            });
        }
        
        // Format expiry
        if (cardExpiry) {
            cardExpiry.addEventListener('input', (e) => {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length >= 2) {
                    value = value.substring(0, 2) + '/' + value.substring(2, 4);
                }
                e.target.value = value;
            });
        }
        
        // Format CVV
        if (cardCvv) {
            cardCvv.addEventListener('input', (e) => {
                e.target.value = e.target.value.replace(/\D/g, '');
            });
        }
    }
    
    function switchPaymentMethod(method) {
        selectedPaymentMethod = method;
        
        // Update button states
        if (cardPaymentBtn && esewaPaymentBtn) {
            cardPaymentBtn.classList.remove('active');
            esewaPaymentBtn.classList.remove('active');
            
            if (method === 'card') {
                cardPaymentBtn.classList.add('active');
                cardPaymentForm.classList.remove('hidden');
                esewaPaymentForm.classList.add('hidden');
                processPaymentBtn.innerHTML = '🔒 Process Card Payment & Start Session';
            } else {
                esewaPaymentBtn.classList.add('active');
                cardPaymentForm.classList.add('hidden');
                esewaPaymentForm.classList.remove('hidden');
                processPaymentBtn.innerHTML = '📱 Pay with eSewa & Start Session';
            }
        }
        
        console.log(`Switched to ${method} payment`);
    }
    
    async function processPayment() {
        console.log('💳 Processing payment...');
        console.log('Selected payment method:', selectedPaymentMethod);
        
        // Validate payment based on selected method
        if (selectedPaymentMethod === 'card') {
            console.log('Validating card payment...');
            if (!validateCardPayment()) {
                console.log('❌ Card validation failed');
                return;
            }
            console.log('✅ Card validation passed');
        }
        
        try {
            processPaymentBtn.disabled = true;
            
            if (selectedPaymentMethod === 'esewa') {
                processPaymentBtn.innerHTML = '🔄 Redirecting to eSewa...';
                await processEsewaPayment();
            } else {
                processPaymentBtn.innerHTML = '🔄 Processing Card Payment...';
                await processCardPayment();
            }
            
            console.log('✅ Payment processed, starting video consultation...');
            
            // Start video consultation after successful payment
            await startVideoConsultation();
            
        } catch (error) {
            console.error('Payment failed:', error);
            alert('Payment failed. Please try again.');
            processPaymentBtn.disabled = false;
            
            if (selectedPaymentMethod === 'esewa') {
                processPaymentBtn.innerHTML = '📱 Pay with eSewa & Start Session';
            } else {
                processPaymentBtn.innerHTML = '🔒 Process Card Payment & Start Session';
            }
        }
    }
    
    function validateCardPayment() {
        const cardNum = cardNumber?.value.replace(/\s/g, '') || '';
        const expiry = cardExpiry?.value || '';
        const cvv = cardCvv?.value || '';
        const name = cardName?.value.trim() || '';
        
        // More permissive validation for demo purposes
        if (cardNum.length < 4) {
            alert('Please enter at least 4 digits for card number (demo)');
            cardNumber?.focus();
            return false;
        }
        
        if (expiry.length < 3) {
            alert('Please enter expiry date (MM/YY)');
            cardExpiry?.focus();
            return false;
        }
        
        if (cvv.length < 3) {
            alert('Please enter CVV (any 3 digits)');
            cardCvv?.focus();
            return false;
        }
        
        if (name.length < 2) {
            alert('Please enter cardholder name');
            cardName?.focus();
            return false;
        }
        
        return true;
    }
    
    async function processCardPayment() {
        // Simulate card payment processing
        return new Promise((resolve) => {
            setTimeout(() => {
                console.log('Card payment processed successfully');
                resolve();
            }, 2000);
        });
    }
    
    async function processEsewaPayment() {
        // Simulate eSewa payment processing
        return new Promise((resolve, reject) => {
            // Create eSewa payment parameters
            const doctor = doctors[selectedDoctor];
            const esewaParams = {
                amt: doctor.price,
                pdc: 0,
                psc: 0,
                txAmt: doctor.price,
                tAmt: doctor.price,
                pid: `AURA-${Date.now()}`, // Unique product ID
                scd: 'AURA001', // Service charge (dummy)
                su: window.location.origin + '/video-chat.html?payment=success',
                fu: window.location.origin + '/video-chat.html?payment=failed'
            };
            
            // Show eSewa simulation dialog
            const confirmed = confirm(
                `eSewa Payment Simulation\n\n` +
                `Amount: Rs. ${doctor.price * 130} (NPR)\n` + // Convert USD to NPR (approx)
                `Service: Video Consultation\n` +
                `Doctor: ${doctor.name}\n` +
                `Time: ${selectedTime}\n\n` +
                `Click OK to simulate successful eSewa payment\n` +
                `Click Cancel to simulate payment failure`
            );
            
            setTimeout(() => {
                if (confirmed) {
                    console.log('eSewa payment processed successfully');
                    console.log('Payment params:', esewaParams);
                    resolve();
                } else {
                    reject(new Error('eSewa payment cancelled by user'));
                }
            }, 1500);
        });
    }
    
    async function startVideoConsultation() {
        if (!selectedDoctor || !selectedTime) {
            alert('Please complete the booking process first!');
            return;
        }
        
        try {
            // Try to get user media, but don't fail if it doesn't work
            try {
                userStream = await navigator.mediaDevices.getUserMedia({ 
                    video: true, 
                    audio: true 
                });
                
                if (userVideo) {
                    userVideo.srcObject = userStream;
                }
                console.log('✅ Camera/microphone access granted');
            } catch (mediaError) {
                console.log('⚠️  Camera/microphone access denied, continuing without video');
                // Continue without user video - this is fine for demo
            }
            
            // Hide booking section and show video chat
            bookingSection.classList.add('hidden');
            videoChatSection.classList.remove('hidden');
            
            // Set up doctor info
            const doctor = doctors[selectedDoctor];
            if (doctorAvatar) doctorAvatar.textContent = doctor.avatar;
            if (doctorName) doctorName.textContent = doctor.name;
            if (sessionCost) sessionCost.textContent = `$${doctor.price}`;
            
            // Start session timer
            startSessionTimer();
            
            // Add doctor's greeting message using Gemini AI
            addTypingIndicator();
            
            // Send greeting through Gemini AI for more personalized welcome
            setTimeout(() => {
                sendToGeminiAI(`Hello, I'm starting my session with ${doctor.name}. Please introduce yourself and let me know how you can help me today.`);
            }, 1000);
            
            console.log(`Started consultation with ${doctor.name} at ${selectedTime}`);
            
        } catch (error) {
            console.error('Error starting video consultation:', error);
            // Don't fail completely - show video section anyway
            bookingSection.classList.add('hidden');
            videoChatSection.classList.remove('hidden');
            
            // Set up basic doctor info
            const doctor = doctors[selectedDoctor];
            if (doctorAvatar) doctorAvatar.textContent = doctor.avatar;
            if (doctorName) doctorName.textContent = doctor.name;
            if (sessionCost) sessionCost.textContent = `$${doctor.price}`;
            
            startSessionTimer();
            console.log('✅ Video consultation started (fallback mode)');
        }
    }
    
    function startSessionTimer() {
        sessionStartTime = Date.now();
        
        timerInterval = setInterval(() => {
            const elapsed = Math.floor((Date.now() - sessionStartTime) / 1000);
            const remaining = Math.max(0, sessionDuration - elapsed);
            
            const minutes = Math.floor(remaining / 60);
            const seconds = remaining % 60;
            
            if (sessionTimer) {
                sessionTimer.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
            }
            
            // Change color as time runs out
            if (remaining <= 300) { // Last 5 minutes
                sessionTimer.classList.add('text-red-400');
                sessionTimer.classList.remove('text-blue-400');
            } else if (remaining <= 600) { // Last 10 minutes
                sessionTimer.classList.add('text-yellow-400');
                sessionTimer.classList.remove('text-blue-400');
            }
            
            // Auto-end session when time is up
            if (remaining <= 0) {
                clearInterval(timerInterval);
                addChatMessage('ai', 'Our session time has ended. Thank you for choosing our service. Take care!');
                setTimeout(() => {
                    endVideoCall();
                }, 3000);
            }
        }, 1000);
    }
    
    function endVideoCall() {
        // Stop session timer
        if (timerInterval) {
            clearInterval(timerInterval);
            timerInterval = null;
        }
        
        // Stop user stream
        if (userStream) {
            userStream.getTracks().forEach(track => track.stop());
            userStream = null;
        }
        
        // Show booking section and hide video chat
        videoChatSection.classList.add('hidden');
        bookingSection.classList.remove('hidden');
        
        // Reset selections
        selectedDoctor = null;
        selectedTime = null;
        sessionStartTime = null;
        
        // Clear selections
        doctorCards.forEach(card => {
            card.classList.remove('border-blue-400', 'bg-blue-500', 'bg-opacity-10');
        });
        
        timeSlotButtons.forEach(button => {
            button.classList.remove('bg-blue-500', 'bg-opacity-30');
        });
        
        // Hide sections
        timeSlots.classList.add('hidden');
        paymentSection.classList.add('hidden');
        bookingInfo.textContent = 'Select a doctor to see available time slots';
        
        // Clear payment form
        if (cardNumber) cardNumber.value = '';
        if (cardExpiry) cardExpiry.value = '';
        if (cardCvv) cardCvv.value = '';
        if (cardName) cardName.value = '';
        
        // Reset payment button
        if (processPaymentBtn) {
            processPaymentBtn.disabled = false;
            processPaymentBtn.innerHTML = '🔒 Process Payment & Start Session';
        }
        
        // Clear chat
        if (chatMessages) {
            chatMessages.innerHTML = '';
        }
        
        // Reset timer display
        if (sessionTimer) {
            sessionTimer.textContent = '50:00';
            sessionTimer.classList.remove('text-red-400', 'text-yellow-400');
            sessionTimer.classList.add('text-blue-400');
        }
        
        console.log('Video call ended');
    }
    
    function sendChatMessage() {
        if (!chatInput || !selectedDoctor) return;
        
        const message = chatInput.value.trim();
        if (!message) return;
        
        // Add user message
        addChatMessage('user', message);
        chatInput.value = '';
        
        // Show typing indicator
        addTypingIndicator();
        
        // Send to Gemini AI endpoint
        sendToGeminiAI(message);
    }
    
    async function sendToGeminiAI(message) {
        try {
            const token = localStorage.getItem('token');
            
            // If no token, use fallback immediately
            if (!token) {
                console.log('No auth token, using fallback response');
                removeTypingIndicator();
                const doctor = doctors[selectedDoctor];
                const fallbackResponses = doctor.responses;
                const randomResponse = fallbackResponses[Math.floor(Math.random() * fallbackResponses.length)];
                addChatMessage('ai', randomResponse, 'Demo Response');
                return;
            }
            
            const doctor = doctors[selectedDoctor];
            const doctorContext = {
                name: doctor.name,
                specialty: doctor.specialty,
                avatar: doctor.avatar
            };
            
            const response = await fetch('/api/video_chat/gemini', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    message: message,
                    doctor_context: doctorContext
                })
            });
            
            const data = await response.json();
            
            // Remove typing indicator
            removeTypingIndicator();
            
            if (data.success) {
                // Add AI response with method indicator
                const methodIndicator = data.method === 'gemini_ai' ? 'Powered by Gemini AI' : 
                                      data.method === 'enhanced_fallback' ? 'Enhanced AI Response' : 
                                      'AI Response';
                
                addChatMessage('ai', data.response, methodIndicator);
                
                // Log successful interaction
                console.log(`✅ Video chat response via ${data.method}:`, data.response.substring(0, 50) + '...');
                
            } else {
                // Fallback response
                addChatMessage('ai', data.response || 'I apologize, but I\'m having trouble responding right now. Please try again.', 'Fallback Response');
                console.error('Gemini AI error:', data.error);
            }
            
        } catch (error) {
            console.error('Error sending message to Gemini AI:', error);
            removeTypingIndicator();
            
            // Ultimate fallback - always works
            const doctor = doctors[selectedDoctor];
            const fallbackResponses = doctor.responses;
            const randomResponse = fallbackResponses[Math.floor(Math.random() * fallbackResponses.length)];
            addChatMessage('ai', randomResponse, 'Demo Response');
        }
    }
    
    function addTypingIndicator() {
        if (!chatMessages) return;
        
        const typingDiv = document.createElement('div');
        typingDiv.className = 'chat-message-ai typing-indicator';
        typingDiv.id = 'typing-indicator';
        
        typingDiv.innerHTML = `
            <div class="flex items-start space-x-2">
                <div class="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center text-xs">🤖</div>
                <div class="bg-blue-600 bg-opacity-30 rounded-lg p-2 max-w-xs">
                    <div class="flex space-x-1">
                        <div class="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                        <div class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                        <div class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                    </div>
                    <span class="text-xs text-gray-400 mt-1 block">AI is thinking...</span>
                </div>
            </div>
        `;
        
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    function addChatMessage(sender, message, methodIndicator = null) {
        if (!chatMessages) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message-${sender}`;
        
        if (sender === 'user') {
            messageDiv.innerHTML = `
                <div class="flex items-start space-x-2 justify-end">
                    <div class="bg-gray-700 bg-opacity-50 rounded-lg p-2 max-w-xs">
                        <p class="text-white text-sm">${message}</p>
                    </div>
                    <div class="w-6 h-6 bg-gray-600 rounded-full flex items-center justify-center text-xs">👤</div>
                </div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="flex items-start space-x-2">
                    <div class="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center text-xs">🤖</div>
                    <div class="bg-blue-600 bg-opacity-30 rounded-lg p-2 max-w-xs">
                        <p class="text-white text-sm">${message}</p>
                        ${methodIndicator ? `<span class="text-xs text-gray-400 mt-1 block">${methodIndicator}</span>` : ''}
                    </div>
                </div>
            `;
        }
        
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function toggleVideo() {
        if (!userStream) return;
        
        videoEnabled = !videoEnabled;
        const videoTrack = userStream.getVideoTracks()[0];
        
        if (videoTrack) {
            videoTrack.enabled = videoEnabled;
        }
        
        // Update button appearance
        if (videoEnabled) {
            toggleVideoBtn.classList.remove('bg-red-600');
            toggleVideoBtn.classList.add('bg-gray-600');
        } else {
            toggleVideoBtn.classList.remove('bg-gray-600');
            toggleVideoBtn.classList.add('bg-red-600');
        }
        
        console.log(`Video ${videoEnabled ? 'enabled' : 'disabled'}`);
    }
    
    function toggleAudio() {
        if (!userStream) return;
        
        audioEnabled = !audioEnabled;
        const audioTrack = userStream.getAudioTracks()[0];
        
        if (audioTrack) {
            audioTrack.enabled = audioEnabled;
        }
        
        // Update button appearance
        if (audioEnabled) {
            toggleAudioBtn.classList.remove('bg-red-600');
            toggleAudioBtn.classList.add('bg-gray-600');
        } else {
            toggleAudioBtn.classList.remove('bg-gray-600');
            toggleAudioBtn.classList.add('bg-red-600');
        }
        
        console.log(`Audio ${audioEnabled ? 'enabled' : 'disabled'}`);
    }
    
    console.log('✅ Video Chat System Ready!');
    
    // Add debug helper
    window.debugVideoChat = function() {
        console.log('🔍 Video Chat Debug Info:');
        console.log('Selected Doctor:', selectedDoctor);
        console.log('Selected Time:', selectedTime);
        console.log('Payment Method:', selectedPaymentMethod);
        console.log('Auth Token:', localStorage.getItem('token') ? 'Present' : 'Missing');
        console.log('Booking Section Hidden:', bookingSection?.classList.contains('hidden'));
        console.log('Video Section Hidden:', videoChatSection?.classList.contains('hidden'));
        
        // Check if elements exist
        console.log('Elements Check:');
        console.log('- bookingSection:', !!bookingSection);
        console.log('- videoChatSection:', !!videoChatSection);
        console.log('- paymentSection:', !!paymentSection);
        console.log('- processPaymentBtn:', !!processPaymentBtn);
        
        // Check doctor cards
        const doctorCardsCount = document.querySelectorAll('.doctor-card').length;
        console.log('- Doctor cards found:', doctorCardsCount);
        
        // Check time slots
        const timeSlotsCount = document.querySelectorAll('.time-slot').length;
        console.log('- Time slots found:', timeSlotsCount);
    };
    
    // Add quick test function
    window.testVideoChat = function() {
        console.log('🧪 Running quick video chat test...');
        
        // Auto-select doctor and time for testing
        selectedDoctor = 'dr-smith';
        selectedTime = '10:00';
        
        // Fill dummy payment data
        if (cardNumber) cardNumber.value = '1234 5678 9012 3456';
        if (cardExpiry) cardExpiry.value = '12/25';
        if (cardCvv) cardCvv.value = '123';
        if (cardName) cardName.value = 'Test User';
        
        // Show payment section
        showPaymentSection();
        
        console.log('✅ Test data filled. Click "Process Payment" to test video chat.');
    };
    
    // Add manual video chat starter (bypass all validation)
    window.forceStartVideoChat = function() {
        console.log('🚀 Force starting video chat...');
        
        // Set defaults if not selected
        if (!selectedDoctor) selectedDoctor = 'dr-smith';
        if (!selectedTime) selectedTime = '10:00';
        
        // Hide booking, show video directly
        if (bookingSection) bookingSection.classList.add('hidden');
        if (videoChatSection) videoChatSection.classList.remove('hidden');
        
        // Set doctor info
        const doctor = doctors[selectedDoctor] || { name: 'Dr. Smith', avatar: '👨‍⚕️', price: 80 };
        if (doctorAvatar) doctorAvatar.textContent = doctor.avatar;
        if (doctorName) doctorName.textContent = doctor.name;
        if (sessionCost) sessionCost.textContent = `$${doctor.price}`;
        
        console.log('✅ Video chat force started!');
    };
    
    console.log('💡 Debug helpers available:');
    console.log('   - debugVideoChat() - Show current state');
    console.log('   - testVideoChat() - Fill test data quickly');
    console.log('   - forceStartVideoChat() - Force start video chat');
});