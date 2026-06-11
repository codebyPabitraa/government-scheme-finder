import json
import os

def load_and_process_schemes():
    with open("data/raw/schemes_full.json", "r", encoding="utf-8") as f:
        schemes = json.load(f)

    processed = []

    for scheme in schemes:
        name = scheme.get("schemeName", "Unknown")
        description = scheme.get("briefDescription", "").strip()
        category = scheme.get("schemeCategory", ["General"])
        if isinstance(category, list):
            category = ", ".join(category)
        state = scheme.get("beneficiaryState", ["All India"])
        if isinstance(state, list):
            state = ", ".join(state)
        ministry = scheme.get("nodalMinistryName", "")
        level = scheme.get("level", "")
        tags = scheme.get("tags", [])
        if isinstance(tags, list):
            tags = ", ".join(tags)

        text = f"""
Scheme Name: {name}
Description: {description}
Category: {category}
State: {state}
Ministry: {ministry}
Level: {level}
Tags: {tags}
        """.strip()

        processed.append({
            "text": text,
            "metadata": {
                "name": name,
                "category": category,
                "state": state,
                "ministry": ministry,
                "level": level
            }
        })

    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/schemes_processed.json", "w", encoding="utf-8") as f:
        json.dump(processed, f, indent=2, ensure_ascii=False)

    print(f"Processed {len(processed)} schemes successfully")
    return processed

if __name__ == "__main__":
    load_and_process_schemes()