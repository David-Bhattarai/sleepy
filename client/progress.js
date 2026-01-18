document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/api/progress');
        if (!response.ok) {
            if (response.status === 401) {
                window.location.href = 'signin.html';
            }
            throw new Error('Failed to fetch progress data');
        }
        const data = await response.json();
        renderEmotionHistory(data.emotions);
        renderEmotionFrequency(data.emotions);
    } catch (error) {
        console.error('Error fetching progress data:', error);
    }
});

function renderEmotionHistory(emotions) {
    const ctx = document.getElementById('emotion-history-chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: emotions.map((_, index) => `Session ${index + 1}`),
            datasets: [{
                label: 'Emotion Over Time',
                data: emotions.map(emotion => emotionToValue(emotion)),
                borderColor: '#4A5568',
                backgroundColor: 'rgba(74, 85, 104, 0.2)',
                fill: true,
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return valueToEmotion(value);
                        }
                    }
                }
            }
        }
    });
}

function renderEmotionFrequency(emotions) {
    const emotionCounts = emotions.reduce((acc, emotion) => {
        acc[emotion] = (acc[emotion] || 0) + 1;
        return acc;
    }, {});

    const ctx = document.getElementById('emotion-frequency-chart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(emotionCounts),
            datasets: [{
                label: 'Emotion Frequency',
                data: Object.values(emotionCounts),
                backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
                ]
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function emotionToValue(emotion) {
    const mapping = { 'Happy': 5, 'Joy': 5, 'Surprised': 4, 'Neutral': 3, 'Fear': 2, 'Anxious': 2, 'Sad': 1, 'Sadness': 1, 'Angry': 0 };
    return mapping[emotion] || 3;
}

function valueToEmotion(value) {
    const mapping = { 5: 'Happy', 4: 'Surprised', 3: 'Neutral', 2: 'Anxious', 1: 'Sad', 0: 'Angry' };
    return mapping[value] || '';
}