# 📐 Project Architecture & Overview

## 🎯 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     STOCK PREDICTOR SYSTEM                       │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐         ┌──────────────────┐
│  Yahoo Finance   │────────▶│   Data Layer     │
│   (yfinance)     │         │  - Fetch stocks  │
└──────────────────┘         │  - Historical    │
                             └────────┬─────────┘
                                      │
                                      ▼
                             ┌──────────────────┐
                             │  Feature Engine  │
                             │  - 30+ indicators│
                             │  - MA, EMA, RSI  │
                             │  - MACD, BB, etc │
                             └────────┬─────────┘
                                      │
                                      ▼
                             ┌──────────────────┐
                             │   ML Model       │
                             │  - Ridge Regress │
                             │  - Train/Test    │
                             │  - Predict       │
                             └────────┬─────────┘
                                      │
                    ┌─────────────────┴──────────────────┐
                    │                                    │
                    ▼                                    ▼
          ┌──────────────────┐              ┌──────────────────┐
          │  Streamlit UI    │              │  Email Service   │
          │  - Multi-stock   │              │  - Daily reports │
          │  - Visualizations│              │  - Subscribers   │
          │  - Predictions   │              │  - Auto send     │
          │  - Trading tips  │              └────────┬─────────┘
          └────────┬─────────┘                       │
                   │                                 │
                   ▼                                 ▼
          ┌──────────────────┐              ┌──────────────────┐
          │  User Browser    │              │ Email Subscribers│
          │  (Worldwide)     │              │   (Inbox)        │
          └──────────────────┘              └──────────────────┘
```

## 📊 Data Flow

```
1. USER ACTION
   └─▶ Selects stocks in Streamlit UI

2. DATA ACQUISITION
   └─▶ yfinance fetches historical data from Yahoo Finance
   └─▶ Data cleaned and validated

3. FEATURE ENGINEERING
   └─▶ 30+ technical indicators calculated:
       • Moving Averages (5,10,20,50 day)
       • EMA, MACD, RSI
       • Bollinger Bands
       • Momentum, Volatility
       • Volume ratios
       • Rate of Change

4. MODEL TRAINING
   └─▶ Features fed to Ridge Regression
   └─▶ 80/20 train/test split
   └─▶ Model optimized with L2 regularization

5. PREDICTION
   └─▶ Latest data used for next-day forecast
   └─▶ Confidence metrics calculated
   └─▶ Error analysis performed

6. VISUALIZATION
   └─▶ Interactive charts generated
   └─▶ Actual vs Predicted comparison
   └─▶ Error analysis graphs

7. TRADING RECOMMENDATIONS
   └─▶ AI analyzes prediction
   └─▶ Generates buy/sell/hold signals
   └─▶ RSI and volatility warnings

8. EMAIL AUTOMATION (Daily 4:30 PM EST)
   └─▶ GitHub Actions triggers script
   └─▶ All stocks analyzed
   └─▶ HTML email generated
   └─▶ Sent to all subscribers
```

## 📁 File Structure Explained

```
stock_predictor_app/
│
├── 📱 MAIN APPLICATION
│   └── app.py                      # Streamlit web interface
│                                   # - Multi-stock selector
│                                   # - Real-time predictions
│                                   # - Visualization engine
│                                   # - Trading recommendations
│
├── 📧 EMAIL AUTOMATION
│   ├── email_automation.py         # Daily prediction emails
│   │                               # - Processes all stocks
│   │                               # - Generates HTML reports
│   │                               # - Sends to subscribers
│   │
│   └── .github/workflows/
│       └── daily_email.yml         # GitHub Actions scheduler
│                                   # - Runs at 4:30 PM EST
│                                   # - Executes email_automation.py
│
├── ⚙️ CONFIGURATION
│   ├── requirements.txt            # Python dependencies
│   ├── .env.example                # Environment template
│   ├── .gitignore                  # Git exclusions
│   └── subscribers.json            # Email list (auto-created)
│
├── 🧪 TESTING & SETUP
│   ├── test_config.py              # Verify email & data setup
│   ├── start.sh                    # Quick start (Mac/Linux)
│   └── start.bat                   # Quick start (Windows)
│
└── 📚 DOCUMENTATION
    ├── README.md                   # Complete guide
    ├── GETTING_STARTED.md          # Quick start guide
    ├── DEPLOYMENT_ALTERNATIVES.md  # Other hosting options
    ├── ARCHITECTURE.md             # This file
    └── LICENSE                     # MIT License
