/**
 * Simple Mood Tracker JavaScript
 * Basic mood tracking with database operations - no complex ML logic
 */

document.addEventListener('DOMContentLoaded', () => {
    // Get DOM elements
    const moodForm = document.getElementById('simple-mood-form');
    const moodButtons = document.querySelectorAll('.mood-btn');
    const moodNotes = document.getElementById('mood-notes');
    const moodFeedback = document.getElementById('mood-feedback');
    const moodChart = document.getElementById('simple-mood-chart');
    
    // Current selected mood
    let selectedMood = 3; // Default to "Okay"
    let chart = null;
    
    // Initialize simple mood tracker
    initializeSimpleMoodTracker();
    
    function initializeSimpleMoodTracker() {
        console.log('🚀 Initializing Simple Mood Tracker...');
        
        // Set up mood button selection
        moodButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                selectMood(parseInt(button.dataset.mood));
            });
        });
        
        // Set up form submission
        if (moodForm) {
            moodForm.addEventListener('submit', handleMoodSubmission);
        }
        
        // Load existing data
        loadMoodData();
    }
    
    function selectMood(moodValue) {
        selectedMood = moodValue;
        
        // Update button selection
        moodButtons.forEach(btn => {
            btn.classList.remove('selected');
        });
        
        const selectedButton = document.querySelector(`[data-mood="${moodValue}"]`);
        if (selectedButton) {
            selectedButton.classList.add('selected');
        }
        
        console.log(`Selected mood: ${moodValue}`);
    }
    
    async function handleMoodSubmission(event) {
        event.preventDefault();
        
        const token = localStorage.getItem('token');
        if (!token) {
            window.location.href = '/signin.html';
            return;
        }
        
        const moodData = {
            mood_rating: selectedMood,
            mood_notes: moodNotes.value.trim()
        };
        
        try {
            showLoadingState(true);
            
            const response = await fetch('/api/mood_simple', {
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
                // Show success message
                const moodInfo = result.mood_info;
                showFeedback(`${moodInfo.emoji} Mood saved: ${moodInfo.label}!`, 'success');
                
                // Clear form
                moodNotes.value = '';
                selectMood(3); // Reset to default
                
                // Reload data
                loadMoodData();
                
            } else {
                throw new Error(result.message || 'Failed to save mood');
            }
            
        } catch (error) {
            console.error('Error saving mood:', error);
            showFeedback(`Error: ${error.message}`, 'error');
        } finally {
            showLoadingState(false);
        }
    }
    
    async function loadMoodData() {
        const token = localStorage.getItem('token');
        if (!token) return;
        
        try {
            // Load mood statistics
            await loadMoodStats();
            
            // Load mood chart
            await loadMoodChart();
            
            // Load recent entries
            await loadRecentMoods();
            
        } catch (error) {
            console.error('Error loading mood data:', error);
        }
    }
    
    async function loadMoodStats() {
        const token = localStorage.getItem('token');
        
        try {
            const response = await fetch('/api/mood_simple/stats?days=30', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) return;
            
            const stats = await response.json();
            
            // Update stats display
            document.getElementById('total-entries').textContent = stats.total_entries || 0;
            document.getElementById('average-mood').textContent = stats.average_mood || '0';
            document.getElementById('highest-mood').textContent = stats.highest_mood || '0';
            document.getElementById('lowest-mood').textContent = stats.lowest_mood || '0';
            
        } catch (error) {
            console.error('Error loading mood stats:', error);
        }
    }
    
    async function loadMoodChart() {
        const token = localStorage.getItem('token');
        
        try {
            const response = await fetch('/api/mood_simple/chart?days=30', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) return;
            
            const chartData = await response.json();
            
            // Update chart
            updateChart(chartData);
            
        } catch (error) {
            console.error('Error loading mood chart:', error);
        }
    }
    
    async function loadRecentMoods() {
        const token = localStorage.getItem('token');
        
        try {
            const response = await fetch('/api/mood_simple?days=7', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) return;
            
            const data = await response.json();
            
            // Update recent moods display
            displayRecentMoods(data.moods || []);
            
        } catch (error) {
            console.error('Error loading recent moods:', error);
        }
    }
    
    function updateChart(chartData) {
        if (!moodChart) return;
        
        // Destroy existing chart
        if (chart) {
            chart.destroy();
        }
        
        const ctx = moodChart.getContext('2d');
        
        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: chartData.labels || [],
                datasets: [{
                    label: 'Mood Rating',
                    data: chartData.data || [],
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
                                const labels = ['', '😭 Very Bad', '😟 Bad', '😐 Okay', '🙂 Good', '😊 Great'];
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
    
    function displayRecentMoods(moods) {
        const container = document.getElementById('recent-moods');
        if (!container) return;
        
        if (moods.length === 0) {
            container.innerHTML = '<p class="text-gray-400 text-center">No recent mood entries found.</p>';
            return;
        }
        
        const moodEmojis = {
            1: '😭',
            2: '😟', 
            3: '😐',
            4: '🙂',
            5: '😊'
        };
        
        const moodLabels = {
            1: 'Very Bad',
            2: 'Bad',
            3: 'Okay', 
            4: 'Good',
            5: 'Great'
        };
        
        container.innerHTML = moods.map(mood => {
            const date = new Date(mood.timestamp).toLocaleDateString();
            const time = new Date(mood.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            
            return `
                <div class="flex items-center justify-between p-3 bg-white bg-opacity-5 rounded-lg">
                    <div class="flex items-center space-x-3">
                        <span class="text-2xl">${moodEmojis[mood.mood_rating]}</span>
                        <div>
                            <div class="text-white font-medium">${moodLabels[mood.mood_rating]}</div>
                            <div class="text-gray-400 text-sm">${date} at ${time}</div>
                            ${mood.mood_notes ? `<div class="text-gray-300 text-sm mt-1">"${mood.mood_notes}"</div>` : ''}
                        </div>
                    </div>
                    <button onclick="deleteMoodEntry(${mood.id})" class="text-red-400 hover:text-red-300 text-sm">
                        Delete
                    </button>
                </div>
            `;
        }).join('');
    }
    
    // Global function for deleting mood entries
    window.deleteMoodEntry = async function(entryId) {
        const token = localStorage.getItem('token');
        if (!token) return;
        
        if (!confirm('Are you sure you want to delete this mood entry?')) {
            return;
        }
        
        try {
            const response = await fetch(`/api/mood_simple/${entryId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                showFeedback('Mood entry deleted successfully', 'success');
                loadMoodData(); // Reload data
            } else {
                throw new Error('Failed to delete mood entry');
            }
            
        } catch (error) {
            console.error('Error deleting mood entry:', error);
            showFeedback('Error deleting mood entry', 'error');
        }
    };
    
    function showFeedback(message, type = 'success') {
        if (!moodFeedback) return;
        
        const typeClasses = {
            success: 'text-green-400',
            error: 'text-red-400',
            warning: 'text-yellow-400',
            info: 'text-blue-400'
        };
        
        moodFeedback.className = `text-center mt-4 ${typeClasses[type] || typeClasses.success}`;
        moodFeedback.textContent = message;
        
        // Auto-hide after 3 seconds
        setTimeout(() => {
            moodFeedback.textContent = '';
        }, 3000);
    }
    
    function showLoadingState(loading) {
        const submitBtn = moodForm.querySelector('button[type="submit"]');
        if (!submitBtn) return;
        
        if (loading) {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Saving...';
        } else {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Save Mood';
        }
    }
    
    console.log('✅ Simple Mood Tracker Ready!');
});