
document.addEventListener('DOMContentLoaded', () => {
    const circle = document.getElementById('breathing-circle');
    const text = document.getElementById('breathing-text');
    const music = document.getElementById('calm-music');

    const exerciseSequence = [
        { instruction: "Breathe In...", duration: 4000, scale: 1.5 },
        { instruction: "Hold", duration: 7000, scale: 1.5 },
        { instruction: "Breathe Out...", duration: 8000, scale: 1 },
    ];

    let currentIndex = 0;

    function runExercise() {
        const currentStep = exerciseSequence[currentIndex];

        // Update text and circle
        text.style.opacity = 1;
        text.textContent = currentStep.instruction;
        circle.style.transform = `scale(${currentStep.scale})`;

        // Wait for the duration of the step, then move to the next
        setTimeout(() => {
            // Fade out the text slightly before the next instruction
            text.style.opacity = 0.7;
            
            // Move to the next step
            currentIndex = (currentIndex + 1) % exerciseSequence.length;
            runExercise();

        }, currentStep.duration);
    }

    // Start the music and the exercise
    function start() {
        music.play().catch(error => {
            console.log("Browser prevented audio playback. User must interact with the page first.");
            // In many browsers, audio can only start after a user action.
            // We can add a "Start" button if this is an issue.
        });
        
        // A brief pause before starting the first instruction
        setTimeout(() => {
            runExercise();
        }, 1000); 
    }

    // Initial setup
    text.textContent = "Get Ready...";
    circle.style.transform = 'scale(1)';

    // Start the experience
    start();
});
