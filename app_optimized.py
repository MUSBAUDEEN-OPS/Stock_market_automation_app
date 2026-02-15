import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings

warnings.filterwarnings("ignore")
plt.style.use("seaborn-v0_8-darkgrid")
sns.set_palette("husl")

# Page configuration
st.set_page_config(
    page_title="Stock Market Predictor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .trading-guide {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        color: #000000;
    }
    .stock-divider {
        border-top: 3px solid #e0e0e0;
        margin: 3rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================================================================================
# STOCK SELECTION DATA
# ==================================================================================
POPULAR_STOCKS = {
    "Technology": ["AAPL", "MSFT", "GOOGL", "META", "NVDA", "TSLA", "AMD", "INTC", "CRM", "ORCL"],
    "Finance": ["JPM", "BAC", "WFC", "GS", "MS", "C", "BLK", "AXP", "SCHW", "USB"],
    "Healthcare": ["JNJ", "UNH", "PFE", "ABBV", "TMO", "MRK", "ABT", "DHR", "LLY", "AMGN"],
    "Consumer": ["AMZN", "WMT", "HD", "MCD", "NKE", "SBUX", "TGT", "LOW", "COST", "DG"],
    "Energy": ["XOM", "CVX", "COP", "SLB", "EOG", "MPC", "PSX", "VLO", "OXY", "HAL"],
    "Industrial": ["BA", "CAT", "GE", "HON", "UPS", "LMT", "MMM", "DE", "RTX", "EMR"],
}

ALL_STOCKS = []
for category in POPULAR_STOCKS.values():
    ALL_STOCKS.extend(category)

# ==================================================================================
# CACHED FUNCTIONS - PREVENT RECOMPUTATION
# ==================================================================================

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_stock_data(TICKER, START_DATE):
    """Fetch stock data from Yahoo Finance - CACHED"""
    df_raw = yf.download(
        TICKER,
        start=START_DATE,
        progress=False,
        repair=True
    )
    
    
    if isinstance(df_raw.columns, pd.MultiIndex):
        df_raw.columns = df_raw.columns.get_level_values(0)
    
    return df_raw

@st.cache_data
def engineer_features(df_raw):
    """Engineer technical indicators and features - CACHED"""
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
    
    # Clean data
    df = df.replace([np.inf, -np.inf], np.nan).dropna()
    
    return df

@st.cache_resource  # Cache the trained model
def train_model(_df):
    """Train Ridge Regression model - CACHED"""
    exclude = ["Open", "High", "Low", "Close", "Volume", "Adj Close", "Target"]
    feature_cols = [c for c in _df.columns if c not in exclude]
    
    X = _df[feature_cols]
    y = _df["Target"]
    
    # Train-test split
    split = int(len(X) * 0.8)
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]
    
    # Scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train
    model = Ridge(alpha=1.0, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    test_pred = model.predict(X_test_scaled)
    metrics = {
        "rmse": np.sqrt(mean_squared_error(y_test, test_pred)),
        "mae": mean_absolute_error(y_test, test_pred),
        "r2": r2_score(y_test, test_pred)
    }
    
    return model, scaler, feature_cols, metrics

# ==================================================================================
# PREDICTION FUNCTION
# ==================================================================================
def get_next_trading_day(last_date):
    """Calculate the next trading day (skip weekends)"""
    next_day = last_date + timedelta(days=1)
    
    # Skip weekends (Saturday=5, Sunday=6)
    while next_day.weekday() >= 5:
        next_day = next_day + timedelta(days=1)
    
    return next_day

def make_prediction(df, model, scaler, feature_cols):
    """Make next day prediction"""
    latest = df.iloc[-1:][feature_cols]
    latest_scaled = scaler.transform(latest)
    next_day_prediction = model.predict(latest_scaled)[0]
    
    current_price = df["Close"].iloc[-1]
    change = next_day_prediction - current_price
    change_pct = (change / current_price) * 100
    
    last_date = df.index[-1]
    
    # Check if last_date is today or in the future
    today = pd.Timestamp.now().normalize()
    
    if last_date.normalize() >= today - pd.Timedelta(days=1):
        # If data is current (today or future), next trading day is tomorrow
        next_date = get_next_trading_day(today)
    else:
        # Data is old, next date is after the last date we have
        next_date = get_next_trading_day(today)
    
    return {
        "predicted_price": next_day_prediction,
        "current_price": current_price,
        "change": change,
        "change_pct": change_pct,
        "last_date": last_date,
        "next_date": next_date,
        "trend": "BULLISH 📈" if change > 0 else "BEARISH 📉"
    }

# ==================================================================================
# VISUALIZATION FUNCTION
# ==================================================================================
def create_visualization(df, model, scaler, feature_cols, prediction_data, lookback_days):
    """Create actual vs predicted visualization"""
    recent_df = df.tail(lookback_days + 1).copy()
    
    # Generate predictions
    X_recent = recent_df[feature_cols]
    X_recent_scaled = scaler.transform(X_recent)
    recent_pred = model.predict(X_recent_scaled)
    
    dates = recent_df.index.tolist()
    actual = recent_df["Close"].tolist()
    predicted = recent_pred.tolist()
    
    # Add next day
    next_date = prediction_data["next_date"]
    dates_extended = dates + [next_date]
    actual_extended = actual + [None]
    predicted_extended = predicted + [prediction_data["predicted_price"]]
    
    # Create figure
    fig, axes = plt.subplots(2, 1, figsize=(16, 10))
    
    # Top Panel: Actual vs Predicted
    ax1 = axes[0]
    ax1.plot(dates, actual, label='Actual Close Price', linewidth=2.5, 
             color='#2E86AB', marker='o', markersize=4, alpha=0.8)
    ax1.plot(dates, predicted, label='Predicted Close Price', linewidth=2.5,
             color='#A23B72', linestyle='--', marker='s', markersize=4, alpha=0.8)
    ax1.plot([dates[-1], next_date], [predicted[-1], prediction_data["predicted_price"]],
             linewidth=3.5, color='#F18F01', marker='*', markersize=18,
             label='Next Day Forecast', zorder=5)
    
    ax1.annotate(f'${prediction_data["predicted_price"]:.2f}',
                xy=(next_date, prediction_data["predicted_price"]),
                xytext=(15, 15), textcoords='offset points',
                fontsize=12, fontweight='bold', color='#F18F01',
                bbox=dict(boxstyle='round,pad=0.6', facecolor='yellow',
                         alpha=0.8, edgecolor='#F18F01', linewidth=2.5))
    
    ax1.axvspan(dates[-1], next_date, alpha=0.15, color='orange', label='Forecast Period')
    ax1.set_title('Actual vs Predicted Price with Next-Day Forecast',
                 fontsize=16, fontweight='bold', pad=20)
    ax1.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Price ($)', fontsize=12, fontweight='bold')
    ax1.legend(loc='best', fontsize=11, framealpha=0.95)
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # Bottom Panel: Error Analysis
    ax2 = axes[1]
    errors = np.array(actual) - np.array(predicted)
    colors = ['#EF476F' if e < 0 else '#06D6A0' for e in errors]
    ax2.bar(dates, errors, color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
    
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=1.5)
    mean_error = np.mean(errors)
    ax2.axhline(y=mean_error, color='blue', linestyle='--', linewidth=2,
               label=f'Mean Error: ${mean_error:.2f}')
    
    ax2.set_title('Prediction Error (Actual - Predicted)',
                 fontsize=16, fontweight='bold', pad=20)
    ax2.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Error ($)', fontsize=12, fontweight='bold')
    ax2.legend(loc='best', fontsize=11, framealpha=0.95)
    ax2.grid(True, alpha=0.3, linestyle='--', axis='y')
    
    # Metrics
    rmse = np.sqrt(np.mean(errors**2))
    mae = np.mean(np.abs(errors))
    mape = np.mean(np.abs(errors / np.array(actual))) * 100
    
    metrics_text = f'Performance Metrics:\nRMSE: ${rmse:.2f}\nMAE: ${mae:.2f}\nMAPE: {mape:.2f}%'
    ax2.text(0.02, 0.98, metrics_text, transform=ax2.transAxes,
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat',
                     alpha=0.9, edgecolor='black', linewidth=1.5),
            fontfamily='monospace')
    
    plt.tight_layout()
    return fig

    

