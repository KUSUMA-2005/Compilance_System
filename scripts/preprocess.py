
import json
import re
from pathlib import Path

# Import our data loader
from data_loader import load_dataset, get_regulations

# ----------------------------------------
# Paths
# ----------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_PATH = BASE_DIR / "Data" / "Processed" / "regulations_processed.json"


# ----------------------------------------
# Clean Text
# ----------------------------------------

def clean_text(text):
    """
    Cleans regulation text.
    """

    if not text:
        return ""

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Remove leading/trailing spaces
    text = text.strip()

    return text


# ----------------------------------------
# Process Regulations
# ----------------------------------------

def preprocess_regulations():

    dataset = load_dataset()

    regulations = get_regulations(dataset)

    processed = []

    for regulation in regulations:

        processed.append({

            "id": regulation["ref"],

            "country": regulation["country"],

            "law": regulation["law"],

            "category": regulation["category"],

            "risk": regulation["risk_level"],

            "text": clean_text(regulation["clause"])

        })

    return processed


# ----------------------------------------
# Save
# ----------------------------------------

def save_processed_data(data):

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:

        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"\nSaved {len(data)} regulations")
    print(f"Location : {OUTPUT_PATH}")


# ----------------------------------------
# Main
# ----------------------------------------

if __name__ == "__main__":

    processed = preprocess_regulations()

    save_processed_data(processed)