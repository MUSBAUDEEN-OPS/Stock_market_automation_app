# 🎥 Video Tutorial Script - Stock Predictor Setup

**Total Duration:** ~30 minutes  
**Difficulty:** Beginner-Friendly  
**Goal:** Complete working stock predictor with email automation

---

## 📺 PART 1: Introduction (2 min)

**[SCREEN: Show finished app running]**

"Welcome! In this tutorial, we'll build an AI-powered stock market predictor that:
- Analyzes multiple stocks simultaneously
- Uses machine learning to predict next-day prices
- Sends daily email reports automatically
- All completely free using Streamlit and GitHub!"

**[SCREEN: Show example email]**

"By the end, you'll have a professional stock predictor deployed online, and it'll email you predictions every day after market close."

**[SCREEN: Requirements checklist]**

"Here's what you'll need:
✓ A computer (Windows, Mac, or Linux)
✓ Python 3.8 or newer installed
✓ A free GitHub account
✓ A free Streamlit account
✓ A Gmail account (or any email service)
✓ About 30 minutes"

"Don't worry if you're not technical - I'll guide you through every step!"

---

## 📺 PART 2: Project Overview (3 min)

**[SCREEN: Project file structure]**

"Let's look at what we're building. The project has three main parts:

1. **The Web App (app.py)**
   - Beautiful Streamlit interface
   - Multi-stock analysis
   - Interactive charts
   - AI predictions
   - Trading recommendations

2. **Email Automation (email_automation.py)**
   - Runs daily after market close
   - Analyzes 10 stocks
   - Sends HTML emails
   - Managed by subscribers

3. **GitHub Actions (daily_email.yml)**
   - Automatic scheduler
   - No server needed
   - Runs in the cloud
   - Completely free"

**[SCREEN: Data flow diagram]**

"Here's how it works:
1. Yahoo Finance provides free stock data
2. We calculate 30+ technical indicators
3. Machine learning model predicts next day's price
4. Results shown on web and sent via email"

**[SCREEN: Architecture diagram]**

"The system is designed to be:
- Free to run
- Easy to maintain
- Fully automated
- Professional quality"

---

## 📺 PART 3: Local Setup (8 min)

### 3.1 Download and Extract (1 min)

**[SCREEN: File explorer with downloaded project]**

"First, extract the project files to a folder. I'm using:
C:\Users\YourName\stock_predictor_app

Or on Mac:
/Users/YourName/stock_predictor_app"

### 3.2 Install Python (2 min)

**[SCREEN: Python download page]**

"If you don't have Python:
1. Go to python.org/downloads
2. Download Python 3.10 or newer
3. IMPORTANT: Check 'Add Python to PATH' during installation
4. Complete installation"

**[SCREEN: Terminal/Command Prompt]**

"Verify Python is installed:
```
python --version
```

Should show: Python 3.10.x or newer"

### 3.3 First Run (5 min)

**[SCREEN: Project folder]**

"Now let's run the app locally!

**For Windows:**
Double-click start.bat

**For Mac/Linux:**
Open Terminal here and run:
```
chmod +x start.sh
./start.sh
```"

**[SCREEN: Terminal showing installation]**

"The script will:
1. Create a virtual environment
2. Install all dependencies
3. Create necessary files
4. Start the app

This takes about 2 minutes the first time."

**[SCREEN: Browser opening to localhost:8501]**

"Success! The app opens in your browser at http://localhost:8501"

**[SCREEN: Demonstrating app features]**

"Let's test it:
1. Select a stock - let's try AAPL
2. See the current price and prediction
3. Check the visualization
4. Read the trading recommendations

Everything works locally! Now let's deploy it online."

---

## 📺 PART 4: Deploy to Internet (8 min)

### 4.1 Setup GitHub (3 min)

**[SCREEN: GitHub homepage]**

"First, let's upload our code to GitHub:

1. Go to github.com
2. Sign in or create free account
3. Click '+' → 'New repository'
4. Name: stock-predictor
5. Keep it public
6. Don't initialize with README
7. Click 'Create repository'"

**[SCREEN: Terminal/Command Prompt in project folder]**

"Now push our code:

```bash
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m \"Initial commit\"

# Set main branch
git branch -M main

# Add GitHub as remote (use YOUR username)
git remote add origin https://github.com/YOUR_USERNAME/stock-predictor.git

# Push to GitHub
git push -u origin main
```"

**[SCREEN: GitHub showing uploaded files]**

"Perfect! Code is now on GitHub."

### 4.2 Deploy on Streamlit (5 min)

**[SCREEN: share.streamlit.io]**

"Now let's make it public:

1. Go to share.streamlit.io
2. Sign in with GitHub (it'll ask for permissions - allow them)
3. Click 'New app'
4. Select your repository: YOUR_USERNAME/stock-predictor
5. Branch: main
6. Main file path: app.py
7. Click 'Deploy'"

**[SCREEN: Deployment process]**

"Streamlit is now:
- Installing dependencies
- Setting up the environment
- Starting your app

This takes 2-3 minutes."

**[SCREEN: Deployed app]**

"🎉 It's live! Your app is now on the internet.

Your URL: https://YOUR-APP-NAME.streamlit.app

IMPORTANT: Copy this URL - we'll need it for email setup!"

**[SCREEN: Testing deployed app]**

"Test it:
1. Click the URL
2. Select stocks
3. View predictions
4. Share with friends!"

---

## 📺 PART 5: Email Setup (10 min)

### 5.1 Get Gmail App Password (4 min)

**[SCREEN: Google Account settings]**

"For emails to work, we need a special password from Gmail:

1. Go to myaccount.google.com
2. Click 'Security' in left menu
3. Find '2-Step Verification'
   - If not enabled: Enable it now
   - Follow the prompts
4. Go back to Security
5. Scroll to '2-Step Verification'
6. At bottom: 'App passwords'
7. Select 'Mail' and your device
8. Click 'Generate'"

**[SCREEN: App password generated]**

"Gmail shows a 16-character password:
abcd efgh ijkl mnop

IMPORTANT:
- Copy this password
- Paste into a notepad
- You can only see it once!"

### 5.2 Configure GitHub Secrets (4 min)

**[SCREEN: GitHub repository settings]**

"Now we'll add this to GitHub securely:

1. Go to your GitHub repository
2. Click 'Settings' tab
3. In left menu: 'Secrets and variables' → 'Actions'
4. Click 'New repository secret'"

**[SCREEN: Adding first secret]**

"Add these 5 secrets one by one:

**Secret 1:**
Name: STREAMLIT_APP_URL
Value: https://your-app-name.streamlit.app
(paste YOUR actual app URL)

Click 'Add secret'"

**[SCREEN: Adding remaining secrets]**

"Continue adding:

**Secret 2:**
Name: SMTP_SERVER
Value: smtp.gmail.com

**Secret 3:**
Name: SMTP_PORT
Value: 587

**Secret 4:**
Name: SENDER_EMAIL
Value: your-email@gmail.com
(use YOUR email)

**Secret 5:**
Name: SENDER_PASSWORD
Value: abcd efgh ijkl mnop
(paste the 16-char app password from Gmail)

All 5 secrets added!"

### 5.3 Enable GitHub Actions (2 min)

**[SCREEN: GitHub Actions tab]**

"Final step:

1. Click 'Actions' tab in your repository
2. If you see 'Workflows are disabled'
   Click 'I understand my workflows, go ahead and enable them'
3. You should see 'Daily Stock Predictions Email' workflow
4. It's now scheduled to run weekdays at 4:30 PM EST"

**[SCREEN: Manual workflow run]**

"Let's test it now:
1. Click 'Daily Stock Predictions Email'
2. Click 'Run workflow' dropdown
3. Click green 'Run workflow' button
4. Wait 30 seconds
5. Refresh page
6. Click on the running workflow"

**[SCREEN: Workflow running]**

"Watch it:
- Set up Python ✓
- Install dependencies ✓
- Run email automation ✓
- Complete ✓"

---

## 📺 PART 6: Testing & Verification (5 min)

### 6.1 Test Email Configuration (2 min)

**[SCREEN: Terminal in project folder]**

"Let's verify emails work locally:

```bash
python test_config.py
```"

**[SCREEN: Test running]**

"The test checks:
✓ Environment variables loaded
✓ SMTP connection works
✓ Authentication successful
✓ Can send emails
✓ Data fetching works"

**[SCREEN: Test email option]**

"Enter your email when prompted.
Check your inbox - you should receive a test email!"

### 6.2 Subscribe on Web App (1 min)

**[SCREEN: Streamlit app sidebar]**

"Test the subscription feature:
1. Open your deployed app
2. Sidebar → Email Alerts
3. Enter your email
4. Click Subscribe
5. See 'Successfully subscribed!' message"

### 6.3 Check Email (2 min)

**[SCREEN: Email inbox]**

"After the GitHub Action runs (or at 4:30 PM EST daily):
1. Check your email inbox
2. Look for 'Daily Stock Predictions'
3. Open it"

**[SCREEN: Prediction email]**

"The email shows:
- All 10 stock predictions
- Current and predicted prices
- Expected changes
- Direct links to detailed analysis
- Professional formatting"

---

## 📺 PART 7: Customization (3 min)

### 7.1 Add Your Stocks (1 min)

**[SCREEN: app.py in editor]**

"Want to track different stocks?

Open app.py
Find POPULAR_STOCKS dictionary
Add your favorites:

```python
POPULAR_STOCKS = {
    \"My Picks\": [\"NVDA\", \"AMD\", \"INTC\"],
    \"Technology\": [\"AAPL\", \"MSFT\", \"GOOGL\"],
    ...
}
```

Save, commit, and push to GitHub:
```bash
git add app.py
git commit -m \"Added my favorite stocks\"
git push
```

Streamlit auto-deploys the update!"

### 7.2 Change Email Schedule (1 min)

**[SCREEN: .github/workflows/daily_email.yml]**

"To change when emails send:

Open: .github/workflows/daily_email.yml

Find the cron line:
```yaml
- cron: '30 21 * * 1-5'
```

This is: 4:30 PM EST on weekdays

Change to:
```yaml
- cron: '0 14 * * 1-5'  # 9 AM EST
- cron: '0 22 * * *'     # 5 PM EST daily
```

Use crontab.guru to help!"

### 7.3 Modify Email Stocks (1 min)

**[SCREEN: email_automation.py]**

"To change which stocks appear in emails:

Open: email_automation.py

Find STOCKS list:
```python
STOCKS = [\"AAPL\", \"MSFT\", \"GOOGL\", ...]
```

Change to your picks:
```python
STOCKS = [\"TSLA\", \"NVDA\", \"AMD\"]
```

Save, commit, push!"

---

## 📺 PART 8: Troubleshooting (2 min)

**[SCREEN: Common issues]**

"Quick fixes for common problems:

**'Module not found'**
```bash
pip install -r requirements.txt
```

**'Authentication failed' (email)**
- Use app password, not regular password
- Check 2FA is enabled
- Generate new app password

**'Insufficient data'**
- Increase date range in sidebar
- Try different stock
- Some stocks are too new

**GitHub Actions not running**
- Check all 5 secrets are added
- Verify workflow file exists
- Check Actions tab for errors"

---

## 📺 PART 9: Conclusion (1 min)

**[SCREEN: All features working]**

"Congratulations! You now have:

✓ Professional stock predictor
✓ Deployed on the internet
✓ Daily automated emails
✓ Multi-stock analysis
✓ AI predictions
✓ Trading recommendations
✓ All completely FREE!"

**[SCREEN: Resources]**

"Resources:
📖 Full documentation in README.md
🚀 Deployment alternatives in DEPLOYMENT_ALTERNATIVES.md
🏗️ Architecture guide in ARCHITECTURE.md
💬 Questions? Open a GitHub issue"

**[SCREEN: Disclaimer]**

"⚠️ Important reminder:
This is for EDUCATIONAL purposes only
Not financial advice
Always do your own research
Consult financial advisors before investing"

**[SCREEN: Call to action]**

"Thanks for watching!
- ⭐ Star the repository on GitHub
- 📧 Share with friends
- 💡 Customize it
- 📊 Happy (responsible) trading!

See you in the next tutorial!"

---

## 📝 Tutorial Checklist

Use this while following the video:

**Before Starting:**
- [ ] Python 3.8+ installed
- [ ] GitHub account created
- [ ] Streamlit account created
- [ ] Gmail 2FA enabled

**Part 1-2: Setup**
- [ ] Project extracted to folder
- [ ] Ran start.sh/start.bat
- [ ] App works on localhost:8501
- [ ] Tested stock selection

**Part 3: Deployment**
- [ ] Code pushed to GitHub
- [ ] Repository is public
- [ ] Streamlit app deployed
- [ ] Got app URL
- [ ] Tested online

**Part 4: Email**
- [ ] Generated Gmail app password
- [ ] Added 5 GitHub secrets
- [ ] Enabled GitHub Actions
- [ ] Tested workflow manually
- [ ] Received test email

**Part 5: Verification**
- [ ] Ran test_config.py
- [ ] Subscribed via web app
- [ ] Checked email works
- [ ] All systems go!

**Optional Customization:**
- [ ] Added favorite stocks
- [ ] Changed email schedule
- [ ] Modified email stocks

---

## 🎬 Recording Tips

**For video creators:**

1. **Screen Setup:**
   - 1920x1080 resolution
   - Large fonts (16-18pt)
   - Dark theme for code
   - Clear cursor

2. **Pacing:**
   - Speak slowly and clearly
   - Pause after each command
   - Show results before moving on
   - Repeat important steps

3. **Editing:**
   - Add chapter markers
   - Include timestamps in description
   - Show errors and fixes
   - Add on-screen text for key points

4. **Engagement:**
   - Ask viewers to like/subscribe
   - Link to GitHub repository
   - Respond to comments
   - Update for new versions

---

**Script Version:** 1.0  
**Last Updated:** 2024  
**Duration:** ~30 minutes  
**Difficulty:** Beginner
