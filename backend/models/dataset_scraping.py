from apify_client import ApifyClient
import time
import json
import os

# Replace this with your actual Apify API token
APIFY_API_TOKEN = "apify_api_TmHzKwMX8cGEihl3NZS9ZyZG1KDaEx1epiWA"

# Initialize the ApifyClient
client = ApifyClient(APIFY_API_TOKEN)

# Paste your 48-cuisine dictionary here
CUISINE_URLS = {
    "amish-and-mennonite": "https://www.allrecipes.com/recipes/732/us-recipes/amish-and-mennonite/",
    "argentinian": "https://www.allrecipes.com/recipes/2432/world-cuisine/latin-american/south-american/argentinian/",
    "australian-and-new-zealander": "https://www.allrecipes.com/recipes/228/world-cuisine/australian-and-new-zealander/",
    "austrian": "https://www.allrecipes.com/recipes/718/world-cuisine/european/austrian/",
    "bangladeshi": "https://www.allrecipes.com/recipes/16100/world-cuisine/asian/bangladeshi/",
    "belgian": "https://www.allrecipes.com/recipes/719/world-cuisine/european/belgian/",
    "brazilian": "https://www.allrecipes.com/recipes/1278/world-cuisine/latin-american/south-american/brazilian/",
    "cajun-and-creole": "https://www.allrecipes.com/recipes/272/us-recipes/cajun-and-creole/",
    "canadian": "https://www.allrecipes.com/recipes/733/world-cuisine/canadian/",
    "chilean": "https://www.allrecipes.com/recipes/1277/world-cuisine/latin-american/south-american/chilean/",
    "chinese": "https://www.allrecipes.com/recipes/695/world-cuisine/asian/chinese/",
    "colombian": "https://www.allrecipes.com/recipes/14759/world-cuisine/latin-american/south-american/colombian/",
    "cuban": "https://www.allrecipes.com/recipes/709/world-cuisine/latin-american/caribbean/cuban/",
    "danish": "https://www.allrecipes.com/recipes/1892/world-cuisine/european/scandinavian/danish/",
    "dutch": "https://www.allrecipes.com/recipes/720/world-cuisine/european/dutch/",
    "filipino": "https://www.allrecipes.com/recipes/696/world-cuisine/asian/filipino/",
    "finnish": "https://www.allrecipes.com/recipes/1893/world-cuisine/european/scandinavian/finnish/",
    "french": "https://www.allrecipes.com/recipes/721/world-cuisine/european/french/",
    "german": "https://www.allrecipes.com/recipes/722/world-cuisine/european/german/",
    "greek": "https://www.allrecipes.com/recipes/731/world-cuisine/european/greek/",
    "indian": "https://www.allrecipes.com/recipes/233/world-cuisine/asian/indian/",
    "indonesian": "https://www.allrecipes.com/recipes/698/world-cuisine/asian/indonesian/",
    "italian": "https://www.allrecipes.com/recipes/723/world-cuisine/european/italian/",
    "jamaican": "https://www.allrecipes.com/recipes/710/world-cuisine/latin-american/caribbean/jamaican/",
    "japanese": "https://www.allrecipes.com/recipes/699/world-cuisine/asian/japanese/",
    "jewish": "https://www.allrecipes.com/recipes/15965/us-recipes/jewish/",
    "korean": "https://www.allrecipes.com/recipes/700/world-cuisine/asian/korean/",
    "lebanese": "https://www.allrecipes.com/recipes/1824/world-cuisine/middle-eastern/lebanese/",
    "malaysian": "https://www.allrecipes.com/recipes/701/world-cuisine/asian/malaysian/",
    "norwegian": "https://www.allrecipes.com/recipes/1891/world-cuisine/european/scandinavian/norwegian/",
    "pakistani": "https://www.allrecipes.com/recipes/15974/world-cuisine/asian/pakistani/",
    "persian": "https://www.allrecipes.com/recipes/15937/world-cuisine/middle-eastern/persian/",
    "peruvian": "https://www.allrecipes.com/recipes/2433/world-cuisine/latin-american/south-american/peruvian/",
    "polish": "https://www.allrecipes.com/recipes/715/world-cuisine/european/eastern-european/polish/",
    "portuguese": "https://www.allrecipes.com/recipes/724/world-cuisine/european/portuguese/",
    "puerto-rican": "https://www.allrecipes.com/recipes/711/world-cuisine/latin-american/caribbean/puerto-rican/",
    "russian": "https://www.allrecipes.com/recipes/716/world-cuisine/european/eastern-european/russian/",
    "scandinavian": "https://www.allrecipes.com/recipes/725/world-cuisine/european/scandinavian/",
    "soul-food": "https://www.allrecipes.com/recipes/16091/us-recipes/soul-food/",
    "south-african": "https://www.allrecipes.com/recipes/15035/world-cuisine/african/south-african/",
    "southern": "https://www.allrecipes.com/recipes/15876/us-recipes/southern/",
    "spanish": "https://www.allrecipes.com/recipes/726/world-cuisine/european/spanish/",
    "swedish": "https://www.allrecipes.com/recipes/1890/world-cuisine/european/scandinavian/swedish/",
    "swiss": "https://www.allrecipes.com/recipes/727/world-cuisine/european/swiss/",
    "tex-mex": "https://www.allrecipes.com/recipes/17502/us-recipes/tex-mex/",
    "thai": "https://www.allrecipes.com/recipes/702/world-cuisine/asian/thai/",
    "turkish": "https://www.allrecipes.com/recipes/1825/world-cuisine/middle-eastern/turkish/",
    "vietnamese": "https://www.allrecipes.com/recipes/703/world-cuisine/asian/vietnamese/"
}

