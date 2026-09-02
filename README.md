# 🤖 BuffTURF Machine Learning Recommendation Engine

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10" />
  <img src="https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Scikit--Learn-NearestNeighbors-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn" />
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
</p>

---

## 🌟 Overview

The **BuffTURF Recommendation Engine** is an intelligent microservice built with **FastAPI** and **Scikit-Learn**. It implements item-based collaborative filtering using the **k-Nearest Neighbors (k-NN)** algorithm to provide personalized, high-affinity sports venue recommendations to players based on historical match booking patterns.

The engine connects directly with the Spring Boot core backend (`GET /api/recommend`) to serve real-time recommendations on venue discovery and detail pages.

---

## 🧠 Machine Learning Methodology

1. **User-Turf Interaction Matrix:** A sparse matrix structured across player bookings and venue affinities.
2. **Nearest Neighbors Algorithm:** Utilizes cosine distance metric to identify turfs with similar booking distributions and user overlapping behaviors.
3. **Cold-Start Handling:** Gracefully handles unseen venues by returning empty matches, triggering the Spring Boot service to fall back to top-rated regional popularity rankings.
4. **Model Serialization:** Models and pre-computed matrix indices are serialized using `joblib` for rapid in-memory inference with sub-5ms response latency.

---

## 📋 API Specification

### Venue Recommendation Endpoint
```http
GET /api/recommend?user_id={userId}&turf_id={turfId}&top_n=3
```

#### Request Parameters:
| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `user_id` | integer | Yes | - | ID of the authenticated player |
| `turf_id` | integer | Yes | - | Currently viewed turf venue ID |
| `top_n` | integer | No | 3 | Number of top recommendations to return |

#### Sample Response (`200 OK`):
```json
{
  "recommended_turfs": [12, 5, 8]
}
```

---

## 💻 Local Setup & Execution

### Prerequisites
* Python 3.10+
* pip

### 1. Installation
```bash
cd buffturf-ml
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Model Training & Data Generation
```bash
# Seed synthetic booking matrix
python seed_data.py

# Train Nearest Neighbors model
python train_model.py
```

### 3. Launch Microservice
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```
Interactive Swagger API documentation is available at `http://localhost:8000/docs`.

---

## 🐳 Docker Containerization

The microservice includes a lightweight Docker container based on `python:3.10-slim`:

```bash
# Build image
docker build -t buffturf-ml .

# Run container on port 8000
docker run -d -p 8000:8000 --name buffturf_ml buffturf-ml
```

---

## 📄 Copyright & Proprietary Rights

**Copyright © 2026 Jay Shinde. All Rights Reserved.**

This machine learning service, models, algorithms, and training pipelines are the exclusive intellectual property of **Jay Shinde**.
* **Viewing & Evaluation:** You are granted permission to view and examine this repository for portfolio review, recruitment, and technical evaluation purposes.
* **Restrictions:** Unauthorized copying, reproduction, modification, redistribution, sublicensing, reverse engineering, or commercial use of any portion of this codebase without prior written permission from the copyright owner is strictly prohibited.
