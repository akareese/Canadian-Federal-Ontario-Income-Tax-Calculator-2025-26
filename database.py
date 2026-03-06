import json
import secrets
import string
from datetime import datetime

DB_FILE = "tax_database.json"


def load_database():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_database(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


def generate_tax_id(year: int | None = None) -> str:
    """
    Generates an ID like: TX-2026-8F3A-K21D
    - Uses secrets for high-quality randomness
    - Uppercase letters + digits, avoiding confusing characters
    """
    if year is None:
        year = datetime.now().year

    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

    part1 = "".join(secrets.choice(alphabet) for _ in range(4))
    part2 = "".join(secrets.choice(alphabet) for _ in range(4))

    return f"TX-{year}-{part1}-{part2}"


def store_tax_return(inputs, result):
    db = load_database()

    tax_id = generate_tax_id()
    while tax_id in db:
        tax_id = generate_tax_id()

    db[tax_id] = {
        "name": inputs.name,
        "province": inputs.province,

        "inputs": inputs.__dict__,
        "results": result.__dict__,

        "timestamp": datetime.now().isoformat()
    }

    save_database(db)
    return tax_id


def retrieve_tax_return(tax_id: str):
    db = load_database()
    return db.get(tax_id)