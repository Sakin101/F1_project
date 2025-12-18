
RSS_FEEDS=[
    "https://www.the-race.com/rss",
    "",
    "",
    ]

DB_CONN_STING="postgresql+psycopg2://f1:F1@localhost:5432/project_db"

CLASSIFICATION_PROMPT_TEMPLATE = """
Classify the following article title into exactly one category:

Categories:
1. HARD_NEWS – factual reporting of a real event or announcement
2. OPINION_ANALYSIS – subjective commentary, ranking, or judgment
3. EXPLAINER – factual explanation without a specific event

Title:
"{title}"

Return only the category name.
""".strip()

KEYWORD_MAP = {
    "F1": [
        "formula 1",
        "f1",
        "grand prix",
        "fia",
        "verstappen",
        "hamilton",
        "leclerc",
        "ferrari",
        "red bull",
        "mercedes",
        "concorde agreement",
    ],
    "FORMULA_E": [
        "formula e",
        "gen3",
        "gen4",
        "abb formula e",
    ],
    "MOTOGP": [
        "motogp",
        "moto gp",
        "ducati",
        "yamaha",
        "aprilia",
        "quartararo",
        "marquez",
    ],
    "INDYCAR": [
        "indycar",
        "indy 500",
        "indianapolis",
    ],
    "WEC": [
        "wec",
        "world endurance",
        "le mans",
        "hypercar",
        "lmdh",
        "lmh",
    ],
    "WRC": [
        "wrc",
        "world rally",
        "rally",
    ],
    "ESPORTS": [
        "esports",
        "sim racing",
        "iracing",
        "f1 esports",
    ],
}
MOTORSPORT_CLASSIFICATION_PROMPT = """
Classify the following article title into exactly one motorsport category.

Categories:
- F1
- FORMULA_E
- MOTOGP
- INDYCAR
- WEC
- WRC
- ESPORTS
- OTHER

Title:
"{title}"

Return only the category name.
""".strip()