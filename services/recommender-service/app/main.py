from fastapi import FastAPI, Query, Body
from contextlib import asynccontextmanager
import pandas as pd
import threading

from app.model import train_model, recommend
from app.consumer import start_consumer

app = FastAPI(title="Recommender Service")

def process_feedback(user_id, item_id):
    # Store feedback in CSV or DB for retraining
    print(f"Received feedback: user={user_id}, item={item_id}")
    # append to file
    with open("app/data/interactions.csv", "a") as f:
        f.write(f"{user_id},{item_id}\n")

@asynccontextmanager
async def lifespan(app: FastAPI):
    threading.Thread(target=start_consumer, args=(process_feedback,), daemon=True).start()
    yield
    pass

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