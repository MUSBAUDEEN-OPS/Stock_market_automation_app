import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings("ignore")

# ==================================================================================
# CONFIGURATION
# ==================================================================================
STREAMLIT_APP_URL = os.getenv("STREAMLIT_APP_URL", "https://your-app.streamlit.app")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# Stocks to analyze
STOCKS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "JPM", "BAC", "JNJ"]

# ==================================================================================
# FEATURE ENGINEERING
# ==================================================================================
def engineer_features(df_raw):
    """Engineer technical indicators"""
    df = df_raw.copy()
    
    # Moving Averages
    df["MA_5"] = df["Close"].rolling(5).mean()
    df["MA_10"] = df["Close"].rolling(10).mean()
    df["MA_20"] = df["Close"].rolling(20).mean()
    df["MA_50"] = df["Close"].rolling(50).mean()
    
    # Exponential Moving Averages
    df["EMA_12"] = df["Close"].ewm(span=12, adjust=False).mean()
    df["EMA_26"] = df["Close"].ewm(span=26, adjust=False).mean()
    
    # MACD
    df["MACD"] = df["EMA_12"] - df["EMA_26"]
    df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    
    # RSI
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))
    
    # Bollinger Bands
    df["BB_Middle"] = df["Close"].rolling(20).mean()
    bb_std = df["Close"].rolling(20).std()
    df["BB_Upper"] = df["BB_Middle"] + (2 * bb_std)
    df["BB_Lower"] = df["BB_Middle"] - (2 * bb_std)
    df["BB_Width"] = df["BB_Upper"] - df["BB_Lower"]
    
    # Price Changes
    df["Daily_Return"] = df["Close"].pct_change()
    df["Price_Change"] = df["Close"].diff()
    df["Log_Return"] = np.log(df["Close"] / df["Close"].shift(1))
    
    # Volume Metrics
    df["Volume_MA_10"] = df["Volume"].rolling(10).mean()
    df["Volume_Ratio"] = df["Volume"] / df["Volume_MA_10"]
    
    # Volatility
    df["Volatility_10"] = df["Daily_Return"].rolling(10).std()
    df["Volatility_30"] = df["Daily_Return"].rolling(30).std()
    
    # Momentum
    df["Momentum_5"] = df["Close"] - df["Close"].shift(5)
    df["Momentum_10"] = df["Close"] - df["Close"].shift(10)
    df["Momentum_20"] = df["Close"] - df["Close"].shift(20)
    
    # Rate of Change
    df["ROC_5"] = ((df["Close"] - df["Close"].shift(5)) / df["Close"].shift(5)) * 100
    df["ROC_10"] = ((df["Close"] - df["Close"].shift(10)) / df["Close"].shift(10)) * 100
    
    # High-Low Range
    df["HL_Range"] = df["High"] - df["Low"]
    df["HL_Pct"] = (df["HL_Range"] / df["Close"]) * 100
    
    # Target
    df["Target"] = df["Close"].shift(-1)
    
    # Clean
    df = df.replace([np.inf, -np.inf], np.nan).dropna()
    
    return df

# ==================================================================================
# TRAIN AND PREDICT
# ==================================================================================
def train_and_predict(ticker, start_date="2015-01-01"):
    """Train model and make prediction for a stock"""
    try:
        # Fetch data
        df_raw = yf.download(
            ticker,
            start=start_date,
            end=datetime.now().strftime("%Y-%m-%d"),
            progress=False
        )
        
        if isinstance(df_raw.columns, pd.MultiIndex):
            df_raw.columns = df_raw.columns.get_level_values(0)
        
        if len(df_raw) < 100:
            return None
        
        # Engineer features
        df = engineer_features(df_raw)
        
        # Prepare data
        exclude = ["Open", "High", "Low", "Close", "Volume", "Adj Close", "Target"]
        feature_cols = [c for c in df.columns if c not in exclude]
        
        X = df[feature_cols]
        y = df["Target"]
        
        # Train
        split = int(len(X) * 0.8)
        X_train = X.iloc[:split]
        y_train = y.iloc[:split]
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        
        model = Ridge(alpha=1.0, random_state=42)
        model.fit(X_train_scaled, y_train)
        
        # Predict
        latest = df.iloc[-1:][feature_cols]
        latest_scaled = scaler.transform(latest)
        next_day_prediction = model.predict(latest_scaled)[0]
        
        current_price = df["Close"].iloc[-1]
        change = next_day_prediction - current_price
        change_pct = (change / current_price) * 100
        
        last_date = df.index[-1]
        next_date = last_date + timedelta(days=1)
        
        return {
            "ticker": ticker,
            "current_price": current_price,
            "predicted_price": next_day_prediction,
            "change": change,
            "change_pct": change_pct,
            "last_date": last_date.strftime("%Y-%m-%d"),
            "next_date": next_date.strftime("%Y-%m-%d")
        }
    
    except Exception as e:
        print(f"Error processing {ticker}: {e}")
        return None

