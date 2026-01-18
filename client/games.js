document.addEventListener('DOMContentLoaded', () => {
    const breathingCircle = document.getElementById('breathing-circle');
    const breathingText = document.getElementById('breathing-text');

    if (breathingCircle) {
        const animation = () => {
            breathingText.textContent = 'Breathe In...';
            breathingCircle.style.transform = 'scale(1.5)';

            setTimeout(() => {
                breathingText.textContent = 'Breathe Out...';
                breathingCircle.style.transform = 'scale(0.5)';
            }, 4000); // 4 seconds to inhale
        };

        // Initial animation call
        animation();

        // Loop the animation every 8 seconds
        setInterval(animation, 8000);

        // Add transition to the circle
        breathingCircle.style.transition = 'transform 4s ease-in-out';
    }
});
