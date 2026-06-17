import json
from pathlib import Path

SAMPLE_PATH = Path(__file__).resolve().parents[3] / "data" / "sample_idealista.json"

def get_anuncios():
    with open(SAMPLE_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return data["elementList"]