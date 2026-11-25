import json
from pathlib import Path

QUESTIONNAIRE_PATH = Path(__file__).parent.parent / "data" / "questions.json"

def load_questionnaire() -> dict:
    return json.loads(QUESTIONNAIRE_PATH.read_text(encoding="utf-8"))