# ==================================================================================
# EMAIL GENERATION
# ==================================================================================
def generate_email_html(predictions):
    """Generate HTML email content"""
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px;
                margin-bottom: 30px;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
            }}
            .date {{
                color: #f0f0f0;
                margin-top: 10px;
            }}
            .stock-card {{
                background: #f8f9fa;
                border-left: 5px solid #667eea;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 5px;
            }}
            .stock-header {{
                font-size: 24px;
                font-weight: bold;
                color: #667eea;
                margin-bottom: 15px;
            }}
            .metrics {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
                margin-top: 15px;
            }}
            .metric {{
                background: white;
                padding: 15px;
                border-radius: 5px;
                border: 1px solid #ddd;
            }}
            .metric-label {{
                font-size: 12px;
                color: #666;
                text-transform: uppercase;
            }}
            .metric-value {{
                font-size: 20px;
                font-weight: bold;
                margin-top: 5px;
            }}
            .positive {{
                color: #28a745;
            }}
            .negative {{
                color: #dc3545;
            }}
            .cta-button {{
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 15px;
                font-weight: bold;
            }}
            .footer {{
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 2px solid #ddd;
                color: #666;
                font-size: 12px;
            }}
            .disclaimer {{
                background: #fff3cd;
                border: 1px solid #ffc107;
                padding: 15px;
                border-radius: 5px;
                margin-top: 30px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📈 Daily Stock Market Predictions</h1>
            <p class="date">Report Generated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
        </div>
    """
    
    for pred in predictions:
        if pred is None:
            continue
        
        change_class = "positive" if pred["change_pct"] >= 0 else "negative"
        change_arrow = "↑" if pred["change_pct"] >= 0 else "↓"
        
        html += f"""
        <div class="stock-card">
            <div class="stock-header">{pred['ticker']}</div>
            <div class="metrics">
                <div class="metric">
                    <div class="metric-label">Current Close</div>
                    <div class="metric-value">${pred['current_price']:.2f}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Predicted Next Close</div>
                    <div class="metric-value {change_class}">
                        ${pred['predicted_price']:.2f} {change_arrow}
                    </div>
                </div>
                <div class="metric">
                    <div class="metric-label">Expected Change</div>
                    <div class="metric-value {change_class}">
                        {pred['change_pct']:+.2f}% (${pred['change']:+.2f})
                    </div>
                </div>
                <div class="metric">
                    <div class="metric-label">Next Trading Day</div>
                    <div class="metric-value">{pred['next_date']}</div>
                </div>
            </div>
            <a href="{STREAMLIT_APP_URL}?stock={pred['ticker']}" class="cta-button">
                View Full Analysis →
            </a>
        </div>
        """
    
    html += f"""
        <div class="disclaimer">
            <strong>⚠️ Disclaimer:</strong> These predictions are generated by AI for educational purposes only. 
            This is not financial advice. Always do your own research and consult with a qualified financial 
            advisor before making investment decisions. Past performance does not guarantee future results.
        </div>
        
        <div class="footer">
            <p><strong>AI Stock Market Predictor</strong></p>
            <p>You're receiving this because you subscribed to daily predictions.</p>
            <p><a href="{STREAMLIT_APP_URL}">Visit Dashboard</a> | 
               <a href="{STREAMLIT_APP_URL}">Unsubscribe</a></p>
        </div>
    </body>
    </html>
    """
    
    return html

# ==================================================================================
# SEND EMAIL
# ==================================================================================
def send_email(to_email, subject, html_content):
    """Send email via SMTP"""
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")
        return False

# ==================================================================================
# MAIN FUNCTION
# ==================================================================================
def main():
    """Main execution function"""
    print(f"Starting daily prediction email task at {datetime.now()}")
    
    # Generate predictions for all stocks
    print("Generating predictions...")
    predictions = []
    for ticker in STOCKS:
        print(f"  Processing {ticker}...")
        pred = train_and_predict(ticker)
        if pred:
            predictions.append(pred)
            print(f"    ✓ {ticker}: ${pred['current_price']:.2f} → ${pred['predicted_price']:.2f}")
    
    print(f"\nSuccessfully generated {len(predictions)} predictions")
    
    # Load subscribers
    subscribers_file = "subscribers.json"
    if not os.path.exists(subscribers_file):
        print("No subscribers found")
        return
    
    with open(subscribers_file, 'r') as f:
        subscribers = json.load(f)
    
    print(f"Found {len(subscribers)} subscribers")
    
    # Generate email
    html_content = generate_email_html(predictions)
    subject = f"📈 Daily Stock Predictions - {datetime.now().strftime('%B %d, %Y')}"
    
    # Send to all subscribers
    success_count = 0
    for email in subscribers:
        print(f"Sending to {email}...")
        if send_email(email, subject, html_content):
            success_count += 1
            print(f"  ✓ Sent successfully")
        else:
            print(f"  ✗ Failed")
    
    print(f"\nEmail task completed: {success_count}/{len(subscribers)} emails sent successfully")

if __name__ == "__main__":
    main()
