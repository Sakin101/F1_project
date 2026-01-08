
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
You are classifying motorsport news titles.

Tasks:
1. Classify the title into exactly one motorsport category.
2. Extract motorsport-specific entities that strongly indicate this category
   (e.g., drivers, teams, manufacturers, championships).

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

Return JSON strictly in this format:
  "category": "CATEGORY",
  "entities": ["entity1", "entity2"]

""".strip()

websites=["https://www.the-race.com/rss","https://www.motorsport.com/rss/f1/news","https://www.planetf1.com/rss","https://www.racefans.net/feed/","https://racingnews365.com/feed/news.xml","https://www.autosport.com/rss/f1/news/"]