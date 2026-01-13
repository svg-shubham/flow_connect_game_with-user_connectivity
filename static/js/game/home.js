let currentSize = 5;
let currentDotConfig = {};

// 1. Level Numbers dikhane wala function
function showLevelNumbers(size) {
    currentSize = size;
    
    const difficultyArea = document.getElementById('difficulty-area');
    const levelSection = document.getElementById('level-numbers-section');
    const numbersGrid = document.getElementById('numbers-grid');
    const label = document.getElementById('current-difficulty-label');

    // UI Toggle
    difficultyArea.style.display = 'none';
    levelSection.style.display = 'block'; 
    label.innerText = `Select ${size}x${size} Level`;
    
    numbersGrid.innerHTML = ''; 

    // 1 se 30 tak stickers banao
    for (let i = 1; i <= 30; i++) {
        const numBtn = document.createElement('div');
        numBtn.className = 'num-sticker';
        numBtn.innerText = i;
        
        // Loop ke andar hi click event dalo
        numBtn.onclick = () => {
            // Naye approach ke mutabiq page reload karwao
            window.location.href = `/play_game/${size}/${i}/`;
        };
        
        numbersGrid.appendChild(numBtn);
    }
}

// 2. Django View ko call karne wala function (AJAX Fetch)
function fetchLevelData(size, levelNum) {
    console.log(`Fetching Data for: ${size}x${size} Level ${levelNum}`);

    fetch(`/get_level/?size=${size}&level=${levelNum}`) 
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        // YAHAN GALTI THI -> console.log(response) chain ko tod raha tha
        .then(data => {
            if (data.status === 'success') {
                currentDotConfig = data.dots; 
                console.log("Data Received Successfully:", currentDotConfig);
                setupNewGame(size, currentDotConfig, levelNum);
            } else {
                throw new Error(data.message || "Unknown error from backend");
            }
        })
        .catch(error => {
            console.error('Fetch Error:', error);
            alert(`Level ${levelNum} load nahi ho paya. Fallback data use kar rahe hain.`);
            currentDotConfig = backendDots; 
            setupNewGame(size, currentDotConfig, levelNum);
        });
}

// 3. Game Start karne ka function
function setupNewGame(size, dotConfig, levelNum) {
    // UI Elements
    const levelSection = document.getElementById('level-numbers-section');
    const playZone = document.getElementById('game-play-zone');
    const gridContainer = document.getElementById('grid-container');
    const infoLabel = document.getElementById('playing-level-info');

    // 1. Selection hide karo, Play area dikhao
    levelSection.style.display = 'none';
    playZone.style.display = 'block';
    infoLabel.innerText = `Playing: ${size}x${size} - Level ${levelNum}`;

    // 2. Grid setup
    gridContainer.innerHTML = '';
    // Grid size dynamic calculation (60px per cell + gap)
    gridContainer.style.gridTemplateColumns = `repeat(${size}, 60px)`;
    
    // 3. Game Logic Functions
    generateGrid(size, size); // Grid boxes banana
    setupDots(dotConfig);     // Dots place karna
}

// Helper: Wapas difficulty par jaane ke liye (Back Button logic)
function backToDifficulty() {
    document.getElementById('level-numbers-section').style.display = 'none';
    document.getElementById('difficulty-area').style.display = 'flex';
}