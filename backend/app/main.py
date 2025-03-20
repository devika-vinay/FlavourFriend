from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models.train_fusion import generate_fusion_recipe

app = FastAPI()

# Define request model
class FusionRequest(BaseModel):
    cuisine1: str
    cuisine2: str

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the AI-powered Cooking App!"}

# Fusion recipe endpoint (using trained model)
@app.post("/fusion")
def fusion_recipe(request: FusionRequest):
    return generate_fusion_recipe(request.cuisine1, request.cuisine2)
