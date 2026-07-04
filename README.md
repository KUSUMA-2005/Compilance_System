# Ordinex Backend

Backend and database module for **Ordinex**, an AI-powered regulatory
compliance platform. This service owns:

- Document upload (PDF/DOCX) and metadata storage
- Regulation management (CRUD)
- Compliance report storage
- Dashboard aggregation
- Audit history

It does **not** implement NLP, embeddings, LLMs, RAG, machine learning, or
any frontend — those are separate modules that connect to the endpoints
and placeholder service functions defined here.

## Tech stack

- Python 3.11+
- FastAPI
- MongoDB via Motor (async driver)
- Pydantic v2 / pydantic-settings
- Uvicorn (ASGI server)

## Project structure

```
backend/
├── app/
│   ├── main.py            # FastAPI app, routers, middleware, lifespan
│   ├── config.py          # Settings (env-var driven)
│   ├── database.py        # Motor client lifecycle + index creation
│   ├── models/             # Mongo document models (Pydantic)
│   ├── routes/             # API routers
│   ├── services/           # Business logic / data access
│   ├── schemas/             # Request/response schemas
│   ├── utils/               # Logging, security, files, exceptions, pagination
│   └── middleware/          # Request logging + global exception handlers
├── uploads/                 # Uploaded PDF/DOCX files (git-ignored)
├── reports/                 # Reserved for generated report files (git-ignored)
├── logs/                    # Rotating app log file (git-ignored)
├── tests/                   # Pytest suite (uses mongomock-motor, no real DB needed)
├── requirements.txt
└── .env.example
```

## Getting started

### 1. Prerequisites

- Python 3.11+
- A running MongoDB instance (local `mongod`, Docker, or MongoDB Atlas)

### 2. Install dependencies

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# edit .env — at minimum set MONGO_URI if not using local MongoDB on the default port
```

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

The API is now available at `http://localhost:8000`.

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI schema: `http://localhost:8000/openapi.json`

### 5. Run tests

Tests use `mongomock-motor` (an in-memory Motor-compatible mock), so no
real MongoDB instance is required to run the suite:

```bash
pytest
```

## API overview

All routes are mounted under `API_V1_PREFIX` (default `/api/v1`).

| Method | Path                          | Description                                             |
| ------ | ------------------------------ | --------------------------------------------------------- |
| POST   | `/upload`                      | Upload a PDF/DOCX policy document                        |
| POST   | `/analyze`                     | Request analysis of a policy — **placeholder response**  |
| GET    | `/dashboard`                   | Aggregate stats: policies, reports, regulations, recent  |
| GET    | `/report/{id}`                 | Fetch a stored compliance report                          |
| GET    | `/reports`                     | List compliance reports (paginated)                       |
| POST   | `/reports`                     | Create a compliance report (used by the AI/engine module) |
| PUT    | `/reports/{id}`                | Update a compliance report                                 |
| DELETE | `/reports/{id}`                | Delete a compliance report                                 |
| GET    | `/regulations`                 | List regulations (paginated, filterable)                  |
| POST   | `/regulations`                 | Insert a regulation                                        |
| GET    | `/regulations/{id}`            | Get a regulation                                            |
| PUT    | `/regulations/{id}`            | Update a regulation                                         |
| DELETE | `/regulations/{id}`            | Delete a regulation                                          |
| GET    | `/policies`                    | List uploaded policies                                       |
| GET    | `/policies/{id}`               | Get a policy's metadata                                       |
| DELETE | `/policies/{id}`               | Delete a policy and its stored file                           |
| POST   | `/users`                       | Create a user                                                  |
| GET    | `/users`                       | List users                                                      |
| GET    | `/users/{id}`                  | Get a user                                                        |
| PUT    | `/users/{id}`                  | Update a user                                                      |
| DELETE | `/users/{id}`                  | Delete a user                                                       |
| GET    | `/audit-history`               | List audit log entries (filterable by `policy_id`)                  |

All list endpoints accept `page` and `page_size` query params and return
`{ total, page, page_size, total_pages, items }`.

### `POST /analyze` — placeholder by design

```json
{
  "policy_id": "64f1c2a5e1b2c3d4e5f6a7b8",
  "status": "Pending Analysis",
  "message": "Document queued. This will be processed by the NLP/compliance engine module once connected."
}
```

