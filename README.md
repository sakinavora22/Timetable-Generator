# Timetable Generator

An algorithmic timetable scheduling application built with Flask and Vanilla JavaScript.

## Features
- Dynamic scheduling algorithms including:
  - **Priority First (Greedy)**: Schedules highest priority subjects first
  - **Best Fit Search (Backtracking)**: Explores all possibilities to find a valid schedule
  - **Urgency Based (Priority Queue)**: Uses a max-heap to process urgent tasks
  - **Shortest Job First (SJF)**: Schedules subjects requiring the least time first
- Simple, modern, and clean UI
- API endpoints returning computation time and time complexity

## Requirements
- Python 3
- Flask
- Flask-CORS

## Installation
1. Clone the repository
2. Install the dependencies:
   ```bash
   pip install flask flask-cors
   ```

## Usage
Run the Flask server:
```bash
python app.py
```
Then open your browser and navigate to `http://localhost:5000/`.
