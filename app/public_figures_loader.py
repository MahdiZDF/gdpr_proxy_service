# public_figures_loader.py
import json
from pathlib import Path

def load_public_figures(file_path: str = "data/public_figures_de.json") -> set:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Public figure file not found: {file_path}")
    
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    
    return set(item["personLabel"] for item in data if "personLabel" in item)
