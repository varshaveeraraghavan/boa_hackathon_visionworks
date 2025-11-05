# BoA Simplification Hackathon - Team - VisionWorks 
# Duplicates detectives Dashboard

A **FastAPI-based backend** and **React-based dashboard** that helps teams **detect functional overlaps and redundancies across APIs** by analyzing their OpenAPI specifications.  

---

##  Introduction

Modern organizations often maintain hundreds of APIs across teams and systems — many of which do similar things.
This project aims to **discover such functional overlaps** automatically by:

1. Parsing API specifications (OpenAPI JSON)
2. Measuring similarity between API endpoints
3. Grouping them using **clustering algorithms**
4. Displaying insights visually on a clean, modern dashboard

---

## Features

✅ **OpenAPI Parsing** – Reads `.json` API specs from a folder  
✅ **Endpoint Comparison** – Uses string similarity to detect overlap  
✅ **Agglomerative Clustering** – Groups similar APIs dynamically  
✅ **Interactive Visualization** – Frontend shows clusters and scores  

---

##  Tech Stack

| Layer | Technology |
|--------|-------------|
| **Backend** | FastAPI, scikit-learn, NumPy |
| **Frontend** | React.js, Chart.js, Bootstrap |
| **Clustering Algorithm** | Agglomerative Clustering (Unsupervised ML) |
| **Similarity Metric** | SequenceMatcher (text-based similarity) |

---

#  Steps to Run 

##  1. Create a Virtual Environment
Create a new virtual environment named **api-sim** using Conda:

```bash
conda create -n api-sim python=3.10 -y
```
## Activate the Environment
```bash
conda activate api-sim
```
## Start the Backend (FastAPI)
Navigate to the backend directory, install dependencies, and start the FastAPI server:
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```
This will start the backend server (default: http://127.0.0.1:8000)

## Start the Frontend (React)

Open a new terminal window or tab, then run the following commands:
```bash
cd frontend
npm install
npm start
```
This will launch the React app on http://localhost:3000.


