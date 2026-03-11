# AI-Driven Adaptive Diagnostic Engine

A full-stack adaptive testing system built with **FastAPI** + **React Vite** that uses **1D Item Response Theory (IRT)** to dynamically calibrate question difficulty in real-time, and **OpenAI GPT** to generate personalized study plans after each session.

---
<img width="1711" height="942" alt="image" src="https://github.com/user-attachments/assets/0e36b556-85aa-40ff-9ecf-235ae298d509" />
<img width="1469" height="943" alt="image" src="https://github.com/user-attachments/assets/5ee37072-5b59-4c95-96ad-00a587c03036" />
<img width="1222" height="916" alt="image" src="https://github.com/user-attachments/assets/edb1b515-b913-40fe-ad6f-57084c0accb6" />
<img width="1191" height="945" alt="image" src="https://github.com/user-attachments/assets/721af24c-0882-41de-8c38-dc6c548816c4" />


## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | FastAPI (Python 3.11+) |
| Database | MongoDB (via Motor async driver) |
| Adaptive Algorithm | 1D IRT (Item Response Theory) |
| AI Study Plans | OpenAI GPT-4o-mini |
| Frontend | React 19 + Vite 7 |
| Styling | Vanilla CSS (glassmorphism dark theme) |

---

## Project Structure

```
internship_tasl/
├── app/
│   ├── main.py                   # FastAPI entry point + CORS
│   ├── database/
│   │   ├── db.py                 # Motor MongoDB connection
│   │   └── seed.py               # 25 GRE-style questions seeder
│   ├── models/
│   │   ├── question.py           # Question Pydantic model
│   │   └── session.py            # UserSession + Response models
│   ├── services/
│   │   ├── adaptive_engine.py    # IRT algorithm (core)
│   │   └── llm_service.py        # OpenAI study plan generator
│   └── routers/
│       └── session.py            # 5 REST API endpoints
├── frontend/
│   └── src/
│       ├── App.jsx               # State machine
│       ├── api.js                # Axios API layer
│       ├── index.css             # Design system
│       └── components/
│           ├── StartScreen.jsx
│           ├── QuestionCard.jsx
│           ├── ResultsScreen.jsx
│           └── StudyPlan.jsx
├── requirements.txt
├── .env.example
└── README.md
```

---

## Setup & Run

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB running locally on port 27017

### 1. Clone and configure

```bash
# Copy environment variables
cp .env.example .env
```

Open `.env` and fill in your keys:
```
MONGODB_URI=mongodb://localhost:27017
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini
```

### 2. Backend setup

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Seed the database with 25 questions
python -m app.database.seed

# Start the API server
uvicorn app.main:app --reload
```

API runs at: **http://localhost:8000**  
Swagger UI: **http://localhost:8000/docs**

### 3. Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: **http://localhost:5173**

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/session/start` | Create new test session |
| `GET` | `/session/{id}/next-question` | Get next adaptive question |
| `POST` | `/session/{id}/submit-answer` | Submit answer, update ability θ |
| `GET` | `/session/{id}/results` | Full session results + topic breakdown |
| `POST` | `/session/{id}/study-plan` | Generate AI personalized study plan |

---

## Adaptive Algorithm — How It Works

### 1-Parameter IRT (Rasch Model)

The system estimates student **ability θ** (theta) using:

**Probability of a correct response:**
```
P(correct | θ, b) = 1 / (1 + exp(-1.7 × (θ - b)))
```
Where:
- `θ` = student ability score (0.0 – 1.0, starts at 0.5)
- `b` = item difficulty (0.0 – 1.0)

**Ability update after each response:**
```
If correct:   θ_new = θ + lr × (1 - P)
If incorrect: θ_new = θ - lr × P
```
Where `lr = 0.3` (learning rate). θ is clamped to [0.01, 0.99].

**Question Selection:**
- After each response, the next question is the unanswered one with difficulty `b` closest to current `θ`
- This ensures the test is always appropriately challenging

**Session Flow:**
1. Start → θ = 0.5 (medium ability)
2. Answer → θ updates via IRT formula
3. Next question selected: `|b - θ|` minimised
4. After 10 questions → session completed → fetch results + AI plan

---

## AI Study Plan Generation

The LLM service:
1. Collects: ability score θ, accuracy per topic, weak topics (< 50%)
2. Constructs a structured prompt for GPT
3. Returns a **structured JSON** 3-step plan with titles, descriptions, and resources
4. Uses `response_format: json_object` for reliable parsing

---

## AI Tools Used

This project was built with AI assistance:

- **Code generation**: Used an AI coding assistant to scaffold the IRT adaptive engine, FastAPI routers, and React components
- **Algorithm validation**: Verified IRT formulas against Rasch model literature
- **Prompt engineering**: Crafted the OpenAI prompt to return consistent JSON study plans
- **UI Design**: AI-assisted dark glassmorphism CSS design system with gradient accents
