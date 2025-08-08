import re

# ===== CONFIG =====
INPUT_FILE = "output.json"

# Terms to skip (case-sensitive)
EXCLUDE_TERMS = {
    "_id",
    "_tpl",
    "parentId",
    "hideout",
    "slotId",
    "upd",
    "UnlimitedCount",
    "StackObjectsCount",
    "count",
    "mod_stock_000",
"mod_reciever",
"mod_sight_rear",
"mod_scope",
"mod_barrel",
"mod_muzzle",
"mod_handguard",
"mod_sight_front",
"mod_mount_001",
"mod_tactical",
"mod_foregrip"
}

# ===== FUNCTIONS =====
def is_mongo_id(s):
    """Check if a string is a valid MongoDB ObjectId."""
    return bool(re.fullmatch(r"[0-9a-f]{24}", s))

# ===== MAIN SCRIPT =====
if __name__ == "__main__":
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    # Find all strings inside double quotes
    quoted_strings = re.findall(r'"([^"]*)"', text)

    # Filter out the ones we don't care about
    filtered_strings = [
        s for s in quoted_strings
        if s not in EXCLUDE_TERMS
    ]

    # Only keep the ones that aren't Mongo IDs
    non_ids = [s for s in filtered_strings if not is_mongo_id(s)]

    if non_ids:
        print("Strings that are NOT MongoDB ObjectIds (excluding known terms):")
        for s in non_ids:
            print(s)
    else:
        print("✅ All relevant quoted strings are valid MongoDB ObjectIds")