# ==================================================================================
# TRADING GUIDE GENERATOR
# ==================================================================================
def generate_trading_guide(prediction_data, df):
    """Generate AI trading recommendations"""
    guide = []
    
    change_pct = prediction_data["change_pct"]
    rsi = df["RSI"].iloc[-1]
    current_price = prediction_data["current_price"]
    predicted_price = prediction_data["predicted_price"]
    
    # Main recommendation
    guide.append(f"**🎯 PREDICTION: {prediction_data['trend']}**")
    guide.append(f"- Expected Change: **{change_pct:+.2f}%** (${prediction_data['change']:+.2f})")
    guide.append("")
    
    # Action recommendation
    if change_pct > 2:
        action = "🟢 **STRONG BUY SIGNAL**"
        guide.append(action)
        guide.append("- Consider entering a long position")
        guide.append(f"- Target entry: ${current_price:.2f}")
        guide.append(f"- Target exit: ${predicted_price:.2f}")
    elif change_pct > 0.5:
        action = "🟢 **BUY SIGNAL**"
        guide.append(action)
        guide.append("- Moderate bullish opportunity")
        guide.append(f"- Entry zone: ${current_price * 0.99:.2f} - ${current_price:.2f}")
    elif change_pct < -2:
        action = "🔴 **STRONG SELL SIGNAL**"
        guide.append(action)
        guide.append("- Consider reducing position or shorting")
        guide.append(f"- Exit near: ${current_price:.2f}")
    elif change_pct < -0.5:
        action = "🔴 **SELL SIGNAL**"
        guide.append(action)
        guide.append("- Moderate bearish pressure")
        guide.append("- Consider taking profits or waiting")
    else:
        action = "🟡 **HOLD**"
        guide.append(action)
        guide.append("- Minimal price movement expected")
        guide.append("- Wait for clearer signals")
    
    guide.append("")
    
    # RSI analysis
    guide.append("**📊 Technical Indicators:**")
    if rsi > 70:
        guide.append(f"- RSI: {rsi:.1f} (Overbought - Potential reversal)")
    elif rsi < 30:
        guide.append(f"- RSI: {rsi:.1f} (Oversold - Potential bounce)")
    else:
        guide.append(f"- RSI: {rsi:.1f} (Neutral)")
    
    guide.append("")
    guide.append("**⚠️ RISK DISCLAIMER:**")
    guide.append("This is an AI-generated prediction for educational purposes only.")
    guide.append("Always do your own research and never invest more than you can afford to lose.")
    guide.append("Past performance does not guarantee future results.")
    
    return "\n".join(guide)

