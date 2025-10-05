import pandas as pd
import numpy as np
from lightfm import LightFM
from lightfm.data import Dataset
from scipy.sparse import coo_matrix
import joblib

MODEL_PATH = "app/artifacts/model.pkl"
USER_MAP_PATH = "app/artifacts/user_mapping.pkl"
ITEM_MAP_PATH = "app/artifacts/item_mapping.pkl"

def train_model(interactions_csv, user_features_csv=None, item_features_csv=None):
    # Load base interaction data
    df = pd.read_csv(interactions_csv)
    dataset = Dataset()
    
    # Build dataset structure
    users = df["user_id"].unique()
    items = df["item_id"].unique()
    dataset.fit(users, items)
    
    # Build interactions matrix
    (interactions, _) = dataset.build_interactions(
        [(x["user_id"], x["item_id"]) for _, x in df.iterrows()]
    )
    
    # Train LightFM model
    model = LightFM(loss="warp")
    model.fit(interactions, epochs=10, num_threads=4)
    
    # Save everything
    joblib.dump(model, MODEL_PATH)
    joblib.dump(users.tolist(), USER_MAP_PATH)
    joblib.dump(items.tolist(), ITEM_MAP_PATH)

    return {"message": "Model trained successfully", "num_users": len(users), "num_items": len(items)}

def recommend(user_id, k=5):
    model = joblib.load(MODEL_PATH)
    users = joblib.load(USER_MAP_PATH)
    items = joblib.load(ITEM_MAP_PATH)
    
    if user_id not in users:
        return []

    user_index = users.index(user_id)
    scores = model.predict(user_index, np.arange(len(items)))
    top_items = np.argsort(-scores)[:k]
    return [items[i] for i in top_items]

def update_model_incremental(feedback):
    """feedback is a list of (user_id, item_id) tuples"""
    model = joblib.load(MODEL_PATH)
    users, items = zip(*feedback)
    
    data = coo_matrix((np.ones(len(users)), (users, items)))
    model.fit_partial(data)
    
    joblib.dump(model, MODEL_PATH)
    print("Incrementally updated model with", len(feedback), "samples.")