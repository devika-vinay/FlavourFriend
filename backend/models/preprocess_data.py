import json
import pandas as pd

# Load the dataset
with open("data/train.json", "r") as file:
    data = json.load(file)

# Convert to a Pandas DataFrame
df = pd.DataFrame(data)

# Convert list of ingredients into a single string
df['ingredients'] = df['ingredients'].apply(lambda x: ', '.join(x))

print(df.head())

# Convert text to lowercase for consistency
df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)

# Save cleaned dataset
df.to_csv("data/cleaned_recipes.csv", index=False)
