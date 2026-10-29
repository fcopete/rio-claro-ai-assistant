import json
from pathlib import Path
DATA_FILE=Path(__file__).parent.parent/"data"/"sample_data.json"
def load_sample_data():
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))