The endpoint validates the policy exists, flips its status to
`Pending Analysis`, writes an audit log entry, and calls
`run_nlp_pipeline()` — which currently just returns dummy JSON. No real
document analysis happens in this module.

## Integration points for other modules

`app/services/ai_placeholder_service.py` defines three stub functions with
stable signatures for the NLP/AI team to implement against:

```python
run_nlp_pipeline(policy_id: str, file_path: str) -> dict
run_compliance_engine(policy_id: str, extracted_clauses: list[dict] | None) -> dict
generate_ai_recommendation(policy_id: str, violations: list[dict] | None) -> dict
```

Once real analysis is implemented, the expected flow is:

1. `POST /analyze` (already implemented here) marks the policy pending.
2. The NLP/AI module extracts text, runs its pipeline, and computes a
   score + violations + recommendations.
3. The AI module calls `POST /reports` (already implemented here) to
   persist the result as a `ComplianceReportModel` document.
4. `GET /report/{id}` and `GET /dashboard` (already implemented here)
   immediately reflect the new report — no backend changes needed.

## Database collections

| Collection          | Purpose                                              | Key indexes                              |
| -------------------- | ------------------------------------------------------ | ------------------------------------------- |
| `users`               | Registered accounts                                       | `email` (unique)                              |
| `regulations`         | Regulatory clauses per country/law/category                | `country + law + category`                    |
| `policies`             | Uploaded company documents + status                          | `upload_date`, `status`                          |
| `compliance_reports`   | Score, violations, recommendations per policy                  | `policy_id`, `created_at`                          |
| `audit_logs`           | Immutable action trail (upload, analyze, CRUD events)             | `policy_id`, `timestamp`                              |

Indexes are created automatically on startup (see `app/database.py`).

## Seed data

`scripts/sample_data.json` + `scripts/seed_data.py` populate a full,
internally-consistent dataset covering every scenario the data model
supports:

- **32 real, verified regulations** — 3 categories (Data Privacy,
  Cybersecurity, Finance) × 3 countries (India, UAE, Singapore), 2-5
  distinct clauses per cell, each citing a real section/notice number
  (e.g. DPDPA Section 6, 7, 9; IT Act Sections 43, 43A, 66, 72A; PMLA
  Rule 9(1); UAE PDPL, Cybercrimes Law, AML Decree-Law 10/2025; Singapore
  PDPA, Cybersecurity Act 2018/2024, MAS Notice 626)
- **4 narrative companies**, each with its own user and a consistent
  regulatory footprint (see the `companies` array in the JSON):
  Ordinex Labs (global, multi-jurisdiction), BrightLedger Pte Ltd
  (Singapore), NexPay Financial Services (UAE), Aarambh FinTech Pvt Ltd
  (India)
- **21 policies spanning all 4 statuses**: `Uploaded`, `Pending Analysis`,
  `Analyzed`, `Failed` — roughly 5-6 per company
- **18 compliance reports spanning all 3 risk bands**, including the
  score **0** (total non-compliance), **50** and **80** (exact dashboard
  bucket boundaries), and **100** (perfect score) edge values
- **Three remediation-over-time stories** — P3, P6, and P8 each have two
  reports showing the compliance score improve after a fix
- **Edge-case filenames and sizes**: an emoji + punctuation filename at
  1 byte under the 20MB upload limit, an Arabic (non-ASCII) filename at
  512 bytes, a 200+ character filename, and a 12-byte near-empty file
- **Every audit action type**, including two `POLICY_DELETED` entries
  that reference policies no longer present in the `policies` collection
  — demonstrating that the audit trail is append-only and outlives the
  records it describes

Run it against a real MongoDB instance:

```bash
cd backend
python -m scripts.seed_data
```

Note: policy documents are seeded as metadata only — no real files are
written to `uploads/`. Use `POST /upload` if you need an actual file on
disk behind a policy record.

## Design notes / scope boundaries

- **No auth flow implemented.** `password_hash` is stored using `bcrypt`
  directly, but there is no login/JWT/session endpoint — that's expected
  to be added by whichever module owns authentication.
- **Audit logs are append-only.** There's a `log_action()` service
  function and a read-only `/audit-history` endpoint, but intentionally no
  update/delete route — mutating an audit trail defeats its purpose.
- **No NLP/AI/ML code.** `run_nlp_pipeline`, `run_compliance_engine`, and
  `generate_ai_recommendation` are stubs that return dummy JSON, as
  specified.
