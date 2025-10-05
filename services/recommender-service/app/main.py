from fastapi import FastAPI, Query
from app.model import train_model, recommend

app = FastAPI(title="Recommender Service")

@app.post("/train")
def train():
    return train_model("app/data/interactions.csv")

@app.get("/recommend")
def get_recommendations(user_id: int = Query(...), k: int = 5):
    return {"user_id": user_id, "recommendations": recommend(user_id, k)}