# ==================================================================================
# LAST 5 DAYS TRADING DATA
# ==================================================================================
def display_last_5_days(df):
    """Display last 5 days of trading data"""
    last_5 = df[["Open", "High", "Low", "Close", "Volume"]].tail(5).copy()
    last_5["Change"] = last_5["Close"].diff()
    last_5["Change %"] = last_5["Close"].pct_change() * 100
    
    # Format
    last_5.index = last_5.index.strftime('%Y-%m-%d')
    last_5["Volume"] = last_5["Volume"].apply(lambda x: f"{x:,.0f}")
    
    for col in ["Open", "High", "Low", "Close", "Change"]:
        last_5[col] = last_5[col].apply(lambda x: f"${x:.2f}")
    
    last_5["Change %"] = last_5["Change %"].apply(lambda x: f"{x:+.2f}%" if pd.notna(x) else "N/A")
    
    return last_5

# ==================================================================================
# MAIN APP
# ==================================================================================
def main():
    # Header
    st.markdown('<h1 class="main-header">📈 AI Stock Market Predictor</h1>', unsafe_allow_html=True)
    st.markdown("### Automated Next-Day Stock Price Prediction using Machine Learning")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Stock selection
        st.subheader("📊 Select Stocks")
        selection_mode = st.radio("Selection Mode:", ["Single Stock", "Multiple Stocks"])
        
        if selection_mode == "Multiple Stocks":
            selected_stocks = st.multiselect(
                "Choose stocks to analyze:",
                options=ALL_STOCKS,
                default=["AAPL"],
                max_selections=3  # Limit to prevent overload
            )
        else:
            selected_stock = st.selectbox("Choose a stock:", ALL_STOCKS, index=0)
            selected_stocks = [selected_stock]
        
        # Date range
        st.subheader("📅 Date Range")
        START_DATE = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=365*2),
            max_value=datetime.now()
        )
        
        # Lookback days for visualization
        lookback_days = st.slider("Visualization Window (days)", 30, 120, 60)
        
        st.markdown("---")
        st.markdown("**💡 How it works:**")
        st.markdown("""
        1. Select stocks to analyze
        2. Data fetched automatically from Yahoo Finance
        3. AI model trained on historical data
        4. Next-day predictions generated
        5. Trading recommendations provided
        """)
        
        st.info("💾 Data is cached for 1 hour to improve performance")
    
    # Main content
    if not selected_stocks:
        st.warning("⚠️ Please select at least one stock from the sidebar")
        return
    
    # Process each stock
    for idx, ticker in enumerate(selected_stocks):
        if idx > 0:
            st.markdown('<div class="stock-divider"></div>', unsafe_allow_html=True)
        
        st.markdown(f"## 📊 {ticker} - Stock Analysis")
        
        with st.spinner(f"🔄 Fetching and analyzing {ticker} data..."):
            try:
                # Fetch data (CACHED)
                st.cache_data.clear()
                df_raw = fetch_stock_data(TICKER, START_DATE.strftime("%Y-%m-%d"))
                
                if len(df_raw) < 100:
                    st.error(f"❌ Insufficient data for {ticker}. Need at least 100 days.")
                    continue
                
                # Engineer features (CACHED)
                df = engineer_features(df_raw)
                
                # Train model (CACHED)
                model, scaler, feature_cols, metrics = train_model(df)
                
                # Make prediction
                prediction_data = make_prediction(df, model, scaler, feature_cols)
                
                # Display prediction card
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Current Close",
                        f"${prediction_data['current_price']:.2f}",
                        help="Latest closing price"
                    )
                
                with col2:
                    st.metric(
                        "Predicted Next Close",
                        f"${prediction_data['predicted_price']:.2f}",
                        f"{prediction_data['change_pct']:+.2f}%",
                        delta_color="normal" if prediction_data['change_pct'] > 0 else "inverse"
                    )
                
                with col3:
                    st.metric(
                        "Last Data Date",
                        prediction_data['last_date'].strftime('%Y-%m-%d')
                    )
                
                with col4:
                    st.metric(
                        "Next Trading Day",
                        prediction_data['next_date'].strftime('%Y-%m-%d')
                    )
                
                # Last 5 days trading data
                st.subheader("📅 Last 5 Days Trading Summary")
                last_5_days = display_last_5_days(df)
                st.dataframe(last_5_days, use_container_width=True)
                
                # Model performance
                with st.expander("🎯 Model Performance Metrics"):
                    met_col1, met_col2, met_col3 = st.columns(3)
                    with met_col1:
                        st.metric("RMSE", f"${metrics['rmse']:.2f}")
                    with met_col2:
                        st.metric("MAE", f"${metrics['mae']:.2f}")
                    with met_col3:
                        st.metric("R² Score", f"{metrics['r2']:.4f}")
                
                # Visualization
                st.subheader(f"📈 {lookback_days}-Day Analysis & Forecast")
                fig = create_visualization(df, model, scaler, feature_cols, prediction_data, lookback_days)
                st.pyplot(fig)
                plt.close()
                
                # Trading guide
                st.subheader("🎯 AI Trading Recommendations")
                trading_guide = generate_trading_guide(prediction_data, df)
                st.markdown(f'<div class="trading-guide">{trading_guide}</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Error processing {ticker}: {str(e)}")
                continue
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; padding: 2rem;'>
        <p><strong>⚠️ Disclaimer:</strong> This tool is for educational and informational purposes only.</p>
        <p>Not financial advice. Always consult with a qualified financial advisor before making investment decisions.</p>
        <p>Past performance does not guarantee future results.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
