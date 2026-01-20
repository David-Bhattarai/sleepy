document.addEventListener('DOMContentLoaded', () => {
    const moodRating = document.getElementById('mood-rating');
    const moodRatingValue = document.getElementById('mood-rating-value');
    const moodNotes = document.getElementById('mood-notes');
    const saveMoodBtn = document.getElementById('save-mood-btn');
    const moodChartCanvas = document.getElementById('mood-chart');

    // Update the display value when the slider changes
    if (moodRating) {
        moodRating.addEventListener('input', () => {
            moodRatingValue.textContent = moodRating.value;
        });
    }

    let moodChart;

    // Function to fetch mood data and render the chart
    const loadMoodHistory = async () => {
        try {
            const response = await fetch('/api/mood', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                console.error('Failed to fetch mood history');
                return;
            }

            const data = await response.json();
            
            if (moodChart) {
                moodChart.destroy(); // Destroy old chart before creating a new one
            }

            const ctx = moodChartCanvas.getContext('2d');
            moodChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.map(entry => new Date(entry.timestamp).toLocaleDateString()),
                    datasets: [{
                        label: 'Mood Rating (1-10)',
                        data: data.map(entry => entry.rating),
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        fill: true,
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 10
                        }
                    }
                }
            });
        } catch (error) {
            console.error('Error loading mood history:', error);
        }
    };

    // Function to save a new mood entry
    const saveMood = async () => {
        const rating = moodRating.value;
        const notes = moodNotes.value;
        const token = localStorage.getItem('token');

        if (!token) {
            window.location.href = '/login.html';
            return;
        }

        try {
            const response = await fetch('/api/mood', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ rating: parseInt(rating), notes })
            });

            if (response.ok) {
                // Clear inputs and reload the chart
                moodNotes.value = '';
                alert('Mood saved successfully!');
                loadMoodHistory();
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.message}`);
            }
        } catch (error) {
            console.error('Error saving mood:', error);
            alert('An error occurred while saving your mood.');
        }
    };

    if (saveMoodBtn) {
        saveMoodBtn.addEventListener('click', saveMood);
    }

    // Initial load of mood history
    if (moodChartCanvas) {
        loadMoodHistory();
    }
});
