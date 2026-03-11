"""
1-Dimension Item Response Theory (IRT) Adaptive Engine
=======================================================
Algorithm:
  1. Session starts with ability θ = 0.5
  2. P(correct | θ, b) = 1 / (1 + exp(-1.7 * (θ - b)))
     where b = item difficulty (0.0 – 1.0)
  3. After each response:
       - Correct:   θ += lr * (1 - P)   → ability rises
       - Incorrect: θ -= lr * P          → ability falls
     θ is clamped to [0.01, 0.99]
  4. Next question: pick unanswered item with difficulty closest to current θ
  5. Session completes after `total_questions` responses
"""
import math
from typing import List, Dict, Any, Optional

LEARNING_RATE = 0.3


def probability_correct(ability: float, difficulty: float) -> float:
    """IRT 1PL (Rasch-like) probability of a correct response."""
    return 1 / (1 + math.exp(-1.7 * (ability - difficulty)))


def update_ability(ability: float, is_correct: bool, difficulty: float) -> float:
    """Update θ using IRT gradient rule."""
    p = probability_correct(ability, difficulty)
    if is_correct:
        new_ability = ability + LEARNING_RATE * (1 - p)
    else:
        new_ability = ability - LEARNING_RATE * p
    return round(max(0.01, min(0.99, new_ability)), 4)


def select_next_question(
    ability: float,
    all_questions: List[Dict[str, Any]],
    answered_ids: List[str],
) -> Optional[Dict[str, Any]]:
    """Return the unanswered question whose difficulty is closest to ability θ."""
    candidates = [q for q in all_questions if str(q["_id"]) not in answered_ids]
    if not candidates:
        return None
    return min(candidates, key=lambda q: abs(q["difficulty"] - ability))
