import pandas as pd
from fastapi import HTTPException
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Load cleaned recipe data
df = pd.read_csv("models/data/cleaned_recipes.csv")

# Vectorize the full dataset for use across all recipes
vectorizer = TfidfVectorizer()
ingredient_matrix = vectorizer.fit_transform(df['ingredients'])

# Thresholds
HIGH_SIM_THRESHOLD = 0.09
MEDIUM_SIM_THRESHOLD = 0.06
TOP_N = 5

def generate_fusion_recipe(cuisine1, cuisine2):
    #Generates a fusion recipe by combining two cuisines.
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

    # Extract ingredient text and split for logic
    text1 = recipe1['ingredients'].values[0]
    text2 = recipe2['ingredients'].values[0]
    ingredients1 = text1.split(', ')
    ingredients2 = text2.split(', ')

     # Compute Cosine Similarity 
    vec1 = vectorizer.transform([text1])
    vec2 = vectorizer.transform([text2])
    similarity = cosine_similarity(vec1, vec2)[0][0]

    if similarity >= HIGH_SIM_THRESHOLD:
        # High compatibility — merge all
        fusion_ingredients = sorted(set(ingredients1 + ingredients2))
        note = "High similarity — full fusion applied."
    elif similarity >= MEDIUM_SIM_THRESHOLD:
        # Medium compatibility — keep top N TF-IDF ingredients from each
        top_1 = get_top_n_ingredients(text1, TOP_N)
        top_2 = get_top_n_ingredients(text2, TOP_N)
        fusion_ingredients = sorted(set(top_1 + top_2))
        note = f"Medium similarity — reduced fusion applied (top {TOP_N} ingredients each)."
    else:
        # Incompatible — abort
        raise HTTPException(
            status_code=400,
            detail=f"Fusion not allowed: cuisines too different (similarity = {round(similarity, 3)})."
        )

    fusion_name = f"{cuisine1.title()}-{cuisine2.title()} Fusion Dish"

    return {
        "fusion_recipe_name": fusion_name,
        "ingredients": ', '.join(fusion_ingredients),
        "cosine_similarity": round(similarity, 3),
        "note": note
    }

def get_top_n_ingredients(text, n):
    # Returns top N ingredients based on TF-IDF scores.
    vec = vectorizer.transform([text])
    feature_array = vectorizer.get_feature_names_out()
    print("feature_array", feature_array)
    tfidf_scores = vec.toarray()[0]
    top_n_indices = tfidf_scores.argsort()[-n:][::-1]
    return [feature_array[i] for i in top_n_indices if tfidf_scores[i] > 0]