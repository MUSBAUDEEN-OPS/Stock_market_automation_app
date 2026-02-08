# 📈 AI Stock Market Predictor - Streamlit Web App

An automated stock market prediction system that uses machine learning to forecast next-day closing prices with email notifications.

## 🌟 Features

### Core Functionality
- **Multi-Stock Analysis**: Analyze multiple stocks simultaneously
- **Real-Time Data**: Automatic data fetching from Yahoo Finance
- **AI Predictions**: Linear regression model for next-day price forecasting
- **Last 5 Days Summary**: Quick view of recent trading activity
- **60-Day Visualization**: Interactive charts showing actual vs predicted prices
- **Error Analysis**: Detailed prediction accuracy metrics
- **Trading Recommendations**: AI-generated trading guides based on predictions

### Email Automation
- **Daily Reports**: Automated emails after market close (4 PM EST)
- **Subscriber Management**: Built-in email subscription system
- **Comprehensive Reports**: All stock predictions in one email
- **Direct Links**: Quick access to detailed analysis on the web app

## 📋 Prerequisites

- Python 3.8 or higher
- GitHub account (for email automation)
- Streamlit account (for deployment)
- Gmail account (for sending emails) or other SMTP service

## 🚀 Quick Start

### 1. Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/stock-predictor-app.git
cd stock-predictor-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### 2. Deploy to Streamlit Cloud

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository and branch
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Get your app URL**: 
   - Your app will be available at: `https://your-app-name.streamlit.app`

### 3. Setup Email Automation

#### A. Configure Email Service (Gmail Example)

1. **Enable 2-Factor Authentication** on your Gmail account

2. **Generate App Password**:
   - Go to Google Account Settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
   - Save this password securely

#### B. Configure GitHub Secrets

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions → New repository secret

Add these secrets:

| Secret Name | Description | Example Value |
|------------|-------------|---------------|
| `STREAMLIT_APP_URL` | Your Streamlit app URL | `https://your-app.streamlit.app` |
| `SMTP_SERVER` | SMTP server address | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP port | `587` |
| `SENDER_EMAIL` | Your email address | `yourname@gmail.com` |
| `SENDER_PASSWORD` | App password from Gmail | `xxxx xxxx xxxx xxxx` |

#### C. Enable GitHub Actions

1. Go to repository → Actions tab
2. Enable workflows if prompted
3. The workflow will run automatically at 4:30 PM EST on weekdays
4. You can also trigger manually: Actions → Daily Stock Predictions Email → Run workflow

## 📁 Project Structure

```
stock-predictor-app/
│
├── app.py                          # Main Streamlit application
├── email_automation.py             # Email sending script
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
│
├── .github/
│   └── workflows/
│       └── daily_email.yml         # GitHub Actions workflow
│
└── subscribers.json                # Email subscribers (auto-created)
```

## 🎯 Usage Guide

### Selecting Stocks

1. **Sidebar**: Choose between "Multiple Stocks" or "Single Stock"
2. **Multi-Select**: Select multiple stocks for simultaneous analysis
3. **Date Range**: Adjust the historical data start date
4. **Visualization Window**: Set how many days to display (30-120)

### Understanding Predictions

**Prediction Card** shows:
- Current Close Price
- Predicted Next Close Price
- Expected Change ($ and %)
- Last Data Date
- Next Trading Day

**Last 5 Days Table**:
- Open, High, Low, Close prices
- Volume
- Daily change and percentage

**Model Performance**:
- RMSE (Root Mean Square Error)
- MAE (Mean Absolute Error)
- R² Score (model accuracy)

**Visualization**:
- Top Panel: Actual vs Predicted prices with next-day forecast
- Bottom Panel: Prediction errors over time

**Trading Recommendations**:
- Buy/Sell/Hold signals
- RSI analysis (overbought/oversold)
- Volatility assessment
- Risk warnings

### Email Subscriptions

1. Enter your email in the sidebar
2. Click "Subscribe"
3. Receive daily predictions after market close (4:30 PM EST)
4. Each email contains:
   - All stock predictions
   - Current and predicted prices
   - Expected changes
   - Direct links to detailed analysis

## 🔧 Customization

### Adding More Stocks

Edit `app.py`, modify the `POPULAR_STOCKS` dictionary:

```python
POPULAR_STOCKS = {
    "Technology": ["AAPL", "MSFT", "GOOGL", "YOUR_STOCK"],
    "Your Category": ["STOCK1", "STOCK2"],
}
```

### Changing Email Schedule

Edit `.github/workflows/daily_email.yml`:

```yaml
on:
  schedule:
    # Change cron expression
    # Format: minute hour day month day-of-week
    - cron: '30 21 * * 1-5'  # 4:30 PM EST on weekdays
```

