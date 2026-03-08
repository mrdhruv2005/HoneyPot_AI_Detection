# 🛡️ CyberGuard: AI-Powered Scam Honeypot System

![CyberGuard Status](https://img.shields.io/badge/Status-Production%20Ready-success)
![AI Model](https://img.shields.io/badge/AI-Llama%203-blue)
![Tech Stack](https://img.shields.io/badge/Stack-Next.js%20%7C%20FastAPI%20%7C%20Redis%20%7C%20Mongo-orange)

**CyberGuard** is a state-of-the-art "National-Level" AI honeypot designed to engage, analyze, and expose digital scammers. By simulating vulnerable personas, it wastes scammers' time while extract critical threat intelligence (Bank Accounts, UPI IDs, Phone Numbers) in real-time.

---

## 🚀 Key Features

### 🧠 National-Level AI Agent
- **Behavioral Memory:** Remembers 20+ turns of conversation context.
- **Psychological Modeling:** Simulates fear, urgent compliance, or suspicion based on scammer tactics.
- **Intentional Mistakes:** Makes typos and corrections (15% rate) to appear human.
- **Multi-Language Support:** Adapts to English, Hindi, and Hinglish.

### 🛡️ Advanced Detection Engine
- **Dual-Layer Analysis:** Combines Rule-Based keyword matching (170+ patterns) with ML-based intent classification (95% accuracy).
- **Real-time Scoring:** Dynamic "Risk Score" updates with every message.
- **Threat Intelligence:** Automatically extracts and logs:
  - 🏦 Bank Account Numbers
  - 💸 UPI IDs
  - 🔗 Phishing Links
  - 📞 Phone Numbers

### 📊 Real-Time Command Center
- Live Dashboard showing active sessions.
- Visualizing threat data and extraction metrics.
- Hard-linked to **GUVI Callback API** for automated reporting.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
|-----------|------------|-------------|
| **Frontend** | Next.js 14, TailwindCSS | Modern, responsive dashboard & chat UI |
| **Backend** | FastAPI (Python) | High-performance async API |
| **AI Core** | Groq API (Llama 3) | Ultra-fast inference for real-time replies |
| **Database** | Redis (Upstash) | Session management & real-time stats |
| **Intelligence**| MongoDB Atlas | Long-term storage for extracted intel |
| **ML Engine** | Scikit-Learn | Naive Bayes Classifier for scam detection |

---

## ⚡ Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+
- Redis (Local or Upstash)
- MongoDB (Atlas or Local)
- Groq API Key

### 1. Clone the Repository
```bash
git clone https://github.com/jp7107/AI-Agnet-fraud-detection.git
cd AI-Agnet-fraud-detection
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file (See .env.example)
cp .env.example .env
# Edit .env and add your GROQ_API_KEY and DB credentials
```

### 3. Frontend Setup
```bash
cd frontend
npm install

# Create .env.local file
cp .env.local.example .env.local
```

### 4. Run the System
**Terminal 1 (Backend):**
```bash
cd backend
uvicorn main:app --reload --port 8001
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

Visit the Dashboard at `http://localhost:3001/dashboard`.

---

## 📸 Screenshots

### Command Center
*Real-time monitoring of scam attempts and extracted intelligence.*
![Dashboard](https://placehold.co/600x400?text=Dashboard+Preview)

### Live Chat Interface
*AI engaging with a scammer while analyzing risk in real-time.*
![Chat](https://placehold.co/600x400?text=Chat+Interface)

---

## 🔒 Security

- **Environment Variables:** All sensitive keys are stored in `.env` files (not committed).
- **Architecture:** Frontend communicates via strict API interfaces.

---

## 👥 Contributors

- **Team CyberGuard**
- Built for **GUVI HAckathon 2026**

---

*This project is for educational and defensive purposes only. Do not use for malicious activities.*
Project deployed by Dhruv Garg