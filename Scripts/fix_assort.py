import json
import re
from bson import ObjectId  # pip install pymongo

# ===== CONFIG =====
INPUT_FILE = "input.json"
OUTPUT_FILE = "output.json"

# ===== HELPERS =====
def generate_mongo_id():
    """Generate a real MongoDB ObjectId string."""
    return str(ObjectId())

def is_mongo_id(s):
    """Check if a string is a valid MongoDB ObjectId."""
    return isinstance(s, str) and bool(re.fullmatch(r"[0-9a-f]{24}", s))

# ===== STEP 1: COLLECT _id VALUES =====
def collect_ids(obj, ids):
    """Recursively collect _id field values."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "_id" and isinstance(v, str):
                ids.add(v)
            collect_ids(v, ids)
    elif isinstance(obj, list):
        for item in obj:
            collect_ids(item, ids)

# ===== STEP 2: REPLACE ALL OCCURRENCES =====
def replace_ids(obj, id_map):
    """Recursively replace IDs in keys and values."""
    if isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            new_key = id_map.get(k, k)
            new_value = replace_ids(v, id_map)
            if isinstance(new_value, str):
                new_value = id_map.get(new_value, new_value)
            new_dict[new_key] = new_value
        return new_dict
    elif isinstance(obj, list):
        return [replace_ids(item, id_map) for item in obj]
    elif isinstance(obj, str):
        return id_map.get(obj, obj)
    return obj

# ===== STEP 3: FIX NON-MONGOS IN _tpl, barter_scheme, loyal_level_items =====
def fix_special_fields(obj):
    """Replace non-Mongo IDs in _tpl, barter_scheme, loyal_level_items."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            # Fix _tpl fields
            if k == "_tpl" and isinstance(v, str) and not is_mongo_id(v):
                obj[k] = generate_mongo_id()

            # Fix barter_scheme values
            if k == "barter_scheme" and isinstance(v, dict):
                for scheme in v.values():
                    if isinstance(scheme, list):
                        for entry_list in scheme:
                            if isinstance(entry_list, list):
                                for entry in entry_list:
                                    if isinstance(entry, dict) and "_tpl" in entry:
                                        if not is_mongo_id(entry["_tpl"]):
                                            entry["_tpl"] = generate_mongo_id()

            # Fix loyal_level_items values
            if k == "loyal_level_items" and isinstance(v, dict):
                keys_to_replace = []
                for item_id in list(v.keys()):  # iterate safely
                    if not is_mongo_id(item_id):
                        keys_to_replace.append(item_id)
                for old_key in keys_to_replace:
                    v[generate_mongo_id()] = v.pop(old_key)

            fix_special_fields(v)

    elif isinstance(obj, list):
        for item in obj:
            fix_special_fields(item)


    elif isinstance(obj, list):
        for item in obj:
            fix_special_fields(item)

# ===== MAIN SCRIPT =====
if __name__ == "__main__":
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Pass 1: Replace _id everywhere
    old_ids = set()
    collect_ids(data, old_ids)
    id_map = {old_id: generate_mongo_id() for old_id in old_ids}
    data = replace_ids(data, id_map)

    # Pass 2: Fix _tpl, barter_scheme, loyal_level_items if non-Mongo
    fix_special_fields(data)

    # Save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"✅ Replaced {len(id_map)} _id values and fixed special fields. Saved to {OUTPUT_FILE}")
