import json
from pathlib import Path
from typing import Dict

TEMPLATE_PATH = Path("data/legal_templates/clauses.json")

def load_clause_templates() -> Dict[str, str]:
    """
    Load clause templates from JSON file and return as a dictionary.
    Keys are clause types (e.g., 'NDA', 'Termination'), values are example texts.
    """
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"Clause template file not found at {TEMPLATE_PATH}")

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
