# Stock-Portfolio-Tracker

A Python/Streamlit web application for tracking stock portfolios and visualising its performance over time to calculate overall returns, though the Yahoo Finance API.

Features:
- Supports investments in multiple currencies with automatic conversion to GBP
- Add multiple stock investments
- Tracks current value and profits for each investment
- Built using Streamlit for responsive web interface

### Installation

Clone repository
```bash
git clone https://github.com/anishn1/Stock-Portfolio-Tracker.git
cd Stock-Portfolio-Tracker
```

Install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
```

Run application
```bash
streamlit run tracker.py
```
### Usage

Enter the stock ticker, date of investment, and the amount invested in GDP.
To track another stock for your portfolio, click "➕ Add Another Investment"
Click "Track Portfolio" to calculate current profit/loss and visualize performance.
Use ❌ buttons next to rows to remove any investment to stop tracking it.

### Future Additions

- Store investments in database using SQL so user does not have to retype in new sessions
- Candlestick chart type for performance visualisation

