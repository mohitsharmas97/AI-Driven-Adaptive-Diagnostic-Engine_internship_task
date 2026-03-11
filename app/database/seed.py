"""
Seed script: populates MongoDB with 25 GRE-style questions
Run: python -m app.database.seed
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

QUESTIONS = [
    # ── ALGEBRA ──────────────────────────────────────────────────────────────
    {
        "text": "If 3x + 7 = 22, what is the value of x?",
        "options": {"A": "3", "B": "4", "C": "5", "D": "6"},
        "correct_answer": "C",
        "difficulty": 0.15,
        "topic": "Algebra",
        "tags": ["linear equations", "basic"],
    },
    {
        "text": "Solve for x: 2x² - 8 = 0",
        "options": {"A": "±1", "B": "±2", "C": "±4", "D": "±8"},
        "correct_answer": "B",
        "difficulty": 0.35,
        "topic": "Algebra",
        "tags": ["quadratic", "exponents"],
    },
    {
        "text": "If f(x) = x² - 3x + 2, what is f(4)?",
        "options": {"A": "4", "B": "5", "C": "6", "D": "7"},
        "correct_answer": "C",
        "difficulty": 0.45,
        "topic": "Algebra",
        "tags": ["functions", "substitution"],
    },
    {
        "text": "A train travels at 60 mph for 2.5 hours. How far did it travel?",
        "options": {"A": "120 miles", "B": "130 miles", "C": "140 miles", "D": "150 miles"},
        "correct_answer": "D",
        "difficulty": 0.20,
        "topic": "Algebra",
        "tags": ["word problem", "rate"],
    },
    {
        "text": "Simplify: (x³ · x⁴) / x²",
        "options": {"A": "x⁵", "B": "x⁷", "C": "x⁹", "D": "x¹²"},
        "correct_answer": "A",
        "difficulty": 0.55,
        "topic": "Algebra",
        "tags": ["exponent rules"],
    },
    # ── GEOMETRY ─────────────────────────────────────────────────────────────
    {
        "text": "What is the area of a circle with radius 7? (Use π ≈ 3.14)",
        "options": {"A": "43.96", "B": "153.86", "C": "44.0", "D": "49.0"},
        "correct_answer": "B",
        "difficulty": 0.25,
        "topic": "Geometry",
        "tags": ["circle", "area"],
    },
    {
        "text": "In a right triangle, the legs are 3 and 4. What is the hypotenuse?",
        "options": {"A": "5", "B": "6", "C": "7", "D": "8"},
        "correct_answer": "A",
        "difficulty": 0.20,
        "topic": "Geometry",
        "tags": ["Pythagorean theorem"],
    },
    {
        "text": "The sum of interior angles of a hexagon is:",
        "options": {"A": "540°", "B": "620°", "C": "720°", "D": "900°"},
        "correct_answer": "C",
        "difficulty": 0.40,
        "topic": "Geometry",
        "tags": ["polygons", "angles"],
    },
    {
        "text": "Two parallel lines are cut by a transversal. If one co-interior angle is 70°, the other is:",
        "options": {"A": "70°", "B": "90°", "C": "110°", "D": "120°"},
        "correct_answer": "C",
        "difficulty": 0.50,
        "topic": "Geometry",
        "tags": ["parallel lines", "transversal"],
    },
    {
        "text": "A cone has radius 3 and height 4. What is its volume? (Use π ≈ 3.14)",
        "options": {"A": "37.68", "B": "75.36", "C": "113.04", "D": "150.72"},
        "correct_answer": "A",
        "difficulty": 0.65,
        "topic": "Geometry",
        "tags": ["3D", "volume", "cone"],
    },
    # ── VOCABULARY ───────────────────────────────────────────────────────────
    {
        "text": "Choose the word closest in meaning to EPHEMERAL:",
        "options": {"A": "Eternal", "B": "Transient", "C": "Permanent", "D": "Robust"},
        "correct_answer": "B",
        "difficulty": 0.45,
        "topic": "Vocabulary",
        "tags": ["synonyms", "GRE word"],
    },
    {
        "text": "GARRULOUS most nearly means:",
        "options": {"A": "Silent", "B": "Angry", "C": "Talkative", "D": "Stubborn"},
        "correct_answer": "C",
        "difficulty": 0.50,
        "topic": "Vocabulary",
        "tags": ["synonyms", "GRE word"],
    },
    {
        "text": "LOQUACIOUS is closest to:",
        "options": {"A": "Articulate", "B": "Verbose", "C": "Reserved", "D": "Sarcastic"},
        "correct_answer": "B",
        "difficulty": 0.55,
        "topic": "Vocabulary",
        "tags": ["synonyms"],
    },
    {
        "text": "PERNICIOUS most nearly means:",
        "options": {"A": "Harmless", "B": "Clever", "C": "Beneficial", "D": "Harmful"},
        "correct_answer": "D",
        "difficulty": 0.60,
        "topic": "Vocabulary",
        "tags": ["synonyms", "advanced"],
    },
    {
        "text": "Select the antonym of OBDURATE:",
        "options": {"A": "Stubborn", "B": "Flexible", "C": "Rigid", "D": "Harsh"},
        "correct_answer": "B",
        "difficulty": 0.70,
        "topic": "Vocabulary",
        "tags": ["antonyms", "GRE word"],
    },
    # ── READING COMPREHENSION ────────────────────────────────────────────────
    {
        "text": "Passage: Renewable energy sources, such as solar and wind, have grown significantly in recent years. While they produce no direct emissions, their manufacturing can be energy-intensive.\n\nWhat is the main idea of this passage?",
        "options": {
            "A": "Renewables are perfect solutions",
            "B": "Manufacturing always outweighs benefits",
            "C": "Renewables have grown but carry production trade-offs",
            "D": "Solar is better than wind",
        },
        "correct_answer": "C",
        "difficulty": 0.30,
        "topic": "Reading Comprehension",
        "tags": ["main idea", "environment"],
    },
    {
        "text": "Passage: The placebo effect demonstrates the power of belief on physiology. Patients given sugar pills have reported reduced pain, often rivalling real medication.\n\nThe passage implies that:",
        "options": {
            "A": "Sugar should replace medicine",
            "B": "Belief can influence physical outcomes",
            "C": "Placebos are ineffective",
            "D": "Pain is always psychological",
        },
        "correct_answer": "B",
        "difficulty": 0.40,
        "topic": "Reading Comprehension",
        "tags": ["inference", "science"],
    },
    {
        "text": "Passage: Although ancient civilisations lacked modern technology, they built remarkably precise structures aligned with astronomical events.\n\nThe author's tone is best described as:",
        "options": {"A": "Dismissive", "B": "Admiring", "C": "Skeptical", "D": "Indifferent"},
        "correct_answer": "B",
        "difficulty": 0.45,
        "topic": "Reading Comprehension",
        "tags": ["tone", "history"],
    },
    {
        "text": "Passage: Automation threatens many traditional jobs. However, historically, technology has also created new categories of employment.\n\nThe passage presents:",
        "options": {
            "A": "A one-sided view against automation",
            "B": "A nuanced view with both risks and historical precedent",
            "C": "Strong support for automation",
            "D": "A call to ban automation",
        },
        "correct_answer": "B",
        "difficulty": 0.55,
        "topic": "Reading Comprehension",
        "tags": ["balanced argument", "economics"],
    },
    {
        "text": "Passage: Stoicism teaches that external events are beyond our control; only our reactions are within our power.\n\nAccording to Stoicism, what should one focus on?",
        "options": {
            "A": "Changing external events",
            "B": "Avoiding all difficult situations",
            "C": "Controlling one's own responses",
            "D": "Ignoring all emotions",
        },
        "correct_answer": "C",
        "difficulty": 0.35,
        "topic": "Reading Comprehension",
        "tags": ["philosophy", "direct recall"],
    },
    # ── QUANTITATIVE REASONING ───────────────────────────────────────────────
    {
        "text": "If the average of 5 numbers is 18, what is their sum?",
        "options": {"A": "72", "B": "80", "C": "90", "D": "95"},
        "correct_answer": "C",
        "difficulty": 0.20,
        "topic": "Quantitative Reasoning",
        "tags": ["averages", "arithmetic"],
    },
    {
        "text": "A bag contains 5 red, 3 blue, and 2 green balls. What is P(picking a blue ball)?",
        "options": {"A": "1/5", "B": "3/10", "C": "1/3", "D": "2/5"},
        "correct_answer": "B",
        "difficulty": 0.35,
        "topic": "Quantitative Reasoning",
        "tags": ["probability", "combinatorics"],
    },
    {
        "text": "Column A: √144    Column B: 13     Which is greater?",
        "options": {
            "A": "Column A",
            "B": "Column B",
            "C": "They are equal",
            "D": "Cannot be determined",
        },
        "correct_answer": "B",
        "difficulty": 0.25,
        "topic": "Quantitative Reasoning",
        "tags": ["comparison", "roots"],
    },
    {
        "text": "A 10% discount is applied to a $250 item, then a further 20% discount. Final price?",
        "options": {"A": "$170", "B": "$175", "C": "$180", "D": "$185"},
        "correct_answer": "C",
        "difficulty": 0.50,
        "topic": "Quantitative Reasoning",
        "tags": ["percentages", "successive discount"],
    },
    {
        "text": "What is the mode of the data set: [4, 7, 2, 7, 3, 4, 7, 9]?",
        "options": {"A": "4", "B": "7", "C": "5.375", "D": "9"},
        "correct_answer": "B",
        "difficulty": 0.15,
        "topic": "Quantitative Reasoning",
        "tags": ["statistics", "mode"],
    },
]


async def seed():
    load_dotenv()
    uri = os.getenv("MONGODB_URI", "mongodb://127.0.0.1:27017")
    client = AsyncIOMotorClient(uri)
    db = client["adaptive_diagnostic"]

    col = db["questions"]
    existing = await col.count_documents({})
    if existing > 0:
        print(f"⚠️  {existing} questions already in DB — dropping and re-seeding.")
        await col.drop()

    result = await col.insert_many(QUESTIONS)
    print(f"✅ Seeded {len(result.inserted_ids)} questions into 'questions' collection.")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
