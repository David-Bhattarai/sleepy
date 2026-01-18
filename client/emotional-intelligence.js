document.addEventListener('DOMContentLoaded', () => {
    const awarenessScoreEl = document.getElementById('awareness-score');
    const regulationScoreEl = document.getElementById('regulation-score');
    const chartCanvas = document.getElementById('ei-chart');
    const loadingStateDiv = document.getElementById('loading-state');
    const contentDiv = document.getElementById('ei-content');

    const token = localStorage.getItem('token');
    let eiChart = null;

    const fetchEiData = async () => {
        if (!token) {
            loadingStateDiv.innerHTML = '<p class="text-red-500">You must be logged in to view this page.</p>';
            return;
        }

        try {
            const response = await fetch('/api/emotional_intelligence', {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (!response.ok) {
                throw new Error('Failed to fetch EI data.');
            }

            const data = await response.json();
            displayScores(data);

        } catch (error) {
            console.error("Error fetching EI data:", error);
            loadingStateDiv.innerHTML = '<p class="text-red-500">Could not load your EI profile. Please try again later.</p>';
        }
    };

    const displayScores = (data) => {
        // Hide loading and show content
        loadingStateDiv.classList.add('hidden');
        contentDiv.classList.remove('hidden');

        // Update latest scores
        if (data.latest) {
            awarenessScoreEl.textContent = data.latest.awareness;
            regulationScoreEl.textContent = data.latest.regulation;
        }

        // Create or update chart
        if (data.history && chartCanvas) {
            const labels = data.history.map(h => new Date(h.timestamp).toLocaleDateString());
            const awarenessData = data.history.map(h => h.awareness_score);
            const regulationData = data.history.map(h => h.regulation_score);

            if (eiChart) {
                eiChart.destroy();
            }

            eiChart = new Chart(chartCanvas, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Emotional Awareness',
                            data: awarenessData,
                            borderColor: '#3B82F6', // blue-600
                            backgroundColor: 'rgba(59, 130, 246, 0.1)',
                            fill: true,
                            tension: 0.3
                        },
                        {
                            label: 'Emotional Regulation',
                            data: regulationData,
                            borderColor: '#10B981', // green-500
                            backgroundColor: 'rgba(16, 185, 129, 0.1)',
                            fill: true,
                            tension: 0.3
                        }
                    ]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    },
                    plugins: {
                        tooltip: {
                            mode: 'index',
                            intersect: false
                        }
                    }
                }
            });
        }
    };

    // Initial load
    fetchEiData();
});