```

## 🔧 Component Details

### 1. **Streamlit App (app.py)**

**Purpose:** User-facing web application

**Key Features:**
- Multi-stock selection (simultaneous analysis)
- Configurable date ranges
- Real-time data fetching
- Automatic feature engineering
- ML model training per stock
- Interactive visualizations
- Trading recommendations
- Email subscription system

**Tech Stack:**
- Streamlit (UI framework)
- Pandas (data manipulation)
- NumPy (numerical operations)
- Matplotlib/Seaborn (visualizations)
- Scikit-learn (ML models)
- yfinance (stock data)

### 2. **Email Automation (email_automation.py)**

**Purpose:** Daily prediction reports

**Features:**
- Analyzes 10 pre-selected stocks
- Generates comprehensive predictions
- Creates HTML email reports
- Sends to all subscribers
- Error handling and logging

**Workflow:**
```
1. Fetch latest data for all stocks
2. Engineer features for each
3. Train model for each stock
4. Generate predictions
5. Create HTML email
6. Load subscriber list
7. Send emails via SMTP
8. Log results
```

### 3. **GitHub Actions Workflow (daily_email.yml)**

**Purpose:** Automated scheduling

**Schedule:**
- Weekdays only (Monday-Friday)
- 4:30 PM EST (after market close at 4 PM)
- Converts to UTC for cron: 21:30

**Process:**
```
1. Checkout code from repository
2. Setup Python 3.10 environment
3. Install dependencies
4. Load secrets from GitHub
5. Execute email_automation.py
6. Upload logs (if errors)
7. Complete
```

### 4. **Feature Engineering**

**30+ Technical Indicators:**

| Category | Indicators |
|----------|-----------|
| **Moving Averages** | MA(5,10,20,50), EMA(12,26) |
| **Momentum** | MACD, Signal Line |
| **Oscillators** | RSI (14-day) |
| **Volatility** | Bollinger Bands (upper/lower/width) |
| **Volume** | Volume MA, Volume Ratio |
| **Price Action** | Daily Return, Price Change, Log Return |
| **Trends** | Momentum (5,10,20), ROC (5,10) |
| **Ranges** | High-Low Range, HL Percentage |

**Feature Engineering Pipeline:**
```python
Raw Stock Data
    ↓
Clean & Validate
    ↓
Calculate Indicators
    ↓
Remove Infinities/NaNs
    ↓
Create Target (next day close)
    ↓
Final Feature Matrix
```

### 5. **Machine Learning Model**

**Algorithm:** Ridge Regression (L2 Regularization)

**Why Ridge?**
- Prevents overfitting
- Handles multicollinearity (correlated features)
- More stable than basic linear regression
- Good for financial time series

**Training Process:**
```
1. Split data: 80% train, 20% test
2. Standardize features (StandardScaler)
3. Train Ridge model (alpha=1.0)
4. Validate on test set
5. Calculate metrics (RMSE, MAE, R²)
6. Use for predictions
```

**Performance Metrics:**
- **RMSE**: Root Mean Square Error (average error in $)
- **MAE**: Mean Absolute Error (average absolute error)
- **R²**: Coefficient of determination (model fit quality)

## 🔄 Deployment Flow

```
LOCAL DEVELOPMENT
    ↓
[Git Push to GitHub]
    ↓
GITHUB REPOSITORY
    ↓           ↓
    │     [GitHub Actions]
    │           ↓
    │     EMAIL AUTOMATION
    │     (Runs 4:30 PM EST)
    │           ↓
    │     [Sends predictions]
    │           ↓
    │     SUBSCRIBERS
    │
    ↓
[Deploy to Streamlit]
    ↓
STREAMLIT CLOUD
    ↓
