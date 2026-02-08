"""
Test Email Functionality
Run this script to verify your email configuration works before deploying
"""

import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

def test_email_config():
    """Test email configuration"""
    print("=" * 60)
    print("📧 Email Configuration Test")
    print("=" * 60)
    print()
    
    # Check environment variables
    print("1️⃣ Checking environment variables...")
    
    if not SENDER_EMAIL:
        print("   ❌ SENDER_EMAIL not found in .env file")
        return False
    else:
        print(f"   ✅ SENDER_EMAIL: {SENDER_EMAIL}")
    
    if not SENDER_PASSWORD:
        print("   ❌ SENDER_PASSWORD not found in .env file")
        return False
    else:
        print(f"   ✅ SENDER_PASSWORD: {'*' * len(SENDER_PASSWORD)} (hidden)")
    
    print(f"   ✅ SMTP_SERVER: {SMTP_SERVER}")
    print(f"   ✅ SMTP_PORT: {SMTP_PORT}")
    print()
    
    # Test SMTP connection
    print("2️⃣ Testing SMTP connection...")
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        print("   ✅ SMTP connection established")
        print("   ✅ TLS enabled")
        
        # Test authentication
        print()
        print("3️⃣ Testing authentication...")
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        print("   ✅ Authentication successful")
        
        # Ask if user wants to send test email
        print()
        print("4️⃣ Send test email?")
        test_email = input("   Enter your email to receive a test message (or press Enter to skip): ").strip()
        
        if test_email and "@" in test_email:
            print(f"   📤 Sending test email to {test_email}...")
            
            # Create test message
            msg = MIMEMultipart('alternative')
            msg['From'] = SENDER_EMAIL
            msg['To'] = test_email
            msg['Subject'] = f"🧪 Stock Predictor Test Email - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; padding: 20px; }}
                    .header {{ 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 20px;
                        border-radius: 10px;
                        text-align: center;
                    }}
                    .content {{
                        background: #f8f9fa;
                        padding: 20px;
                        border-radius: 5px;
                        margin-top: 20px;
                    }}
                    .success {{
                        color: #28a745;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🧪 Email Configuration Test</h1>
                </div>
                <div class="content">
                    <p class="success">✅ SUCCESS!</p>
                    <p>Your email configuration is working correctly.</p>
                    <p><strong>Test Details:</strong></p>
                    <ul>
                        <li>From: {SENDER_EMAIL}</li>
                        <li>SMTP Server: {SMTP_SERVER}:{SMTP_PORT}</li>
                        <li>Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
                    </ul>
                    <p>You're all set to receive daily stock predictions!</p>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html_content, 'html'))
            server.send_message(msg)
            
            print("   ✅ Test email sent successfully!")
            print(f"   📬 Check your inbox at {test_email}")
        
        server.quit()
        print()
        print("=" * 60)
        print("🎉 All tests passed! Email configuration is working.")
        print("=" * 60)
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("   ❌ Authentication failed!")
        print()
        print("Common issues:")
        print("   • Using regular password instead of app password")
        print("   • App password not generated correctly")
        print("   • 2-factor authentication not enabled")
        print()
        print("For Gmail:")
        print("   1. Enable 2-factor authentication")
        print("   2. Go to: Google Account → Security → 2-Step Verification")
        print("   3. Scroll down to 'App passwords'")
        print("   4. Generate new app password for 'Mail'")
        print("   5. Copy the 16-character password to .env file")
        return False
        
    except smtplib.SMTPException as e:
        print(f"   ❌ SMTP error: {e}")
        return False
        
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_prediction():
    """Test prediction functionality"""
    print()
    print("=" * 60)
    print("🤖 Testing Prediction Functionality")
    print("=" * 60)
    print()
    
    try:
        print("Importing required libraries...")
        import yfinance as yf
        import pandas as pd
        import numpy as np
        from sklearn.linear_model import Ridge
        from sklearn.preprocessing import StandardScaler
        
        print("✅ All libraries imported successfully")
        print()
        
        print("Testing data fetch from Yahoo Finance...")
        ticker = "AAPL"
        df = yf.download(ticker, period="1y", progress=False)
        
        if len(df) > 0:
            print(f"✅ Successfully fetched {len(df)} days of data for {ticker}")
            print(f"   Latest close: ${df['Close'].iloc[-1]:.2f}")
        else:
            print("❌ No data fetched")
            return False
        
        print()
        print("=" * 60)
        print("✅ Prediction test passed!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print()
    print("╔════════════════════════════════════════════════════════╗")
    print("║     Stock Market Predictor - Configuration Test       ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()
    
    # Run tests
    email_ok = test_email_config()
    prediction_ok = test_prediction()
    
    print()
    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print(f"Email Configuration: {'✅ PASS' if email_ok else '❌ FAIL'}")
    print(f"Prediction System:   {'✅ PASS' if prediction_ok else '❌ FAIL'}")
    print("=" * 60)
    print()
    
    if email_ok and prediction_ok:
        print("🎉 All systems ready! You can now deploy your app.")
    else:
        print("⚠️  Please fix the issues above before deploying.")
    
    print()
    input("Press Enter to exit...")
