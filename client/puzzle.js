document.addEventListener('DOMContentLoaded', () => {
    const puzzleContainer = document.getElementById('puzzle-container');
    const shuffleButton = document.getElementById('shuffle-button');
    const moveCounter = document.getElementById('move-counter');

    let tiles = [];
    let emptyTile = { row: 2, col: 2 };
    let moves = 0;

    function createTiles() {
        puzzleContainer.innerHTML = '';
        tiles = [];
        moves = 0;
        moveCounter.textContent = moves;
        let count = 1;
        for (let i = 0; i < 3; i++) {
            const row = [];
            for (let j = 0; j < 3; j++) {
                if (i === 2 && j === 2) {
                    row.push(null); // The empty space
                } else {
                    row.push(count++);
                }
            }
            tiles.push(row);
        }
    }

    function drawTiles() {
        puzzleContainer.innerHTML = '';
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
                const tileValue = tiles[i][j];
                const tile = document.createElement('div');
                tile.classList.add('puzzle-tile');
                if (tileValue === null) {
                    tile.classList.add('empty-tile');
                } else {
                    tile.textContent = tileValue;
                }
                tile.dataset.row = i;
                tile.dataset.col = j;
                tile.addEventListener('click', handleTileClick);
                puzzleContainer.appendChild(tile);
            }
        }
    }

    function handleTileClick(event) {
        const row = parseInt(event.target.dataset.row, 10);
        const col = parseInt(event.target.dataset.col, 10);

        // Check if the clicked tile is adjacent to the empty tile
        const isAdjacent = Math.abs(row - emptyTile.row) + Math.abs(col - emptyTile.col) === 1;

        if (isAdjacent) {
            // Swap the tile with the empty tile
            tiles[emptyTile.row][emptyTile.col] = tiles[row][col];
            tiles[row][col] = null;
            emptyTile = { row, col };
            moves++;
            moveCounter.textContent = moves;
            drawTiles();
            checkWin();
        }
    }

    function shuffleTiles() {
        // Perform a large number of random valid moves to shuffle
        let shuffles = 100;
        for (let i = 0; i < shuffles; i++) {
            const neighbors = [];
            const { row, col } = emptyTile;
            if (row > 0) neighbors.push({ row: row - 1, col });
            if (row < 2) neighbors.push({ row: row + 1, col });
            if (col > 0) neighbors.push({ row, col: col - 1 });
            if (col < 2) neighbors.push({ row, col: col + 1 });

            const randomNeighbor = neighbors[Math.floor(Math.random() * neighbors.length)];
            
            // Swap
            tiles[emptyTile.row][emptyTile.col] = tiles[randomNeighbor.row][randomNeighbor.col];
            tiles[randomNeighbor.row][randomNeighbor.col] = null;
            emptyTile = randomNeighbor;
        }
        moves = 0;
        moveCounter.textContent = moves;
        drawTiles();
    }

    function checkWin() {
        let count = 1;
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
                if (i === 2 && j === 2) {
                    if (tiles[i][j] !== null) return;
                } else {
                    if (tiles[i][j] !== count++) return;
                }
            }
        }
        // If we get here, the puzzle is solved
        setTimeout(() => {
            alert(`You won in ${moves} moves!`);
            createTiles(); // Reset to solved state
            drawTiles();
        }, 300); 
    }

    // Initialize the game
    createTiles();
    drawTiles();
    shuffleButton.addEventListener('click', shuffleTiles);
});