let gridData = {};
let selectedColor = null;
let startCellId = null;
let lastHoveredId = null;
let isDrawing = false; 
let isTargetReached = false;

const pathColors = {
    "yellow": "rgba(255, 255, 0, 0.3)",
    "orange": "rgba(255, 165, 0, 0.3)",
    "blue":   "rgba(0, 0, 255, 0.3)",
    "green":  "rgba(0, 128, 0, 0.3)",
    "red":    "rgba(255, 0, 0, 0.3)"
};

function generateGrid(rows, cols) {
    const container = document.getElementById('grid-container');
    gridData = {};
    for (let r = 1; r <= rows; r++) {
        for (let c = 1; c <= cols; c++) {
            const cellId = `${r}${c}`;
            gridData[cellId] = { id: cellId, color: "", hasDot: false };
            const cell = document.createElement('div');
            cell.id = cellId;
            cell.className = `cell cell_${cellId}`;

            cell.addEventListener('click', () => handleCellClick(cellId));
            cell.addEventListener('mouseenter', () => handleHover(cellId));

            container.appendChild(cell);
        }
    }
}

function checkWin() {
    let filledCells = 0;
    let completedPaths = 0;
    const totalCells = 25; 
    const targetPaths = 5; 

    for (let id in gridData) {
        const element = document.getElementById(id);
        if (element && element.style.backgroundColor !== "") {
            filledCells++;
        }
    }

    const colors = ["yellow", "orange", "blue", "green", "red"];
    colors.forEach(clr => {
        const dots = Object.keys(gridData).filter(id => gridData[id].hasDot && gridData[id].color === clr);
        const startDotEl = document.getElementById(dots[0]);
        const endDotEl = document.getElementById(dots[1]);
        
        if (startDotEl.style.backgroundColor !== "" && 
            startDotEl.style.backgroundColor === endDotEl.style.backgroundColor) {
            completedPaths++;
        }
    });

    if (filledCells === totalCells && completedPaths === targetPaths) {
        setTimeout(() => {
            alert("Mubarak ho bhai! Aap Jeet Gaye! 🎉\nRules Followed: All connected, All boxes filled!");
        }, 100);
    }
}

function handleCellClick(id) {
    const cell = gridData[id];
    const element = document.getElementById(id);

    // CASE 1: Target dot par click karke path LOCK karna
    if (isDrawing && cell.hasDot && cell.color === selectedColor && id !== startCellId) {
        if (isAdjacent(lastHoveredId, id)) {
            element.style.backgroundColor = pathColors[selectedColor];
            console.log("Path Locked Successfully!");
            
            // Sab kuch reset magar rasta (color) wahi rahega
            isDrawing = false;
            isTargetReached = false; // Reset for next color
            selectedColor = null;
            startCellId = null;
            lastHoveredId = null;

            checkWin(); 
        }
        return;
    }

    // CASE 2: Naya rasta shuru karna (First Dot click)
    if (cell.hasDot) {
        clearPathByColor(cell.color); 
        selectedColor = cell.color;
        startCellId = id;
        lastHoveredId = id;
        isDrawing = true;
        isTargetReached = false; // Naya rasta shuru ho raha hai
        
        element.style.backgroundColor = pathColors[selectedColor];
    }
}

function handleHover(id) {
    // Agar drawing off hai, ya target touch ho chuka hai, toh aage mat badho
    if (!isDrawing || !selectedColor || isTargetReached) return;

    const cell = gridData[id];
    const element = document.getElementById(id);

    if (!isAdjacent(lastHoveredId, id)) return;

    // Crossing logic
    if (cell.color !== "" && cell.color !== selectedColor) {
        clearPathByColor(cell.color);
    }

    // Target dot detection
    if (cell.hasDot) {
        if (cell.color === selectedColor && id !== startCellId) {
            element.style.backgroundColor = pathColors[selectedColor];
            lastHoveredId = id;
            isTargetReached = true; // Hover yahi stop ho jayega, ab sirf click kaam karega
            console.log("Target touched. Now click to lock!");
        }
        return; 
    }

    // Normal path drawing
    element.style.backgroundColor = pathColors[selectedColor];
    gridData[id].color = selectedColor; 
    lastHoveredId = id;
}

function isAdjacent(id1, id2) {
    if (!id1 || !id2) return false;
    let r1 = parseInt(id1[0]), c1 = parseInt(id1[1]);
    let r2 = parseInt(id2[0]), c2 = parseInt(id2[1]);
    return (Math.abs(r1 - r2) + Math.abs(c1 - c2)) === 1;
}

function clearPathByColor(colorToClear) {
    if (!colorToClear) return;
    for (let id in gridData) {
        if (gridData[id].color === colorToClear) {
            const el = document.getElementById(id);
            if (el) el.style.backgroundColor = "";
            if (!gridData[id].hasDot) {
                gridData[id].color = ""; 
            }
        }
    }
}

function setupDots(config) {
    for (let id in config) {
        const targetCell = document.getElementById(id);
        
        if (targetCell && gridData[id]) {
            // 1. Dot element banao
            const dot = document.createElement('span');
            dot.className = 'dot';
            dot.style.backgroundColor = config[id];
            
            // 2. Cell mein dot add karo
            targetCell.appendChild(dot);
            
            // 3. gridData (Logic) ko update karo
            gridData[id].hasDot = true;
            gridData[id].color = config[id];
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    generateGrid(5, 5);
    const level1Data = {
        "11": "yellow", "31": "yellow",
        "15": "orange", "34": "orange",
        "23": "blue",   "45": "blue",
        "41": "green",  "44": "green",
        "51": "red",    "55": "red",
    };
    setupDots(level1Data);
});