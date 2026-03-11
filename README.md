# 🧠 Single-File Turing Machine Simulator for Binary Operations

## 📌 Project Overview
This compact implementation features a **complete multi-tape Turing Machine simulator** in a single Python file, performing three core binary operations:
- Binary Addition
- Binary Subtraction (2's complement method)
- Binary Multiplication (via repeated addition)

## ✨ Key Features

### Core Functionality
- ✅ **All-in-one implementation** in a single Python file
- ➕ **Addition**, **➖ Subtraction**, **✖️ Multiplication** support
- 🧠 Unified state machine handling all operations
- 🏎️ **Optimized performance** despite single-file design

### Visualization Features
- 🎮 **Pygame-powered interface** with:
  - Multi-tape visualization
  - Animated head movements
  - Real-time state display
  - Operation progress tracking

## 🖥️ Interface Components

### Built-in Controls:
- **Tape Display**: Shows Input_1, Input_2, and Output tapes
- **State Indicator**: Current operation and phase
- **Execution Controls**:
  - Step-through execution
  - Continuous run mode
  - Pause/Resume
  - Reset functionality

## 🚀 Quick Start

### Requirements
- Python 3.6+
- Pygame 2.0+ (`pip install pygame`)

### Usage
```bash
python tm_engine.py
```

## 📋 File Structure
```
project/
└── tm_engine/
    └── tm_engine.py      # Complete simulator implementation
```

## 👥 Development Team
- **Shaheer Uddin Ahmed (23K-0649)**
- **Yahya Shaikh (23K-0718)**
- **Faizan Jawaid (23K-0688)**

## 📚 Educational Value
Demonstrates:
- Multi-tape Turing Machine principles
- Binary operation algorithms
- State transition systems
- Computational complexity

## 💡 Key Implementation Details
- **Unified State Machine**: Handles all operations through state transitions
- **Tape Management**: Simulates multiple tapes within single data structures
- **Visualization**: Integrated Pygame rendering for real-time feedback
- **Efficient Design**: Maintains clean architecture despite single-file constraint

Note: This single-file implementation contains all the functionality of a multi-tape Turing Machine simulator while being completely self-contained.
