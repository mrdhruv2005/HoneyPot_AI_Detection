import joblib
import os
import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import json

logger = logging.getLogger("ml_engine")

class MLEngine:
    """
    Enhanced ML-Based Scam Detection Engine
    Features:
    - TF-IDF vectorization
    - Naive Bayes classifier
    - Training on scam/legitimate message dataset
    - Model persistence
    - Confidence scoring
    """
    
    def __init__(self):
        self.model = None
        self.model_path = os.path.join(os.path.dirname(__file__), "../models/scam_model.pkl")
        self.training_data_path = os.path.join(os.path.dirname(__file__), "../models/training_data.json")
        
        # Ensure models directory exists
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        self.load_model()
    
    def load_model(self):
        """Load pre-trained model or train new one"""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                logger.info(f"✅ ML Model loaded from {self.model_path}")
            else:
                logger.warning(f"⚠️ Model not found. Training new model...")
                self.train_model()
        except Exception as e:
            logger.error(f"❌ Failed to load ML model: {e}")
            self.model = None

    def get_training_data(self):
        """
        Get training dataset
        Returns: (texts, labels) where labels: 0=legitimate, 1=scam
        """
        
        # Comprehensive scam message examples
        scam_messages = [
            # Account suspension scams
            "Your bank account has been suspended due to suspicious activity. Verify immediately.",
            "URGENT: Your account will be blocked in 24 hours. Click here to verify.",
            "Your SBI account is locked. Call +919876543210 to unlock.",
            "HDFC Bank: Unauthorized transaction detected. Update KYC now.",
            
            # Legal threat scams
            "Police case will be filed against you. Pay fine immediately.",
            "Income tax notice: Pay Rs. 50,000 or face arrest.",
            "Cyber crime FIR registered. Contact immediately to avoid legal action.",
            "Court summons issued. Settle amount to avoid warrant.",
            
            # Prize/lottery scams
            "Congratulations! You won Rs. 25 lakhs in lucky draw. Claim now.",
            "You are selected for Amazon gift voucher worth Rs. 10,000.",
            "KBC lottery winner! Transfer processing fee to claim prize.",
            "Flipkart anniversary offer: You won iPhone 15. Pay delivery charges.",
            
            # Tech support scams
            "Your computer has virus. Download TeamViewer for immediate fix.",
            "Microsoft security alert: Install AnyDesk to remove malware.",
            "Google account compromised. Share screen to secure it.",
            "Apple support: Your iCloud is hacked. Download remote tool.",
            
            # Payment/refund scams
            "Paytm refund of Rs. 5000 pending. Share UPI ID to receive.",
            "GPay cashback failed. Send OTP to retry.",
            "PhonePe: Verify account to get Rs. 2000 bonus.",
            "LPG subsidy refund available. Share bank details.",
            
            # OTP/credential phishing
            "Your OTP is 123456. Do not share with anyone. (This is test)",
            "Enter your ATM PIN to verify card.",
            "Share CVV number for transaction verification.",
            "Confirm your internet banking password for security update.",
            
            # Impersonation scams
            "I am calling from SBI Bank customer care. Your KYC is pending.",
            "This is Amazon customer support. Your order is on hold.",
            "Government of India: Aadhaar card will be blocked.",
            "RBI official: Your PAN card needs immediate update.",
            
            # Job/investment scams
            "Work from home opportunity. Earn Rs. 50,000 per month.",
            "Invest Rs. 10,000 and get Rs. 1 lakh in 30 days guaranteed.",
            "Part-time job: Just click ads and earn daily.",
            "Bitcoin investment: Double your money in 1 week.",
            
            # COVID/emergency scams
            "COVID relief fund: Claim Rs. 15,000 government compensation.",
            "Vaccine registration fee pending. Pay now to book slot.",
            "PM Kisan Yojana: Transfer Rs. 500 to receive Rs. 6000.",
            
            # Gift card scams
            "Pay via Google Play gift card to unlock account.",
            "Send iTunes card code to verify identity.",
            "Purchase Amazon gift card for processing fee.",
            
            # Courier/parcel scams
            "Your courier parcel is held at customs. Pay duty charges.",
            "FedEx: Package delivery failed. Click link to reschedule.",
            "India Post: Parcel contains illegal items. Contact immediately.",
            
            # Cryptocurrency scams
            "Invest in USDT now. 500% returns guaranteed.",
            "Bitcoin wallet suspended. Verify with seed phrase.",
            "Crypto airdrop: Send 0.1 BTC to receive 1 BTC.",
            
            # Romance/social media scams
            "I am stuck in airport. Send money urgently.",
            "Investment opportunity from your Facebook friend.",
            "WhatsApp: Your account will expire. Verify now.",
            
            # Rental/property scams
            "Advance payment required to book flat. Transfer now.",
            "Property investment: Pay token amount immediately.",
            
            # Charity scams
            "Donate for flood victims. Send to this UPI ID.",
            "NGO fundraising: Transfer amount for orphan children.",
            
            # Additional variations
            "Click this link immediately: http://scam-site.com",
            "Download app from bit.ly/scam123",
            "Visit www.fake-bank-verify.com to update details",
            "Your Aadhaar is linked to 5 SIM cards. Verify now or face arrest.",
            "GST refund pending. Share bank account number.",
            "Electricity bill overdue. Pay now to avoid disconnection.",
            "Insurance claim approved. Pay processing fee to receive amount.",
            "Credit card application approved. Pay activation fee.",
            "Loan approved instantly. Transfer documentation charges.",
            "Your number won car in lucky draw. Pay registration fee."
        ]
        
        # Legitimate message examples
        legitimate_messages = [
            # Normal banking
            "Your account balance is Rs. 10,000.",
            "Transaction successful. Rs. 500 debited from your account.",
            "Your credit card bill is due on 15th.",
            "Thank you for using our ATM services.",
            
            # Normal customer service
            "Thank you for contacting customer support. How can I help?",
            "Your order has been shipped and will arrive tomorrow.",
            "Your appointment is confirmed for Monday 10 AM.",
            "We received your feedback. Thank you.",
            
            # Normal notifications
            "Your OTP for login is 123456. Valid for 10 minutes.",
            "Password changed successfully.",
            "Your booking is confirmed. Reference number: ABC123.",
            "Payment received. Invoice attached.",
            
            # Personal messages
            "Hey, how are you doing?",
            "Can we meet for coffee tomorrow?",
            "Happy birthday! Have a great day.",
            "Thanks for your help yesterday.",
            
            # Work messages
            "Meeting scheduled for 3 PM today.",
            "Please review the attached document.",
            "Project deadline extended to next week.",
            "Good work on the presentation.",
            
            # Service updates
            "Your internet connection will be upgraded tomorrow.",
            "Scheduled maintenance on Sunday 2-4 AM.",
            "New features added to the app. Update now.",
            "Your subscription renews on 1st of next month.",
            
            # E-commerce
            "Your order is out for delivery.",
            "Item added to wishlist successfully.",
            "Sale starts tomorrow. Check our website.",
            "Product review: Thank you for your purchase.",
            
            # Travel
            "Flight booking confirmed. PNR: XYZ789.",
            "Hotel check-in at 2 PM.",
            "Cab will arrive in 5 minutes.",
            "Train running 10 minutes late.",
            
            # Education
            "Exam results will be announced next week.",
            "Assignment submission deadline: Friday.",
            "Class rescheduled to Thursday.",
            "Library books due for return.",
            
            # Health
            "Your appointment with Dr. Smith is tomorrow.",
            "Prescription ready for pickup.",
            "Lab reports available online.",
            "Annual checkup reminder.",
            
            # Social
            "You have a new friend request.",
            "Someone liked your post.",
            "Event invitation: Birthday party on Saturday.",
            "Group created: Family Chat.",
            
            # Utilities
            "Electricity bill generated: Rs. 1200.",
            "Water supply will be interrupted tomorrow 10-12 AM.",
            "Gas cylinder booking confirmed.",
            "Broadband plan renewed successfully.",
            
            # Government (legitimate)
            "Aadhaar card delivered to your address.",
            "PAN card application under process.",
            "Voter ID ready for collection.",
            "Passport application submitted successfully.",
            
            # Additional normal messages
            "Good morning! Have a nice day.",
            "Reminder: Doctor appointment at 5 PM.",
            "Your package has been delivered.",
            "Thank you for your order.",
            "Welcome to our service.",
            "Your profile has been updated.",
            "Newsletter subscription confirmed.",
            "Event registration successful.",
            "Feedback submitted. Thank you.",
            "Your query has been forwarded to the concerned department."
        ]
        
        # Create labels
        texts = scam_messages + legitimate_messages
        labels = [1] * len(scam_messages) + [0] * len(legitimate_messages)
        
        logger.info(f"📊 Training data: {len(scam_messages)} scam, {len(legitimate_messages)} legitimate")
        
        return texts, labels

    def train_model(self):
        """Train the ML model"""
        try:
            logger.info("🎓 Starting model training...")
            
            # Get training data
            texts, labels = self.get_training_data()
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                texts, labels, test_size=0.2, random_state=42, stratify=labels
            )
            
            # Create pipeline
            self.model = Pipeline([
                ('tfidf', TfidfVectorizer(
                    max_features=1000,
                    ngram_range=(1, 2),  # Unigrams and bigrams
                    min_df=1,
                    max_df=0.9
                )),
                ('clf', MultinomialNB(alpha=0.1))
            ])
            
            # Train
            self.model.fit(X_train, y_train)
            
            # Evaluate
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            logger.info(f"✅ Model trained successfully!")
            logger.info(f"📈 Accuracy: {accuracy:.2%}")
            logger.info(f"\n{classification_report(y_test, y_pred, target_names=['Legitimate', 'Scam'])}")
            
            # Save model
            joblib.dump(self.model, self.model_path)
            logger.info(f"💾 Model saved to {self.model_path}")
            
        except Exception as e:
            logger.error(f"❌ Training failed: {e}")
            self.model = None

    def predict(self, text: str) -> float:
        """
        Predict scam probability
        Returns: 0.0 to 1.0 (probability of being a scam)
        """
        if not self.model:
            logger.warning("⚠️ Model not available. Using fallback.")
            return 0.1
        
        try:
            # Get probability of scam class (class 1)
            proba = self.model.predict_proba([text])[0][1]
            return float(proba)
        except Exception as e:
            logger.error(f"❌ Prediction error: {e}")
            return 0.0

    def predict_with_confidence(self, text: str) -> dict:
        """
        Predict with detailed confidence scores
        Returns: dict with prediction, probability, and confidence level
        """
        if not self.model:
            return {
                "is_scam": False,
                "probability": 0.0,
                "confidence": "low",
                "message": "Model not available"
            }
        
        try:
            proba = self.model.predict_proba([text])[0]
            scam_prob = float(proba[1])
            
            # Determine confidence level
            if scam_prob >= 0.8 or scam_prob <= 0.2:
                confidence = "high"
            elif scam_prob >= 0.6 or scam_prob <= 0.4:
                confidence = "medium"
            else:
                confidence = "low"
            
            return {
                "is_scam": scam_prob >= 0.5,
                "probability": scam_prob,
                "confidence": confidence,
                "legitimate_prob": float(proba[0])
            }
        except Exception as e:
            logger.error(f"❌ Prediction error: {e}")
            return {
                "is_scam": False,
                "probability": 0.0,
                "confidence": "error",
                "message": str(e)
            }

    def retrain(self):
        """Retrain the model with current data"""
        logger.info("🔄 Retraining model...")
        self.train_model()
