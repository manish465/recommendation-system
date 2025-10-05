from fastapi import FastAPI, Query, Body
from app.model import train_model, recommend
import datetime
import pandas as pd

app = FastAPI(title="Recommender Service")

@app.post("/train")
def train(interactions: list[dict] = Body(None)):
    """
    Retrain model.
    Optional: pass new interactions as a JSON list:
    [{"user_id": 1, "item_id": 101}, ...]
    """
    if interactions:
        # Append new data to CSV
        df_new = pd.DataFrame(interactions)
        df_existing = pd.read_csv("app/data/interactions.csv")
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_csv("app/data/interactions.csv", index=False)
    return train_model("app/data/interactions.csv")

@app.get("/recommend")
def get_recommendations(user_id: int = Query(...), k: int = 5):
    return {"user_id": user_id, "recommendations": recommend(user_id, k)}

@app.post("/feedback")
def feedback(event: dict = Body(...)):
    """
    Receive a new user-item interaction:
    {"user_id": 1, "item_id": 101}
    """
    df_existing = pd.read_csv("app/data/interactions.csv")
    df_new = pd.DataFrame([event])
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined.to_csv("app/data/interactions.csv", index=False)
    return {"message": "Feedback recorded"}