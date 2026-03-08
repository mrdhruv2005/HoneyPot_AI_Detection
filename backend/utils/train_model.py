import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
import logging
import os

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("model_trainer")

def generate_processed_data():
    """
    Generates a synthetic dataset of Scam vs Safe messages.
    """
    scam_messages = [
        "Urgent: Your bank account is locked. Click here to verify: http://bit.ly/scam",
        "You have won a lottery of $50000. Send $500 processing fee to claim.",
        "RBI alert: Your KYC is pending. Update immediately or account blocked.",
        "Dear customer, your electricity will be disconnected tonight. Call 9876543210.",
        "Quick loan approved! 5 lakhs in 5 mins. No documents. Apply now.",
        "Hot singles in your area looking to chat. Click link.",
        "Investment opportunity! Double your money in 24 hours. Crypto scheme.",
        "Your package is held at customs. Pay shipping fee to release.",
        "IRS Final Notice: Lawsuit filed against you. Call immediately.",
        "Tech Support: Your computer has a virus. Download this patch."
    ]
    
    safe_messages = [
        "Hey, are you coming to the party tonight?",
        "Your otp for transaction is 123456. Do not share with anyone.",
        "Meeting rescheduled to 4 PM.",
        "Can you send me the grocery list?",
        "Happy Birthday! Have a great day ahead.",
        "Your Amazon order has been delivered.",
        "Let's catch up over coffee this weekend.",
        "Please find the attached invoice for your reference.",
        "Don't forget to pay the electricity bill by Friday.",
        "The weather looks great today."
    ]
    
    # Expand dataset (duplicates for weight, in real scenario use better augmentation)
    data = []
    for msg in scam_messages:
        data.append({"text": msg, "label": 1}) # 1 = Scam
        
    for msg in safe_messages:
        data.append({"text": msg, "label": 0}) # 0 = Safe
        
    return pd.DataFrame(data)

def train():
    logger.info("Generating synthetic dataset...")
    df = generate_processed_data()
    
    logger.info(f"Training model on {len(df)} samples...")
    
    # Create Pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', ngram_range=(1,2))),
        ('clf', LogisticRegression(solver='liblinear'))
    ])
    
    # Train
    pipeline.fit(df['text'], df['label'])
    
    # Save
    model_path = os.path.join(os.path.dirname(__file__), "../models/scam_model.pkl")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    joblib.dump(pipeline, model_path)
    logger.info(f"Model saved to {model_path}")
    
    # Test
    test_msg = "Urgent: Account blocked. Verify now."
    prediction = pipeline.predict_proba([test_msg])[0][1]
    logger.info(f"Test Prediction for '{test_msg}': {prediction:.2f}")

if __name__ == "__main__":
    train()
