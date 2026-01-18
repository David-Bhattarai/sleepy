document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('zen-canvas');
    const ctx = canvas.getContext('2d');
    const clearBtn = document.getElementById('clear-btn');
    const colorPicker = document.getElementById('color-picker');

    let isDrawing = false;
    let sandColor = colorPicker.value;

    // Set canvas dimensions based on container
    const setCanvasSize = () => {
        const container = canvas.parentElement;
        canvas.width = container.offsetWidth - (2 * 32); // Adjust for padding
        canvas.height = 500;
        fillBackground();
    };

    function fillBackground() {
        ctx.fillStyle = 'rgba(15, 23, 42, 0.8)'; // Dark blue-grey
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    function startDrawing(e) {
        isDrawing = true;
        draw(e);
    }

    function stopDrawing() {
        isDrawing = false;
        ctx.beginPath(); // Reset the path
    }

    function draw(e) {
        if (!isDrawing) return;
        
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        ctx.lineWidth = 3;
        ctx.lineCap = 'round';
        ctx.strokeStyle = sandColor;

        ctx.lineTo(x, y);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(x, y);
    }

    clearBtn.addEventListener('click', fillBackground);
    colorPicker.addEventListener('change', (e) => {
        sandColor = e.target.value;
    });

    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing); // Stop if mouse leaves canvas
    canvas.addEventListener('mousemove', draw);

    // Touch events for mobile
    canvas.addEventListener('touchstart', (e) => {
        e.preventDefault();
        startDrawing(e.touches[0]);
    }, { passive: false });
    canvas.addEventListener('touchend', stopDrawing);
    canvas.addEventListener('touchmove', (e) => {
        e.preventDefault();
        draw(e.touches[0]);
    }, { passive: false });

    window.addEventListener('resize', setCanvasSize);
    setCanvasSize();
});
