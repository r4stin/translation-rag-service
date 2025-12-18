# RAG Translation Backend

This project implements a lightweight Retrieval-Augmented Generation (RAG)
backend for translation prompts.

The system stores translation examples, retrieves the most relevant ones
using similarity search, and builds prompts suitable for LLM-based translation.
An additional advanced component detects stammering in translated sentences.

---

## Features

- REST API built with FastAPI
- SQLite-based persistent storage for translation pairs
- Deduplication via database-level UNIQUE constraint
- TF-IDF + cosine similarity for retrieval
- Retrieval-Augmented prompt construction
- Heuristic stammering detection
- Dockerized for easy deployment

---

## Setup (Local)

### 1. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the server
```bash
uvicorn app.main:app --reload --port 8000
```

---

## Setup (Docker)

```bash
docker build -t translation-rag .
docker run -p 8000:8000 translation-rag
```

---

## API Usage

The provided `client.py` script can be used to interact with the service and
validate its behavior.

```bash
python client.py
```

The client allows you to:
1. Populate the database with translation pairs
2. Request translation prompts
3. Run stammering detection tests

---

## Design Choices

### Retrieval
TF-IDF was chosen for similarity search due to its simplicity,
interpretability, and suitability for small to medium-sized datasets.
It provides fast inference and avoids unnecessary infrastructure complexity.

### Persistence
SQLite is used as a lightweight persistence layer to ensure translation
pairs survive application restarts. Duplicate translation pairs are prevented
using a database-level UNIQUE constraint, making the API idempotent.

### Stammering Detection
Stammering is detected using deterministic, explainable heuristics that capture:
- Character flooding (e.g. `sooooo`)
- Repetition amplification introduced during translation
- Phrase-level repetition via n-gram analysis

The focus is on robustness and explainability rather than black-box models.

---

## Client Output

The following output was captured by running `client.py` after a clean setup:

```
Line 1: Response -> No (Expected: No)
Line 2: Response -> No (Expected: No)
Line 3: Response -> Yes (Expected: Yes)
Line 4: Response -> No (Expected: No)
Line 5: Response -> No (Expected: No)
Line 6: Response -> No (Expected: No)
Line 7: Response -> No (Expected: No)
Line 8: Response -> No (Expected: No)
Line 9: Response -> No (Expected: No)
Line 10: Response -> Yes (Expected: Yes)
Line 11: Response -> Yes (Expected: Yes)
Line 12: Response -> Yes (Expected: Yes)
```

---

## Notes & Future Improvements

- Cache TF-IDF vectorizers per language pair for larger datasets
- Replace TF-IDF with embedding-based retrieval if scale increases
- Add structured logging and monitoring for production deployment
