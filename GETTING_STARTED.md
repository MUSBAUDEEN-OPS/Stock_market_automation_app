# 🎯 GETTING STARTED - Quick Guide

Welcome! This guide will help you get your Stock Market Predictor app up and running in minutes.

## 📋 What You'll Need

- [ ] Computer with internet connection
- [ ] Python 3.8+ installed ([Download here](https://www.python.org/downloads/))
- [ ] Gmail account (or other email service)
- [ ] GitHub account ([Sign up free](https://github.com))
- [ ] Streamlit account ([Sign up free](https://streamlit.io))

## 🚀 Three Steps to Success

### Step 1: Test Locally (5 minutes)

**Windows Users:**
```bash
# Double-click start.bat
# OR open Command Prompt in project folder and run:
start.bat
```

**Mac/Linux Users:**
```bash
# Open Terminal in project folder and run:
chmod +x start.sh
./start.sh
```

The app will open at http://localhost:8501

**Test the features:**
- ✅ Select a stock (try AAPL)
- ✅ Adjust date range
- ✅ View predictions and charts
- ✅ Check trading recommendations

### Step 2: Deploy to Internet (10 minutes)

#### A. Push to GitHub

```bash
# In your terminal/command prompt
git init
git add .
git commit -m "Initial commit"
git branch -M main

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/stock-predictor.git
git push -u origin main
```

#### B. Deploy on Streamlit

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your GitHub repository
4. Main file: `app.py`
5. Click "Deploy"
6. Wait 2-3 minutes
7. Your app is live! 🎉

Copy your app URL (like: https://your-app.streamlit.app)

### Step 3: Setup Email Notifications (15 minutes)

#### A. Generate Gmail App Password

1. Go to [Google Account](https://myaccount.google.com)
2. Security → 2-Step Verification (enable if not already)
3. Scroll to bottom → App passwords
4. Select "Mail" and your device
5. Copy the 16-character password
6. **Save it!** You'll need it next

#### B. Configure GitHub Secrets

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add these 5 secrets:

| Name | Value |
|------|-------|
| STREAMLIT_APP_URL | https://your-app.streamlit.app |
| SMTP_SERVER | smtp.gmail.com |
| SMTP_PORT | 587 |
| SENDER_EMAIL | your-email@gmail.com |
| SENDER_PASSWORD | (paste app password) |

#### C. Enable GitHub Actions

1. Go to repository → Actions tab
2. Click "I understand my workflows, go ahead and enable them"
3. Done! Emails will send daily at 4:30 PM EST

## ✅ Verify Everything Works

### Test Email Configuration

```bash
python test_config.py
```

This will:
- ✓ Check your email settings
- ✓ Test SMTP connection
- ✓ Send a test email (if you want)
- ✓ Verify data fetching works

### Manual Email Test

```bash
python email_automation.py
```

Check your inbox for the prediction email!

## 📱 Using the App

### For Single Stock Analysis
1. Sidebar → "Single Stock"
2. Select stock from dropdown
3. View prediction, charts, recommendations

### For Multiple Stocks
1. Sidebar → "Multiple Stocks"
2. Select multiple stocks
3. All analyses appear stacked
4. Scroll to compare

### Subscribe to Emails
1. Sidebar → Email Alerts section
2. Enter your email
3. Click Subscribe
4. You'll receive daily predictions after market close

## 🎨 Customization

### Add Your Favorite Stocks

Edit `app.py`, find `POPULAR_STOCKS`:

```python
POPULAR_STOCKS = {
    "My Favorites": ["YOUR", "FAVORITE", "STOCKS"],
    "Technology": ["AAPL", "MSFT", ...],
}
```

### Change Email Schedule

Edit `.github/workflows/daily_email.yml`:

```yaml
- cron: '30 21 * * 1-5'  # 4:30 PM EST weekdays
```

Change to your preferred time ([Cron Helper](https://crontab.guru))

### Customize Stocks in Emails

Edit `email_automation.py`, find `STOCKS`:

```python
STOCKS = ["AAPL", "MSFT", "YOUR", "PICKS"]
```

## 🐛 Common Issues & Solutions

### "Python not found"
**Solution:** Install Python from [python.org](https://python.org)

### "Module not found"
**Solution:** 
```bash
pip install -r requirements.txt
```

### "Authentication failed" (email)
**Solution:** 
- Make sure you're using **app password**, not regular password
- Enable 2-factor authentication first
- Generate new app password

### "Insufficient data for stock"
**Solution:**
- Increase date range in sidebar
- Try a different stock
- Stock might be too new

### GitHub Actions not running
**Solution:**
- Check if secrets are added correctly
- Verify workflow file is in `.github/workflows/`
- Check Actions tab for error messages

### App is slow
**Solution:**
- Reduce number of stocks analyzed
- Reduce date range
- Free tier has limited resources

## 📞 Get Help

### Documentation
- 📖 Full README: See `README.md`
- 🚀 Deployment Options: See `DEPLOYMENT_ALTERNATIVES.md`
- 💻 Your notebook: `standalone_predictor__1_.ipynb`

### Resources
- Streamlit Docs: https://docs.streamlit.io
- GitHub Actions: https://docs.github.com/actions
- Yahoo Finance: https://finance.yahoo.com

### Community
- Streamlit Forum: https://discuss.streamlit.io
- GitHub Issues: Open an issue in your repo
- Stack Overflow: Tag with `streamlit`, `yfinance`

## 🎓 Next Steps

Once everything works:

1. **Customize**: Add your favorite stocks
2. **Share**: Send app link to friends
3. **Monitor**: Check email predictions daily
4. **Improve**: Add more features (see README for ideas)
5. **Learn**: Study how the ML model works

## ⚠️ Important Reminders

- 📊 **Not Financial Advice**: Use for education only
- 🔐 **Protect Secrets**: Never commit .env or passwords
- 💰 **Free Tiers**: Be aware of usage limits
- 📧 **Spam**: Check spam folder for emails
- 🕐 **Market Hours**: Predictions update after market close

## 🎉 You're Ready!

Your stock predictor is now:
- ✅ Running locally
- ✅ Deployed online
- ✅ Sending daily emails
- ✅ Analyzing multiple stocks

**Start exploring and happy trading (responsibly)!** 📈

---

**Quick Links:**
- 🌐 Your App: (paste your Streamlit URL here)
- 💻 GitHub Repo: (paste your GitHub URL here)
- 📧 Email: (your email here)

**Remember:** This is an educational tool. Always do your own research and consult financial advisors before investing.
