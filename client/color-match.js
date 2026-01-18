document.addEventListener('DOMContentLoaded', () => {
    const scoreSpan = document.getElementById('score');
    const timerSpan = document.getElementById('timer');
    const wordEl = document.getElementById('word');
    const yesBtn = document.getElementById('yes-btn');
    const noBtn = document.getElementById('no-btn');
    const startScreen = document.getElementById('start-screen');
    const endScreen = document.getElementById('end-screen');
    const startBtn = document.getElementById('start-btn');
    const restartBtn = document.getElementById('restart-btn');
    const finalScoreSpan = document.getElementById('final-score');

    const colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange'];
    let score = 0;
    let timeLeft = 30;
    let timerInterval = null;
    let currentWord;
    let currentColor;
    let isMatch;

    function getRandomItem(arr) {
        return arr[Math.floor(Math.random() * arr.length)];
    }

    function nextTurn() {
        currentWord = getRandomItem(colors);
        currentColor = getRandomItem(colors);
        isMatch = currentWord === currentColor;

        wordEl.textContent = currentWord;
        wordEl.style.color = currentColor;
    }

    function startGame() {
        score = 0;
        timeLeft = 30;
        scoreSpan.textContent = score;
        timerSpan.textContent = `${timeLeft}s`;
        startScreen.classList.add('hidden');
        endScreen.classList.add('hidden');

        nextTurn();

        timerInterval = setInterval(() => {
            timeLeft--;
            timerSpan.textContent = `${timeLeft}s`;
            if (timeLeft <= 0) {
                endGame();
            }
        }, 1000);
    }

    function endGame() {
        clearInterval(timerInterval);
        finalScoreSpan.textContent = score;
        endScreen.classList.remove('hidden');
    }

    function handleAnswer(userAnswer) {
        if ((userAnswer && isMatch) || (!userAnswer && !isMatch)) {
            score++;
            scoreSpan.textContent = score;
        } else {
            // Optional: penalty for wrong answer
            // score--; 
        }
        nextTurn();
    }

    yesBtn.addEventListener('click', () => handleAnswer(true));
    noBtn.addEventListener('click', () => handleAnswer(false));
    startBtn.addEventListener('click', startGame);
    restartBtn.addEventListener('click', startGame);
});
