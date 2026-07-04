import json
from pathlib import Path

# -------------------------------------------------------
# Define the path to the dataset
# -------------------------------------------------------

DATA_PATH = Path("Data/Raw/ordinex-sample-data.json")


# -------------------------------------------------------
# Function to load JSON
# -------------------------------------------------------

def load_dataset():
    """
    Loads the complete Ordinex dataset.
    """

    with open(DATA_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


# -------------------------------------------------------
# Function to extract regulations
# -------------------------------------------------------

def get_regulations(data):
    """
    Returns only the regulations section.
    """

    return data.get("regulations", [])


# -------------------------------------------------------
# Main Function
# -------------------------------------------------------

if __name__ == "__main__":

    dataset = load_dataset()

    regulations = get_regulations(dataset)

    print("=" * 70)
    print(f"Total Regulations Loaded : {len(regulations)}")
    print("=" * 70)

    for regulation in regulations:

        print(f"Reference : {regulation['ref']}")
        print(f"Country   : {regulation['country']}")
        print(f"Law       : {regulation['law']}")
        print(f"Category  : {regulation['category']}")
        print(f"Risk      : {regulation['risk_level']}")
        print(f"Clause    : {regulation['clause']}")
        print("-" * 70)