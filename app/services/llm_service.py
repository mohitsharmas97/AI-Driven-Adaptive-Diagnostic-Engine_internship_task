"""
LLM Service — generates a personalized study plan via OpenAI.
The plan is a JSON object with:
  {
    "summary": "...",
    "steps": [
      {"step": 1, "title": "...", "description": "...", "resources": ["...", "..."]},
      ...
    ],
    "estimated_duration": "..."
  }
"""
import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

_client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)
MODEL = os.getenv("OPENAI_MODEL", "meta-llama/llama-3-8b-instruct")


def _build_prompt(
    ability_score: float,
    total_questions: int,
    accuracy: float,
    weak_topics: list[str],
    topic_accuracy: dict[str, float],
) -> str:
    level = "beginner" if ability_score < 0.35 else "intermediate" if ability_score < 0.65 else "advanced"
    return f"""
You are an expert GRE tutor. A student just completed a 10-question adaptive diagnostic test.
Here are their results:

- Ability Score (θ): {ability_score:.2f} / 1.00  (Level: {level})
- Overall Accuracy: {accuracy:.1f}%
- Weak Topics: {', '.join(weak_topics) if weak_topics else 'None — great work!'}
- Accuracy by Topic: {json.dumps(topic_accuracy, indent=2)}

Generate a personalized 3-step study plan to help them improve. Return ONLY valid JSON in this exact format:
{{
  "summary": "One sentence summarising the student's level and main improvement area.",
  "steps": [
    {{
      "step": 1,
      "title": "Short title for this step",
      "description": "2-3 sentence actionable description.",
      "resources": ["Resource 1", "Resource 2"]
    }},
    {{
      "step": 2,
      "title": "...",
      "description": "...",
      "resources": ["...", "..."]
    }},
    {{
      "step": 3,
      "title": "...",
      "description": "...",
      "resources": ["...", "..."]
    }}
  ],
  "estimated_duration": "e.g. 2 weeks of 30 min/day"
}}
"""


async def generate_study_plan(
    ability_score: float,
    responses: list,
) -> dict:
    total = len(responses)
    correct = sum(1 for r in responses if r["is_correct"])
    accuracy = (correct / total * 100) if total > 0 else 0

    topic_stats: dict[str, dict] = {}
    for r in responses:
        t = r["topic"]
        if t not in topic_stats:
            topic_stats[t] = {"correct": 0, "total": 0}
        topic_stats[t]["total"] += 1
        if r["is_correct"]:
            topic_stats[t]["correct"] += 1

    topic_accuracy = {
        t: round(v["correct"] / v["total"] * 100, 1)
        for t, v in topic_stats.items()
    }
    weak_topics = [t for t, acc in topic_accuracy.items() if acc < 50]

    prompt = _build_prompt(ability_score, total, accuracy, weak_topics, topic_accuracy)

    completion = await _client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        response_format={"type": "json_object"},
    )
    content = completion.choices[0].message.content
    return json.loads(content)


