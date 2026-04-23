# 🌳 Daily Reflection Tree  
### Deterministic Reflection Agent (No Runtime LLM)

## 📌 Project Overview

The Daily Reflection Tree is a deterministic end-of-day reflection system that helps a user examine their workday through three psychological dimensions:

1. Locus of Control → Internal vs External  
2. Orientation → Contribution vs Entitlement  
3. Radius of Concern → Self vs Others  

Unlike conversational AI systems, this project:

✅ uses a static decision tree  
✅ produces predictable outcomes  
✅ stores structured state  
✅ performs zero LLM calls at runtime

The intelligence lives inside the tree design, not inside a model.

## 🎯 Assignment Goal

This project was built to demonstrate:

- Knowledge engineering
- Deterministic system design
- Psychology-to-data translation
- User-centered reflection flow

## 🧠 Psychological Foundations

This tree was informed by:

### Axis 1 — Locus
- Julian Rotter → Locus of Control
- Carol Dweck → Growth Mindset

### Axis 2 — Orientation
- Campbell → Psychological Entitlement
- Organ → Organizational Citizenship Behavior

### Axis 3 — Radius
- Maslow → Self-Transcendence
- Batson → Perspective Taking


## 🏗️ Project Structure

id="s19a2x" /tree/   reflection-tree.json      # Deterministic reflection tree /agent/   app.py                    # FastAPI API layer   agent.py                  # Tree engine /transcripts/   persona-1-transcript.md   persona-2-transcript.md /screenshots/ write-up.md README.md


## ⚙️ How It Works

### Reflection flow

1. Start session
2. Load tree from JSON
3. Ask fixed-option question
4. Store answer
5. Update psychological signals
6. Route to next node
7. Generate final summary

No free text.  
No probabilistic output.  
Fully auditable.



## 🌿 Three Reflection Axes

### 1. Control
The system asks:
> Did the user experience the day as something they shaped or something that happened to them?


### 2. Contribution
The system asks:
> Was the user focused on what they gave or what they expected?



### 3. Perspective
The system asks:
> Did the user frame the day around themselves or around a larger system?



## 🚀 Running the Project Locally



### Backend

bash id="7qf2k8" cd agent uvicorn app:app --reload --port 8000 

Backend available at:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs


### Frontend

From root folder:

bash id="0w9jz4" python3 -m http.server 3000 

Frontend available at:

http://localhost:3000

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | /health | API health check |
| POST | /start | Start session |
| POST | /answer | Submit answer |
| POST | /continue | Continue flow |


## 📷 Screenshots
<img width="1310" height="736" alt="Screenshot 2026-04-23 at 10 55 14 PM" src="https://github.com/user-attachments/assets/d515680e-de94-46a5-9327-5e37438e9cb8" />
<img width="1310" height="736" alt="Screenshot 2026-04-23 at 11 08 11 PM" src="https://github.com/user-attachments/assets/922801d4-fe24-47ab-abd2-0b064b060bc0" />


Example:

id="m83hf1" /screenshots/home.png /screenshots/question.png /screenshots/summary.png

Then reference:

markdown id="u7j3l0" ![Home](screenshots/home.png) 

---

## 🎥 Demo Video
https://youtu.be/ThlZGYByiUI?si=b9GZ3uflXbFRV5Fn

## 📄 Sample Reflection Paths

Two example transcripts are included:

- transcripts/persona-1-transcript.md
- transcripts/persona-2-transcript.md

These demonstrate:
- different choices
- different branches
- different summaries

## 💡 Design Decisions

Key design choices:

### Determinism
Every answer leads to:
- one known node
- one known reflection
- one reproducible outcome

### Human Tone
The reflections were written to feel:
- thoughtful
- neutral
- non-judgmental


### Separation of Concerns
Tree data remains separate from:
- backend logic
- frontend rendering

This allows:
- easy modification
- reuse across interfaces
- cleaner maintenance


## 👤 Author

Mohammad Ammar

Aspiring:
Data Analyst → Data Scientist → Knowledge Engineer
