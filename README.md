# Drink Market Simulator

A real-time web dashboard that simulates a stock market for 5 types of drinks. Prices update in whole dollars as orders are placed. Built with Python Flask and Flask-SocketIO.

## Features
- 5 drinks, each with a price in whole dollars
- When a drink is ordered, its price increases by $1 and all other drinks decrease by $1 (never below $1)
- Real-time updates for all connected clients
- Simple web UI for inputting orders and viewing prices

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python app.py
   ```
3. Open your browser to http://localhost:5000

---

This is a starter project. Customize as needed!