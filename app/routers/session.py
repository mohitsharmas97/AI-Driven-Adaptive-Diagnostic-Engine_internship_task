from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime

from app.database.db import get_db
from app.services.adaptive_engine import update_ability, select_next_question
from app.services.llm_service import generate_study_plan

router = APIRouter(prefix="/session", tags=["session"])


# ── Request Schemas ──────────────────────────────────────────────────────────

class StartRequest(BaseModel):
    student_id: str


class AnswerRequest(BaseModel):
    question_id: str
    selected_answer: str  # "A" | "B" | "C" | "D"


# ── Helpers ──────────────────────────────────────────────────────────────────

def _oid(s: str) -> ObjectId:
    try:
        return ObjectId(s)
    except Exception:
        raise HTTPException(400, f"Invalid ID: {s}")


async def _get_session(session_id: str):
    db = get_db()
    doc = await db["sessions"].find_one({"_id": _oid(session_id)})
    if not doc:
        raise HTTPException(404, "Session not found")
    doc["id"] = str(doc["_id"])
    return doc


# ── Endpoints ────────────────────────────────────────────────────────────────

@router.post("/start")
async def start_session(body: StartRequest):
    """Create a new adaptive test session for a student."""
    db = get_db()
    doc = {
        "student_id": body.student_id,
        "ability_score": 0.5,
        "responses": [],
        "answered_ids": [],
        "status": "active",
        "created_at": datetime.utcnow(),
        "total_questions": 10,
        "study_plan": None,
    }
    result = await db["sessions"].insert_one(doc)
    return {"session_id": str(result.inserted_id), "message": "Session started"}


@router.get("/{session_id}/next-question")
async def next_question(session_id: str):
    """Return the next adaptive question based on current ability score."""
    session = await _get_session(session_id)

    if session["status"] == "completed":
        raise HTTPException(400, "Session already completed")

    if len(session["responses"]) >= session["total_questions"]:
        # Auto-mark as complete
        db = get_db()
        await db["sessions"].update_one(
            {"_id": _oid(session_id)}, {"$set": {"status": "completed"}}
        )
        return {"message": "Session complete — fetch /results", "completed": True}

    db = get_db()
    all_questions = await db["questions"].find({}).to_list(length=None)
    question = select_next_question(
        session["ability_score"], all_questions, session["answered_ids"]
    )
    if not question:
        return {"message": "No more questions available", "completed": True}

    return {
        "question_id": str(question["_id"]),
        "text": question["text"],
        "options": question["options"],
        "topic": question["topic"],
        "question_number": len(session["responses"]) + 1,
        "total_questions": session["total_questions"],
        "current_ability": round(session["ability_score"], 4),
    }


@router.post("/{session_id}/submit-answer")
async def submit_answer(session_id: str, body: AnswerRequest):
    """Submit an answer, update ability score via IRT, and return feedback."""
    session = await _get_session(session_id)

    if session["status"] == "completed":
        raise HTTPException(400, "Session already completed")

    db = get_db()
    question = await db["questions"].find_one({"_id": _oid(body.question_id)})
    if not question:
        raise HTTPException(404, "Question not found")

    if body.question_id in session["answered_ids"]:
        raise HTTPException(400, "Question already answered")

    is_correct = body.selected_answer.upper() == question["correct_answer"].upper()
    ability_before = session["ability_score"]
    ability_after = update_ability(ability_before, is_correct, question["difficulty"])

    response_doc = {
        "question_id": body.question_id,
        "selected_answer": body.selected_answer.upper(),
        "correct_answer": question["correct_answer"],
        "is_correct": is_correct,
        "difficulty": question["difficulty"],
        "topic": question["topic"],
        "ability_before": ability_before,
        "ability_after": ability_after,
    }

    new_count = len(session["responses"]) + 1
    new_status = "completed" if new_count >= session["total_questions"] else "active"

    await db["sessions"].update_one(
        {"_id": _oid(session_id)},
        {
            "$push": {
                "responses": response_doc,
                "answered_ids": body.question_id,
            },
            "$set": {
                "ability_score": ability_after,
                "status": new_status,
            },
        },
    )

    return {
        "is_correct": is_correct,
        "correct_answer": question["correct_answer"],
        "ability_before": ability_before,
        "ability_after": ability_after,
        "questions_answered": new_count,
        "session_complete": new_status == "completed",
    }


@router.get("/{session_id}/results")
async def get_results(session_id: str):
    """Return the full session summary with per-topic breakdown."""
    session = await _get_session(session_id)

    responses = session["responses"]
    total = len(responses)
    correct = sum(1 for r in responses if r["is_correct"])

    topic_stats: dict = {}
    for r in responses:
        t = r["topic"]
        if t not in topic_stats:
            topic_stats[t] = {"correct": 0, "total": 0}
        topic_stats[t]["total"] += 1
        if r["is_correct"]:
            topic_stats[t]["correct"] += 1

    topic_breakdown = [
        {
            "topic": t,
            "correct": v["correct"],
            "total": v["total"],
            "accuracy": round(v["correct"] / v["total"] * 100, 1),
        }
        for t, v in topic_stats.items()
    ]

    ability = session["ability_score"]
    return {
        "session_id": session_id,
        "student_id": session["student_id"],
        "status": session["status"],
        "ability_score": round(ability, 4),
        "level": "Beginner" if ability < 0.35 else "Intermediate" if ability < 0.65 else "Advanced",
        "total_questions": total,
        "correct_answers": correct,
        "accuracy": round(correct / total * 100, 1) if total else 0,
        "topic_breakdown": topic_breakdown,
        "responses": responses,
    }


@router.post("/{session_id}/study-plan")
async def get_study_plan(session_id: str):
    """Generate a personalised AI study plan using OpenAI."""
    session = await _get_session(session_id)

    if session.get("study_plan"):
        return session["study_plan"]

    plan = await generate_study_plan(session["ability_score"], session["responses"])

    db = get_db()
    await db["sessions"].update_one(
        {"_id": _oid(session_id)}, {"$set": {"study_plan": plan}}
    )
    return plan
