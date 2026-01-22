/**
 * Advanced Mood Tracker with AI-Powered Intelligence
 * Integrates with backend mood intelligence system for comprehensive tracking
 */

document.addEventListener('DOMContentLoaded', () => {
    // Get DOM elements
    const moodForm = document.getElementById('mood-form');
    const moodSelect = document.getElementById('mood');
    const notesInput = document.getElementById('notes');
    const moodFeedback = document.getElementById('mood-feedback');
    const moodChartCanvas = document.getElementById('mood-chart');
    
    // Advanced tracking variables
    let moodChart;
    let currentInsights = null;
    let analyticsData = null;
    
    // Initialize advanced mood tracker
    initializeAdvancedMoodTracker();
    
    function initializeAdvancedMoodTracker() {
        console.log('🚀 Initializing Advanced Mood Intelligence System...');
        
        // Load existing mood data and analytics
        loadMoodAnalytics();
        loadMoodInsights();
        
        // Set up form submission
        if (moodForm) {
            moodForm.addEventListener('submit', handleAdvancedMoodSubmission);
        }
        
        // Set up real-time mood interpretation
        if (moodSelect) {
            moodSelect.addEventListener('change', showMoodInterpretation);
        }
        
        // Show initial mood interpretation
        showMoodInterpretation();
    }
    
    async function handleAdvancedMoodSubmission(event) {
        event.preventDefault();
        
        const token = localStorage.getItem('token');
        if (!token) {
            window.location.href = '/signin.html';
            return;
        }
        
        // Collect comprehensive mood data
        const moodData = {
            mood_rating: parseInt(moodSelect.value),
            mood_notes: notesInput.value.trim(),
            energy_level: 3, // Default - could be expanded with UI
            sleep_quality: 3, // Default - could be expanded with UI
            stress_level: 3, // Default - could be expanded with UI
            social_interaction: 3, // Default - could be expanded with UI
            physical_activity: 3, // Default - could be expanded with UI
            weather_condition: '', // Could be auto-detected
            location: '', // Could be auto-detected
            triggers: '', // Could be extracted from notes
            medications: '' // Could be tracked separately
        };
        
        try {
            showLoadingState(true);
            
            // Submit to advanced mood intelligence system
            const response = await fetch('/api/mood_advanced', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(moodData)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            
            if (result.success) {
                // Show success with AI insights
                displayMoodSubmissionSuccess(result);
                
                // Clear form
                notesInput.value = '';
                moodSelect.value = '3';
                
                // Reload analytics and insights
                await Promise.all([
                    loadMoodAnalytics(),
                    loadMoodInsights()
                ]);
                
            } else {
                throw new Error(result.message || 'Failed to log mood');
            }
            
        } catch (error) {
            console.error('Error submitting mood:', error);
            showMoodFeedback(`Error: ${error.message}`, 'error');
        } finally {
            showLoadingState(false);
        }
    }
    
    function displayMoodSubmissionSuccess(result) {
        const { mood_category, immediate_insights } = result;
        
        // Show immediate feedback
        const feedbackHtml = `
            <div class="mood-success-feedback">
                <div class="flex items-center justify-center mb-3">
                    <span class="text-2xl mr-2">${mood_category.emoji}</span>
                    <span class="font-semibold">${mood_category.label}</span>
                </div>
                <p class="text-sm opacity-90">${immediate_insights.mood_interpretation.message}</p>
            </div>
        `;
        
        showMoodFeedback(feedbackHtml, 'success');
        
        // Show insights if available
        if (immediate_insights.recommendations && immediate_insights.recommendations.length > 0) {
            setTimeout(() => {
                displayRecommendations(immediate_insights.recommendations);
            }, 2000);
        }
        
        // Show risk assessment if concerning
        if (immediate_insights.risk_assessment && 
            ['moderate', 'high'].includes(immediate_insights.risk_assessment.risk_level)) {
            setTimeout(() => {
                displayRiskAssessment(immediate_insights.risk_assessment);
            }, 3000);
        }
    }
    
    function displayRecommendations(recommendations) {
        const highPriorityRecs = recommendations.filter(rec => rec.priority === 'high');
        
        if (highPriorityRecs.length > 0) {
            const rec = highPriorityRecs[0];
            const recHtml = `
                <div class="recommendation-popup">
                    <h4 class="font-semibold text-blue-300 mb-2">💡 Personalized Recommendation</h4>
                    <h5 class="font-medium mb-1">${rec.title}</h5>
                    <p class="text-sm opacity-90">${rec.description}</p>
                </div>
            `;
            
            showMoodFeedback(recHtml, 'info');
        }
    }
    
    function displayRiskAssessment(riskAssessment) {
        if (riskAssessment.risk_level === 'high') {
            const alertHtml = `
                <div class="risk-alert">
                    <h4 class="font-semibold text-red-300 mb-2">⚠️ Important Notice</h4>
                    <p class="text-sm mb-2">${riskAssessment.message}</p>
                    <p class="text-xs opacity-80">Consider reaching out for professional support.</p>
                </div>
            `;
            
            showMoodFeedback(alertHtml, 'warning');
        }
    }
    
    async function loadMoodAnalytics() {
        const token = localStorage.getItem('token');
        if (!token) return;
        
        try {
            const response = await fetch('/api/mood_analytics?days=30', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error('Failed to load mood analytics');
            }
            
            analyticsData = await response.json();
            
            // Update chart with analytics data
            updateMoodChart(analyticsData.chart_data);
            
            // Display analytics summary
            displayAnalyticsSummary(analyticsData.summary);
            
        } catch (error) {
            console.error('Error loading mood analytics:', error);
        }
    }
    
    async function loadMoodInsights() {
        const token = localStorage.getItem('token');
        if (!token) return;
        
        try {
            const response = await fetch('/api/mood_insights', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error('Failed to load mood insights');
            }
            
            currentInsights = await response.json();
            
            // Display insights in UI
            displayInsightsPanel(currentInsights);
            
        } catch (error) {
            console.error('Error loading mood insights:', error);
        }
    }
    
    function updateMoodChart(chartData) {
        if (!moodChartCanvas || !chartData) return;
        
        // Destroy existing chart
        if (moodChart) {
            moodChart.destroy();
        }
        
        const ctx = moodChartCanvas.getContext('2d');
        
        moodChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: chartData.mood_over_time.labels,
                datasets: [{
                    label: 'Mood Rating',
                    data: chartData.mood_over_time.datasets[0].data,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#3b82f6',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 4
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
                            color: '#ffffff'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        max: 5,
                        ticks: {
                            color: '#ffffff',
                            callback: function(value) {
                                const labels = ['', '😭 Awful', '😟 Bad', '😐 Neutral', '🙂 Good', '😊 Excellent'];
                                return labels[value] || value;
                            }
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    }
                }
            }
        });
    }
    
    function displayAnalyticsSummary(summary) {
        if (!summary) return;
        
        // Create analytics summary display
        const summaryHtml = `
            <div class="analytics-summary mt-6 p-4 bg-black bg-opacity-20 rounded-xl border border-white/10">
                <h3 class="text-lg font-semibold text-white mb-3">📊 Your Mood Analytics</h3>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                    <div class="stat-item">
                        <div class="text-2xl font-bold text-blue-400">${summary.average_mood}</div>
                        <div class="text-xs text-gray-300">Average Mood</div>
                    </div>
                    <div class="stat-item">
                        <div class="text-2xl font-bold text-green-400">${summary.total_entries}</div>
                        <div class="text-xs text-gray-300">Total Entries</div>
                    </div>
                    <div class="stat-item">
                        <div class="text-2xl font-bold text-purple-400">${getMoodTrendEmoji(summary.mood_trend)}</div>
                        <div class="text-xs text-gray-300">${summary.mood_trend}</div>
                    </div>
                    <div class="stat-item">
                        <div class="text-2xl font-bold text-yellow-400">${summary.mood_stability}</div>
                        <div class="text-xs text-gray-300">Stability</div>
                    </div>
                </div>
            </div>
        `;
        
        // Insert after chart
        const chartContainer = moodChartCanvas.parentElement;
        const existingSummary = chartContainer.parentElement.querySelector('.analytics-summary');
        if (existingSummary) {
            existingSummary.remove();
        }
        
        chartContainer.insertAdjacentHTML('afterend', summaryHtml);
    }
    
    function displayInsightsPanel(insights) {
        if (!insights || !insights.recommendations) return;
        
        const insightsHtml = `
            <div class="insights-panel mt-6 p-4 bg-black bg-opacity-20 rounded-xl border border-white/10">
                <h3 class="text-lg font-semibold text-white mb-3">🧠 AI Insights & Recommendations</h3>
                <div class="space-y-3">
                    ${insights.recommendations.map(rec => `
                        <div class="recommendation-item p-3 bg-white bg-opacity-5 rounded-lg">
                            <div class="flex items-start">
                                <span class="text-lg mr-2">${getRecommendationIcon(rec.type)}</span>
                                <div class="flex-1">
                                    <h4 class="font-medium text-white">${rec.title}</h4>
                                    <p class="text-sm text-gray-300 mt-1">${rec.description}</p>
                                    <span class="inline-block mt-2 px-2 py-1 text-xs rounded-full ${getPriorityClass(rec.priority)}">
                                        ${rec.priority} priority
                                    </span>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        
        // Insert insights panel
        const mainContainer = document.querySelector('.max-w-4xl');
        const existingInsights = mainContainer.querySelector('.insights-panel');
        if (existingInsights) {
            existingInsights.remove();
        }
        
        mainContainer.insertAdjacentHTML('beforeend', insightsHtml);
    }
    
    function showMoodInterpretation() {
        const selectedMood = parseInt(moodSelect.value);
        const moodInfo = {
            1: { emoji: '😭', label: 'Severely Low', message: 'Take extra care of yourself today.' },
            2: { emoji: '😟', label: 'Low', message: 'Consider reaching out for support.' },
            3: { emoji: '😐', label: 'Neutral', message: 'A balanced day - room for improvement.' },
            4: { emoji: '🙂', label: 'Good', message: 'Great to see you feeling positive!' },
            5: { emoji: '😊', label: 'Excellent', message: 'Wonderful! Keep up the good energy!' }
        };
        
        const mood = moodInfo[selectedMood];
        const interpretationHtml = `
            <div class="mood-interpretation flex items-center justify-center p-2 bg-white bg-opacity-5 rounded-lg">
                <span class="text-xl mr-2">${mood.emoji}</span>
                <span class="text-sm">${mood.label}: ${mood.message}</span>
            </div>
        `;
        
        // Show interpretation below form
        let interpretationDiv = document.querySelector('.mood-interpretation-container');
        if (!interpretationDiv) {
            interpretationDiv = document.createElement('div');
            interpretationDiv.className = 'mood-interpretation-container mt-3';
            moodForm.appendChild(interpretationDiv);
        }
        
        interpretationDiv.innerHTML = interpretationHtml;
    }
    
    function showMoodFeedback(message, type = 'success') {
        if (!moodFeedback) return;
        
        const typeClasses = {
            success: 'text-green-400',
            error: 'text-red-400',
            warning: 'text-yellow-400',
            info: 'text-blue-400'
        };
        
        moodFeedback.className = `text-center mt-4 ${typeClasses[type] || typeClasses.success}`;
        moodFeedback.innerHTML = message;
        
        // Auto-hide after 5 seconds for success messages
        if (type === 'success') {
            setTimeout(() => {
                moodFeedback.innerHTML = '';
            }, 5000);
        }
    }
    
    function showLoadingState(loading) {
        const submitBtn = moodForm.querySelector('button[type="submit"]');
        if (!submitBtn) return;
        
        if (loading) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '🔄 Analyzing...';
        } else {
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Log Mood';
        }
    }
    
    // Helper functions
    function getMoodTrendEmoji(trend) {
        const trendEmojis = {
            'improving': '📈',
            'declining': '📉',
            'stable': '➡️',
            'insufficient_data': '❓'
        };
        return trendEmojis[trend] || '➡️';
    }
    
    function getRecommendationIcon(type) {
        const icons = {
            'immediate': '⚡',
            'social': '👥',
            'physical': '🏃',
            'planning': '📋',
            'nutrition': '🥗',
            'evening': '🌙',
            'getting_started': '🚀'
        };
        return icons[type] || '💡';
    }
    
    function getPriorityClass(priority) {
        const classes = {
            'high': 'bg-red-500 bg-opacity-20 text-red-300',
            'medium': 'bg-yellow-500 bg-opacity-20 text-yellow-300',
            'low': 'bg-green-500 bg-opacity-20 text-green-300'
        };
        return classes[priority] || classes.medium;
    }
    
    // Initialize on page load
    console.log('✅ Advanced Mood Intelligence System Ready!');
});
