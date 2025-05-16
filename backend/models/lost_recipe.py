import pandas as pd
import json

# Path to your JSONL file (adjust if needed)
jsonl_path = "models/data/all_cuisines_combined.jsonl"

# Read line-by-line and parse JSON objects
data = []
with open(jsonl_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            data.append(json.loads(line))
        except json.JSONDecodeError as e:
            print("Error reading line:", e)

df = pd.DataFrame(data)

# Optional: show all columns and a wider display for cleaner output
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

# Print a preview
print(df.head())
