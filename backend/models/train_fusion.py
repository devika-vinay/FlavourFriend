import pandas as pd
from fastapi import HTTPException


# Load cleaned recipe data
df = pd.read_csv("models/data/cleaned_recipes.csv")

def generate_fusion_recipe(cuisine1, cuisine2):
    """Generates a fusion recipe by combining two cuisines."""
    cuisine1 = cuisine1.lower().strip()
    cuisine2 = cuisine2.lower().strip()

    # Error: Check if both cuisines are the same
    if cuisine1 == cuisine2:
        raise HTTPException(status_code=400, detail="Please select two different cuisines.")

    # Error: Check if cuisines exist in the dataset
    if cuisine1 not in df['cuisine'].unique():
        raise HTTPException(status_code=404, detail=f"Cuisine '{cuisine1}' not found in the dataset.")
    if cuisine2 not in df['cuisine'].unique():
        raise HTTPException(status_code=404, detail=f"Cuisine '{cuisine2}' not found in the dataset.")

    # Select random recipes from each cuisine
    recipe1 = df[df['cuisine'] == cuisine1].sample(n=1)
    recipe2 = df[df['cuisine'] == cuisine2].sample(n=1)

    # Extract ingredient lists as sets (to ignore order)
    ingredients1 = set(recipe1['ingredients'].values[0].split(', '))
    ingredients2 = set(recipe2['ingredients'].values[0].split(', '))

    # Error: Check if both cuisines have identical ingredients (ignoring order)
    if ingredients1 == ingredients2:
        raise HTTPException(status_code=400, detail="Both cuisines have identical ingredients. No fusion possible.")

    # Combine ingredients for fusion dish
    fusion_ingredients = list(ingredients1.union(ingredients2))
    fusion_name = f"{cuisine1.title()}-{cuisine2.title()} Fusion Dish"

    return {
        "fusion_recipe_name": fusion_name,
        "ingredients": ', '.join(fusion_ingredients)
    }