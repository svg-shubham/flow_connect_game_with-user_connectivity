# 🧩 ConnectDots: Topological Logic Engine
> A high-performance, grid-based pathfinding puzzle engineered with Vanilla JS and Django.

[![Language](https://img.shields.io/badge/Language-JavaScript_ES6-yellow.svg)](https://js.org/)
[![Backend](https://img.shields.io/badge/Backend-Django_4.2-green.svg)](https://www.djangoproject.com/)
[![UI](https://img.shields.io/badge/UI-Glassmorphism-blue.svg)](#)

---

## 📺 Project Preview


## 🌟 Key Features
* **Dynamic Grid Scaling:** Supports $5 \times 5$ to $12 \times 12$ grids injected via Backend JSON.
* **Real-time Analytics:** Tracks moves, time-to-complete, and path efficiency.
* **Smart Validation:** Adjacency-based pathfinding with zero-latency collision detection.
* **Persistence:** Global leaderboard integration via Django Rest-based architecture.

---

## 🛠️ The "Engineering" Behind the Game

### 📍 Spatial Adjacency Logic
To maintain a smooth 60fps experience, I avoided heavy loops. Instead, I used **Manhattan Distance** for $O(1)$ move validation:
$$|r_1 - r_2| + |c_1 - c_2| = 1$$



### 📊 Backend Integration & Security
The engine communicates with a Django REST API to persist player metrics.
* **Data Integrity:** Implemented CSRF protection for all game-state transmissions.
* **Performance:** Optimized database queries for the Global Leaderboard.

---

## 🚀 Performance Metrics (Analytical Focus)
| Metric | Implementation | Benefit |
| :--- | :--- | :--- |
| **Pathfinding** | Adjacency Matrix | Zero-lag user interaction |
| **Win Logic** | Dual-Constraint Check | Prevents false-positive completions |
| **Data Sync** | Asynchronous Fetch | Smooth transitions without page reload |

---

## 📂 Project Structure
```bash
├── static/
│   ├── js/
│   │   ├── engine.js       # Core Game Logic & Adjacency
│   │   └── analytics.js    # Fetch API & Leaderboard Logic
│   └── css/
│       └── style.css       # Modern Glassmorphism UI
├── templates/              # Django Dynamic Templates
└── models.py               # Analytical Data Schema
💻 Installation
git clone https://github.com/yourusername/ConnectDots.git

pip install -r requirements.txt

python manage.py runserver
