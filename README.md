# Daily Reflection Tree AI Agent

## 🚀 Overview
This project implements a deterministic reflection agent that guides users through a structured end-of-day reflection using a decision tree.

The system does NOT use any LLM at runtime. Instead, all intelligence is encoded into a predefined tree structure, ensuring predictability, consistency, and auditability.

---

## 🧠 Psychological Axes

The reflection is structured across 3 axes:

1. Locus of Control (Victim vs Victor)
2. Contribution vs Entitlement
3. Radius (Self vs Others)

---

## 🛠 Tech Stack

- Python (FastAPI)
- HTML + JavaScript (Frontend)
- JSON (Tree structure)

---

## ⚙️ How to Run

### Backend
cd agent  
uvicorn app:app --reload  

### Frontend
python3 -m http.server 3000  



## 📌 API Endpoints

- GET /health → check server
- POST /start → start session
- POST /answer → submit answer
- POST /continue → move forward


## 🌐 Access

- Frontend → http://localhost:3000/index.html  
- API Docs → http://127.0.0.1:8000/docs  


## 🎥 Demo
(Add your video link here)


## 📁 Project Structure

/tree → reflection tree data  
/agent → backend logic  
/transcripts → sample runs  

---

## 👨‍💻 Author
Mohammad Amm
