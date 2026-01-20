document.addEventListener('DOMContentLoaded', () => {
    const gameBoard = document.getElementById('game-board');
    const movesSpan = document.getElementById('moves');
    const timerSpan = document.getElementById('timer');
    const resetBtn = document.getElementById('reset-btn');

    const icons = ['🧠','💧','🧘','☀️','🌙','❤️','😊','✨'];
    let cards = [...icons, ...icons];
    let flippedCards = [];
    let matchedPairs = 0;
    let moves = 0;
    let timer = 0;
    let timerInterval = null;

    function shuffle(array) {
        array.sort(() => Math.random() - 0.5);
    }

    function startGame() {
        shuffle(cards);
        gameBoard.innerHTML = '';
        flippedCards = [];
        matchedPairs = 0;
        moves = 0;
        movesSpan.textContent = moves;
        clearInterval(timerInterval);
        timer = 0;
        timerSpan.textContent = `${timer}s`;

        cards.forEach(icon => {
            const cardElement = document.createElement('div');
            cardElement.classList.add('card');
            cardElement.dataset.icon = icon;
            cardElement.innerHTML = `
                <div class="card-inner">
                    <div class="card-face card-front"></div>
                    <div class="card-face card-back">${icon}</div>
                </div>
            `;
            gameBoard.appendChild(cardElement);
            cardElement.addEventListener('click', handleCardClick);
        });
    }

    function handleCardClick(event) {
        const clickedCard = event.currentTarget;
        if (flippedCards.length < 2 && !clickedCard.classList.contains('flipped')) {
            if (moves === 0 && timer === 0) { 
                timerInterval = setInterval(() => {
                    timer++;
                    timerSpan.textContent = `${timer}s`;
                }, 1000);
            }

            flipCard(clickedCard);

            if (flippedCards.length === 2) {
                checkForMatch();
            }
        }
    }

    function flipCard(card) {
        card.classList.add('flipped');
        flippedCards.push(card);
    }

    function checkForMatch() {
        moves++;
        movesSpan.textContent = moves;
        const [card1, card2] = flippedCards;
        if (card1.dataset.icon === card2.dataset.icon) {
            matchedPairs++;
            flippedCards = [];
            if (matchedPairs === icons.length) {
                clearInterval(timerInterval);
                setTimeout(() => alert(`You won in ${moves} moves and ${timer} seconds!`), 500);
            }
        } else {
            setTimeout(() => {
                unflipCards();
            }, 1000);
        }
    }

    function unflipCards() {
        flippedCards.forEach(card => card.classList.remove('flipped'));
        flippedCards = [];
    }

    resetBtn.addEventListener('click', startGame);

    startGame();
});
