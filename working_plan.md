# Working Plan — AI-Driven Adaptive Diagnostic Engine

> This document explains **what we built**, **why we made each decision**, and **how the system works end-to-end**. Use it alongside the README as a technical reference.

---

## What We Built

A complete full-stack web application for adaptive educational testing:

- **Backend API** (FastAPI + MongoDB) — implements 5 REST endpoints managing test sessions
- **Adaptive Algorithm** (1D IRT) — dynamically selects questions based on student ability
- **AI Study Plan** (OpenAI GPT-4o-mini) — generates personalized 3-step improvement plans
- **React Frontend** (Vite + Vanilla CSS) — premium dark glassmorphism UI with real-time ability tracking

---

## Architecture Decisions

### Why FastAPI?
- Native async support (motor for MongoDB)
- Automatic Swagger/OpenAPI documentation at `/docs`
- Pydantic v2 for type-safe request/response validation
- Fast cold-start — ideal for prototypes

### Why Motor (not PyMongo)?
- Motor is the async-native MongoDB driver for Python
- Allows non-blocking I/O in FastAPI's async event loop
- PyMongo would block the event loop during DB operations

### Why 1D IRT over simpler difficulty ladders?
- IRT is the academic standard used in GRE, SAT, and GMAT adaptive testing
- The Rasch model provides mathematically principled ability estimation
- Unlike simple "get harder if correct" rules, IRT accounts for item difficulty probability curves (S-shaped logistic function)
- The ability score θ is a continuous, interpretable metric (not just a step ladder)

### Why 10 questions?
- Balances diagnostic precision with user experience
- Research shows IRT ability estimates stabilize after 8–12 items
- Short enough to complete in < 10 minutes

### Why store `answered_ids` in the session document?
- Prevents the same question appearing twice in a session
- Allows resuming sessions (future feature)
- MongoDB's `$push` operation makes appending IDs atomic

### Why React + Vite (not Next.js)?
- The application is purely client-side (no SSR needed)
- Vite offers instant HMR and the fastest dev startup
- Keeps the frontend simple and focused on the assignment requirements

### Why Vanilla CSS (no Tailwind)?
- Full design control without a build step configuration
- CSS custom properties (variables) give a clean design token system
- Glassmorphism and custom animations are simpler in pure CSS

---

## Data Flow (End-to-End)

```
User types name → POST /session/start → MongoDB session doc created (θ=0.5)
          ↓
GET /session/{id}/next-question
  → IRT engine selects question with difficulty closest to θ
  → Question returned (without answer)
          ↓
User picks A/B/C/D → POST /session/{id}/submit-answer
  → IRT: P = 1/(1+exp(-1.7*(θ-b)))
  → If correct: θ += 0.3*(1-P)   else: θ -= 0.3*P
  → MongoDB: push response, update ability_score
  → Return: is_correct, ability_before, ability_after
          ↓
Repeat 10 times
          ↓
GET /session/{id}/results
  → Aggregate per-topic accuracy
  → Return ability score, level, full topic breakdown
          ↓
POST /session/{id}/study-plan
  → Build OpenAI prompt with weak topics + accuracy data
  → GPT returns JSON: summary + 3 steps + resources + duration
  → Saved to session doc, returned to frontend
```

---

## Phase Breakdown

| Phase | What We Did |
|-------|------------|
| **1 — Config** | requirements.txt, .env.example, .gitignore, .env |
| **2 — DB Layer** | motor connection, seed script with 25 GRE-style questions across 5 topics |
| **3 — Models** | Pydantic `Question` and `UserSession` (with `Response` sub-model) |
| **4 — IRT Engine** | `probability_correct()`, `update_ability()`, `select_next_question()` |
| **5 — LLM Service** | OpenAI async client, performance prompt builder, JSON response parser |
| **6 — API Routes** | 5 FastAPI endpoints with full error handling |
| **7 — Frontend CSS** | Dark glassmorphism design system with gradient tokens and animations |
| **8 — React Components** | StartScreen, QuestionCard, ResultsScreen, StudyPlan |
| **9 — App State Machine** | App.jsx managing 5 screens: start/loading/question/results/plan |
| **10 — Docs** | README.md (setup, algorithm), working_plan.md (this file) |

---

## Question Bank Design (25 Questions)

| Topic | Count | Difficulty Range |
|-------|-------|----------------|
| Algebra | 5 | 0.15 – 0.55 |
| Geometry | 5 | 0.20 – 0.65 |
| Vocabulary | 5 | 0.45 – 0.70 |
| Reading Comprehension | 5 | 0.30 – 0.55 |
| Quantitative Reasoning | 5 | 0.15 – 0.50 |

Each question has: `text`, `options` (A–D), `correct_answer`, `difficulty`, `topic`, `tags`.

---

## IRT Math (Worked Example)

Starting ability: **θ = 0.5**

**Question 1:** difficulty b = 0.20 (easy)
```
P = 1 / (1 + exp(-1.7 × (0.5 - 0.20))) = 1 / (1 + exp(-0.51)) ≈ 0.625
If correct: θ = 0.5 + 0.3 × (1 - 0.625) = 0.5 + 0.1125 = 0.6125
```

**Question 2:** Next question selected with b ≈ 0.61 (medium-hard)

This continues, converging toward the student's true ability level by question 10.

---

## How to Demo This Project

1. Start MongoDB
2. `python -m app.database.seed` (one time)
3. `uvicorn app.main:app --reload`
4. `cd frontend && npm run dev`
5. Open http://localhost:5173
6. Enter your name → take 10 questions → view results → generate AI study plan
7. Open http://localhost:8000/docs to inspect the API live
