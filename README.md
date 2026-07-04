# Ordinex – AI Compliance Management System

## 📌 Overview

Ordinex is an AI-powered compliance management platform that helps startups and businesses analyze company policies against national and international regulations.

The system uses Natural Language Processing (NLP), Semantic Search, and Retrieval-Augmented Generation (RAG) to detect compliance gaps, assign risk levels, and generate actionable recommendations.

---

## 🚀 Features

- AI-powered document analysis
- Semantic regulation matching
- Compliance gap detection
- Risk scoring
- Multi-country regulation support
- AI-generated compliance recommendations
- Compliance dashboard
- Audit history
- Real-time regulation updates
- Industry-specific compliance

---

## 🛠 Tech Stack

### AI

- Sentence Transformers
- SpaCy
- ChromaDB
- Llama 3.1 (RAG)

### Backend

- Python
- FastAPI

### Database

- MongoDB

### Frontend

- React
- Chart.js

---

## 📂 Project Structure

```
Compilance_System/

Backend/
Frontend/
Data/
scripts/
vector_db/
models/
reports/
requirements.txt
README.md
```

---

## Installation

```bash
git clone <repository-url>

cd Compilance_System

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python -m spacy download en_core_web_sm
```

---

## Running

```bash
python scripts/data_loader.py

python scripts/preprocess.py

python scripts/embedder.py
```

---

## Team Members

- Member 1 – AI Engine
- Member 2 – Backend
- Member 3 – Frontend
- Member 4 – Testing & Integration