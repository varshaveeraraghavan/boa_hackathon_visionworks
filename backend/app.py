from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json, os
from pathlib import Path
from difflib import SequenceMatcher
import numpy as np
from sklearn.cluster import AgglomerativeClustering

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Load OpenAPI specs ---
def load_specs():
    specs_dir = Path(__file__).parent / "mock_specs"
    apis = {}
    for file in specs_dir.glob("*.json"):
        with open(file) as f:
            data = json.load(f)
            name = data["info"]["title"]
            endpoints = []
            for path, methods in data.get("paths", {}).items():
                for method, details in methods.items():
                    summary = details.get("summary", "")
                    endpoints.append(f"{method.upper()} {path} - {summary}")
            apis[name] = {"endpoints": endpoints, "description": data["info"].get("description", "")}
    return apis

# --- Similarity computation ---
def text_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def compute_similarity(apis):
    names = list(apis.keys())
    n = len(names)
    sim_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                sim_matrix[i][j] = 1
            else:
                a_text = " ".join(apis[names[i]]["endpoints"])
                b_text = " ".join(apis[names[j]]["endpoints"])
                sim_matrix[i][j] = text_similarity(a_text, b_text)
    return names, sim_matrix

@app.get("/api/similarity")
def get_similarity():
    apis = load_specs()
    names, sim_matrix = compute_similarity(apis)

    # Cluster
    clustering = AgglomerativeClustering(
        n_clusters=None, distance_threshold=0.6, affinity='precomputed', linkage='average'
    ).fit(1 - sim_matrix)

    results = []
    for i, name in enumerate(names):
        results.append({
            "api_name": name,
            "description": apis[name]["description"],
            "cluster": int(clustering.labels_[i])
        })

    return {"apis": results, "similarity": sim_matrix.tolist(), "names": names}