# Your actor ID (epctex recipe scraper)
ACTOR_ID = "iw2Kd0eeiv2DNadMk"

def trigger_and_fetch(cuisine, url):
    print(f"\nStarting run for: {cuisine}")
    run_input = {
        "search": "",
        "startUrls": [url],
        "maxItems": 100,
        "endPage": 1, # Remove/edit to prevent Apify from scraping only first page
        "extendOutputFunction": "($) => { return {} }",
        "customMapFunction": "(object) => { return {...object} }",
        "proxy": { "useApifyProxy": True }
    }

    # Trigger and wait for run to complete
    run = client.actor(ACTOR_ID).call(run_input=run_input)

    # Download dataset to file
    dataset_id = run["defaultDatasetId"]
    output_filename = f"{cuisine}_recipes.json"
    items = list(client.dataset(dataset_id).iterate_items())
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    print(f"Saved {cuisine} results to {output_filename}")

def merge_output():
    # Change this if your files are in a different folder
    INPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    OUTPUT_FILE = os.path.join(INPUT_DIR, "all_cuisines_combined.jsonl")

    combined_count = 0

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
        for filename in os.listdir(INPUT_DIR):
            if filename.endswith("_recipes.json"):
                cuisine = filename.replace("_recipes.json", "")
                path = os.path.join(INPUT_DIR, filename)

                try:
                    with open(path, "r", encoding="utf-8") as f:
                        recipes = json.load(f)
                        for recipe in recipes:
                            recipe["cuisine"] = cuisine
                            out_f.write(json.dumps(recipe, ensure_ascii=False) + "\n")
                            combined_count += 1
                    print(f"Merged {len(recipes)} recipes from {filename}")
                except Exception as e:
                    print(f"Failed to load {filename}: {e}")

    print(f"\nFinished. Total recipes merged: {combined_count}")
    print(f"📄 Output saved to: {OUTPUT_FILE}")

def main():
    for cuisine, url in CUISINE_URLS.items():
        trigger_and_fetch(cuisine, url)
        time.sleep(2)  # avoid hammering the API
    merge_output()

if __name__ == "__main__":
    main()