WEB APPLICATION
(Public Access)
```

## 🎨 UI Components

### Main Dashboard
```
┌─────────────────────────────────────────┐
│     📈 AI Stock Market Predictor        │
├─────────────────────────────────────────┤
│                                         │
│  SIDEBAR                    MAIN AREA   │
│  ┌─────────────┐           ┌─────────┐ │
│  │Stock Select │           │ STOCK 1 │ │
│  │Date Range   │           │ ├─Pred  │ │
│  │Lookback     │           │ ├─Chart │ │
│  │Email Sub    │           │ └─Guide │ │
│  └─────────────┘           ├─────────┤ │
│                            │ STOCK 2 │ │
│                            │ ├─Pred  │ │
│                            │ ├─Chart │ │
│                            │ └─Guide │ │
│                            └─────────┘ │
└─────────────────────────────────────────┘
```

### Stock Analysis Card
```
┌──────────────────────────────────────┐
│  📊 STOCK TICKER                     │
├──────────────────────────────────────┤
│  Current: $XXX    Predicted: $XXX   │
│  Last Date: YYYY-MM-DD               │
│  Next Date: YYYY-MM-DD               │
├──────────────────────────────────────┤
│  📅 Last 5 Days Trading Table        │
├──────────────────────────────────────┤
│  🎯 Model Metrics (RMSE, MAE, R²)    │
├──────────────────────────────────────┤
│  📈 60-Day Visualization             │
│  • Actual vs Predicted               │
│  • Next-day forecast                 │
│  • Error analysis                    │
├──────────────────────────────────────┤
│  🎯 Trading Recommendations          │
│  • Buy/Sell/Hold signal              │
│  • RSI analysis                      │
│  • Volatility warning                │
└──────────────────────────────────────┘
```

## 🔐 Security Architecture

### Environment Variables
```
.env (local)          GitHub Secrets (production)
    ↓                         ↓
Application reads      Actions workflow reads
    ↓                         ↓
Never committed       Encrypted storage
```

### Data Protection
- No user passwords stored
- Subscriber emails in local JSON only
- SMTP credentials in environment only
- No financial transactions

## 📈 Scalability Considerations

### Current Capacity
- **Stocks per session:** Unlimited (performance depends on user's machine)
- **Email subscribers:** Unlimited (limited by SMTP provider)
- **Historical data:** 2+ years per stock
- **Predictions per day:** Once per stock

### Optimization Options

1. **Caching:**
   ```python
   @st.cache_data(ttl=3600)  # Cache for 1 hour
   def fetch_data(ticker):
       ...
   ```

2. **Database:**
   Replace JSON with SQLite/PostgreSQL for subscribers

3. **Async Processing:**
   Use asyncio for concurrent stock analysis

4. **CDN:**
   Store charts in cloud storage

## 🧪 Testing Strategy

1. **Unit Tests:** Individual functions
2. **Integration Tests:** Email sending
3. **Manual Tests:** UI functionality
4. **Configuration Test:** `test_config.py`

## 📊 Success Metrics

### Application
- Prediction accuracy (R² > 0.7)
- Response time (< 5 seconds per stock)
- Uptime (99%+)

### Email Service
- Delivery rate (95%+)
- Open rate
- Click-through rate

## 🚀 Future Enhancements

Possible improvements:
1. More ML models (LSTM, Random Forest)
2. Sentiment analysis (news, tweets)
3. Portfolio optimization
4. Backtesting engine
5. Mobile app
6. Real-time WebSocket updates
7. User accounts & portfolios
8. Premium features

## 📚 Technical Dependencies

### Core Libraries
```
streamlit       → Web framework
pandas          → Data manipulation
numpy           → Numerical computing
yfinance        → Stock data API
matplotlib      → Plotting
seaborn         → Statistical viz
scikit-learn    → ML algorithms
python-dotenv   → Environment config
```

### Infrastructure
```
GitHub          → Code repository & Actions
Streamlit Cloud → Web hosting
SMTP Server     → Email delivery
```

## 🎓 Learning Resources

- **Streamlit:** https://docs.streamlit.io
- **Machine Learning:** scikit-learn.org
- **Finance:** investopedia.com
- **GitHub Actions:** docs.github.com/actions

---

**Architecture Version:** 1.0  
**Last Updated:** 2024  
**Maintained by:** Stock Predictor Team
