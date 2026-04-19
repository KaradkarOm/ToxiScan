# 🛡️ Toxicity & Cyberbullying Detector

A real-time web application to detect toxic and harmful messages using NLP.

## ⚡ Quick Start

### Option 1: Two Terminals

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install  # First time only
npm start
```

## 🌐 Access
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Info:** http://localhost:8000/api/info

## 📁 Project Structure
```
├── backend/              # Flask REST API
│   ├── app.py           # Server (runs on :8000)
│   └── requirements.txt  # Python dependencies
│
├── frontend/            # React web UI
│   ├── src/
│   │   ├── App.jsx      # Main component
│   │   ├── App.css      # Styling
│   │   └── main.jsx
│   └── package.json
│
├── vaderSentiment/      # NLP detector engine
│   ├── toxicity_detector.py
│   └── vader_lexicon.txt
│
└── run-dev.sh          # Start both servers
```

## 🎯 Features
✅ Real-time toxicity detection  
✅ Severity classification (Clean → Red)  
✅ Toxic words highlighting  
✅ Sentiment analysis breakdown  
✅ Mobile responsive UI  

## 🔧 Technology Stack
- **Backend:** Flask, Python
- **Frontend:** React, Vite
- **NLP:** VADER Sentiment Analysis
- **Styling:** Pure CSS3

## 📌 Requirements
- Python 3.7+
- Node.js 16+
- npm

## ⚠️ Troubleshooting

**Port 8000 already in use:**
```bash
kill -9 $(lsof -t -i :8000)
```

**Dependencies not found:**
```bash
# Backend
cd backend && pip install -r requirements.txt

# Frontend
cd frontend && npm install
```

---

**Created:** April 19, 2026  
**Status:** Production Ready ✅
