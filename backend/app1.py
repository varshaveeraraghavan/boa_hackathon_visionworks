from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os, json
import numpy as np
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer, util

# Initialize FastAPI
app = FastAPI(title="API Similarity Dashboard (Semantic Version)")

# Enable CORS (so React frontend can access it)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load pre-trained sentence-transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# --- Function to Load API Specs ---
def load_api_specs(spec_folder="mock_specs"):
    apis = []
    for file in os.listdir(spec_folder):
        if file.endswith(".json"):
            with open(os.path.join(spec_folder, file), "r") as f:
                data = json.load(f)
                name = data.get("info", {}).get("title", file.replace(".json", ""))
                desc = data.get("info", {}).get("description", "")
                paths = " ".join(data.get("paths", {}).keys())
                combined_text = f"{name} {desc} {paths}"
                apis.append({"api_name": name, "description": desc, "text": combined_text})
    return apis

# --- Compute Semantic Similarity ---
def compute_semantic_similarity(api_texts):
    embeddings = model.encode(api_texts, convert_to_tensor=True)
    sim_matrix = util.cos_sim(embeddings, embeddings).cpu().numpy()
    return sim_matrix

# --- Cluster APIs ---
def cluster_apis(apis):
    api_texts = [api["text"] for api in apis]
    similarity_matrix = compute_semantic_similarity(api_texts)

    # Convert similarity into feature vectors for clustering
    features = np.array(similarity_matrix)
    num_clusters = min(3, len(apis))  # Up to 3 clusters
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init="auto")
    clusters = kmeans.fit_predict(features)

    for i, api in enumerate(apis):
        api["cluster"] = int(clusters[i])

    return {
        "apis": apis,
        "similarity": similarity_matrix.tolist(),
        "names": [api["api_name"] for api in apis]
    }

# --- API Endpoint ---
@app.get("/api/similarity")
def get_api_similarity():
    apis = load_api_specs()
    result = cluster_apis(apis)
    return result

# --- Root Endpoint ---
@app.get("/")
def root():
    return {"message": "API Similarity Semantic Dashboard is running 🚀"}
