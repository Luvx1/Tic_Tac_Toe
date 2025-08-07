# 🎮 Tic-Tac-Toe 3x3 - Modern Edition

A beautiful and feature-rich Tic-Tac-Toe game built with Python and Tkinter, featuring intelligent AI, modern UI design, and comprehensive statistics tracking.

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

### 🎯 Game Modes
- **Player vs Player (PvP)**: Classic two-player gameplay with alternating first moves
- **Player vs Computer (PvE)**: Challenge AI with three difficulty levels:
  - 🟢 **Easy**: Random moves
  - 🟡 **Medium**: 70% smart moves, 30% random
  - 🔴 **Hard**: Unbeatable AI using Minimax algorithm with Alpha-Beta pruning

### 🎨 Modern UI/UX
- **Beautiful Design**: Modern gradient backgrounds and smooth animations
- **Responsive Layout**: Full-screen interface with organized panels
- **Hover Effects**: Interactive buttons with visual feedback
- **Color-coded Players**: X (Blue) and O (Orange) for easy identification
- **Professional Typography**: Clean, readable fonts throughout

### ⏱️ Game Features
- **Turn Timer**: 10-second countdown for each move
- **Draw Requests**: PvP mode allows players to request draws
- **Auto-switching**: Alternating first player in PvP mode for fairness
- **Real-time Status**: Live game information and player turn indicators

### 📊 Statistics & Analytics
- **Comprehensive Tracking**: Win/loss/draw statistics for all game modes
- **Player Performance**: Individual player statistics in PvP mode
- **Win Rate Calculations**: Percentage-based performance metrics
- **Persistent Storage**: JSON-based score saving and loading
- **Statistics Reset**: Option to clear all game history

### 🤖 Intelligent AI
- **Minimax Algorithm**: Optimal move calculation for hard difficulty
- **Alpha-Beta Pruning**: Efficient search tree optimization
- **Adaptive Difficulty**: Three distinct AI personalities
- **Smart Decision Making**: Strategic gameplay at higher levels

## 🚀 Installation

### Prerequisites
- Python 3.6 or higher
- Tkinter (usually included with Python)

### Quick Start
1. **Clone the repository**
   ```bash
   git clone https://github.com/Luvx1/Tic_Tac_Toe.git
   cd Tic_Tac_Toe
   ```

2. **Run the game**
   ```terminal
   py tic_tac_toe.py
   ```

### Alternative Installation
If you don't have Python installed:
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Ensure "Add Python to PATH" is checked during installation
3. Follow the Quick Start steps above

## 📁 Project Structure

```
Tic-Tac-Toe/
├── tic_tac_toe.py          # Main game application
├── tic_tac_toe_scores.json # Statistics and scores storage
└── README.md               # This file
```

### Key Components

#### `tic_tac_toe.py`
- **ModernButton Class**: Custom button with hover effects
- **TicTacToe Class**: Main game logic and UI management
- **AI Implementation**: Minimax algorithm with Alpha-Beta pruning
- **Statistics System**: Score tracking and analytics
- **UI Components**: Modern interface with organized panels

#### `tic_tac_toe_scores.json`
- Stores game statistics in JSON format
- Tracks wins, losses, and draws for each mode
- Maintains individual player performance data
- Automatically created on first run

## 🛠️ Technical Details

### Algorithms
- **Minimax**: Recursive algorithm for optimal move calculation
- **Alpha-Beta Pruning**: Optimization technique to reduce search space
- **Game State Management**: Efficient board state tracking

### UI Framework
- **Tkinter**: Python's standard GUI toolkit
- **Custom Widgets**: Enhanced button and frame classes
- **Responsive Design**: Adaptive layout for different screen sizes

### Data Management
- **JSON Storage**: Human-readable score persistence
- **Error Handling**: Graceful handling of file operations
- **Statistics Calculation**: Real-time performance metrics

## 🎯 Features in Detail

### Smart AI System
The AI uses the Minimax algorithm with Alpha-Beta pruning:
- **Easy Mode**: Random moves for beginners
- **Medium Mode**: 70% optimal moves, 30% random for variety
- **Hard Mode**: Unbeatable AI using full Minimax search

### Statistics Tracking
- **Mode-specific Stats**: Separate tracking for PvP and each AI difficulty
- **Player Performance**: Individual win rates in PvP mode
- **Persistent Storage**: Scores saved between sessions
- **Visual Analytics**: Clean statistics display with percentages

### Modern Interface
- **Professional Design**: Clean, modern aesthetic
- **Intuitive Navigation**: Easy-to-use menus and controls
- **Visual Feedback**: Hover effects and color coding
- **Responsive Layout**: Adapts to different screen sizes
  
##📝 Game Interface

###👉 Main Interface
<img width="1916" height="895" alt="image" src="https://github.com/user-attachments/assets/3130afb8-b92b-4d60-8b65-20d2b92bd0fe" />
###👉 PvE Interface
<img width="1917" height="937" alt="image" src="https://github.com/user-attachments/assets/24fda271-ef64-46a0-ad48-7919d54ea3dc" />
###👉 PvE(Easy) Interface
<img width="1913" height="1013" alt="image" src="https://github.com/user-attachments/assets/9f5577c3-5b5d-41f2-9bc1-44bc884202ab" />
###👉 PvP Interface
<img width="1915" height="1011" alt="image" src="https://github.com/user-attachments/assets/1ede86e6-53ed-422a-bd82-5918bd8dd226" />


*Built with ❤️ using Python and Tkinter*
