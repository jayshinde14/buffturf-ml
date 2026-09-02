from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
import os

app = FastAPI(title="BuffTURF Recommendation Engine")

# Load the trained model and data matrix on startup
MODEL_PATH = "model.pkl"
DATA_PATH = "turf_user.pkl"

if not os.path.exists(MODEL_PATH) or not os.path.exists(DATA_PATH):
    print("WARNING: Model files not found. Please run train_model.py first.")
    model = None
    turf_user = None
else:
    try:
        model = joblib.load(MODEL_PATH)
        turf_user = joblib.load(DATA_PATH)
        print("Model loaded successfully!")
    except Exception as e:
        model = None
        turf_user = None
        print(f"Error loading models: {e}")

@app.get("/api/recommend")
def recommend(user_id: int, turf_id: int, top_n: int = 3):
    if model is None or turf_user is None:
        raise HTTPException(status_code=503, detail="Model is not trained yet.")
        
    # Cold start check: What if the turf is completely new and has no history?
    if turf_id not in turf_user.index:
        # Fallback: We don't have data for this turf, return empty list
        # In the Spring Boot backend, you'd catch this empty list and return most popular overall
        return {"recommended_turfs": []}
        
    try:
        # 1. Find the most similar turfs
        distances, indices = model.kneighbors(
            turf_user.loc[turf_id].values.reshape(1, -1), n_neighbors=top_n + 1)
        
        # 2. Get the turf IDs (skipping the first one because it's the turf itself)
        similar = [int(turf_user.index[i]) for i in indices.flatten()[1:]]
        
        return {"recommended_turfs": similar}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