**Cron Examples**:
- `30 21 * * 1-5` - Weekdays 4:30 PM EST
- `0 22 * * *` - Daily 5:00 PM EST
- `0 14 * * 1-5` - Weekdays 9:00 AM EST

### Adjusting Model Parameters

In `app.py`, find the `train_model` function:

```python
# Change regularization strength
model = Ridge(alpha=1.0, random_state=42)  # Increase alpha for more regularization

# Or use standard Linear Regression
from sklearn.linear_model import LinearRegression
model = LinearRegression()
```

## 📊 Technical Details

### Feature Engineering

The model uses 30+ technical indicators:
- **Moving Averages**: MA(5,10,20,50), EMA(12,26)
- **MACD**: MACD line and signal
- **RSI**: Relative Strength Index
- **Bollinger Bands**: Upper, lower, middle, width
- **Momentum**: 5, 10, 20-day momentum
- **Volatility**: 10, 30-day volatility
- **Volume**: Volume ratios and moving averages
- **Rate of Change**: 5, 10-day ROC

### Model Training

- **Algorithm**: Ridge Regression (L2 regularization)
- **Train/Test Split**: 80/20
- **Feature Scaling**: StandardScaler normalization
- **Validation**: RMSE, MAE, R² metrics

### Data Sources

- **Yahoo Finance**: Historical and real-time stock data via `yfinance`
- **Update Frequency**: Real-time when app is accessed
- **Historical Range**: Configurable (default: 2 years)

## ⚠️ Important Notes

### Market Hours
- US stock market: 9:30 AM - 4:00 PM EST
- Email automation runs at 4:30 PM EST (after market close)
- Predictions are for the next trading day

### Limitations
- Predictions are for **educational purposes only**
- Not financial advice
- Past performance doesn't guarantee future results
- Model accuracy varies by stock and market conditions

### Data Requirements
- Minimum 100 days of historical data required
- Model performs better with more historical data
- Some stocks may have insufficient data

## 🐛 Troubleshooting

### "Insufficient Data" Error
- Increase the date range in the sidebar
- Some newer stocks may not have enough history
- Try a different stock

### Email Not Sending
- Check GitHub Secrets are correctly configured
- Verify app password (not your regular password)
- Check GitHub Actions logs for errors
- Ensure SMTP settings are correct for your provider

### Slow Performance
- Analyzing many stocks takes longer
- Reduce number of stocks or date range
- Consider caching (see advanced customization)

### Yahoo Finance Connection Issues
- Yahoo Finance API can be rate-limited
- Wait a few minutes and try again
- Check internet connection

## 🔐 Security Best Practices

1. **Never commit secrets** to GitHub
2. Use **GitHub Secrets** for sensitive data
3. Use **app passwords**, not regular passwords
4. Regularly rotate app passwords
5. Keep dependencies updated

## 🚀 Advanced Features (Optional)

### Add Caching for Better Performance

```python
import streamlit as st

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_stock_data(ticker, start_date):
    return yf.download(ticker, start=start_date)
```

### Add More Email Providers

**SendGrid**:
```python
SMTP_SERVER = "smtp.sendgrid.net"
SMTP_PORT = 587
```

**Outlook**:
```python
SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = 587
```

**AWS SES**:
```python
SMTP_SERVER = "email-smtp.us-east-1.amazonaws.com"
SMTP_PORT = 587
```

### Database Integration

Store subscribers in a database instead of JSON:

```python
import sqlite3

def save_subscriber(email):
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS subscribers
                 (email TEXT PRIMARY KEY, subscribed_date TEXT)''')
    c.execute("INSERT OR IGNORE INTO subscribers VALUES (?, ?)",
              (email, datetime.now().isoformat()))
    conn.commit()
    conn.close()
```

## 🆘 Support

- **Issues**: Open an issue on GitHub
- **Questions**: Check existing issues or create new one
- **Contributions**: Pull requests welcome!

## 📜 License

This project is licensed under the MIT License.

## ⚖️ Disclaimer

**IMPORTANT**: This application is for educational and informational purposes only. It does not constitute financial advice, investment advice, trading advice, or any other type of advice. 

- Always do your own research
- Consult with a qualified financial advisor
- Never invest more than you can afford to lose
- Past performance does not guarantee future results
- The creators assume no responsibility for trading losses

## 🙏 Acknowledgments

- Yahoo Finance for providing free financial data
- Streamlit for the amazing web framework
- scikit-learn for machine learning tools

## 📧 Contact

For questions or suggestions, open an issue on GitHub.

---

**Made with ❤️ for educational purposes**
