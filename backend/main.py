from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime, timezone
import json
import uuid
import os

from supabase import create_client, Client


# -----------------------------
# Project paths
# -----------------------------
ROOT = Path(__file__).resolve().parents[1]

QUESTIONS = json.loads(
    (ROOT / "frontend" / "questions.json").read_text(encoding="utf-8")
)


# -----------------------------
# Supabase connection
# -----------------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client | None = None

if SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY:
    supabase = create_client(
        SUPABASE_URL,
        SUPABASE_SERVICE_ROLE_KEY
    )


# -----------------------------
# FastAPI
# -----------------------------
app = FastAPI(title="ScrollWise Survey API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Request model
# -----------------------------
class Submission(BaseModel):
    answers: dict


# -----------------------------
# Health check
# -----------------------------
@app.get("/api/health")
def health():

    return {
        "ok": True,
        "database": supabase is not None
    }


# -----------------------------
# Submit response
# -----------------------------
@app.post("/api/submit")
def submit(body: Submission):

    if supabase is None:
        return {
            "ok": False,
            "error": "Database is not configured"
        }

    response_id = "R-" + uuid.uuid4().hex[:10].upper()

    timestamp = datetime.now(timezone.utc).isoformat()

    age_group = body.answers.get("Q02", "")


    # Build database row
    row = {
        "response_id": response_id,
        "timestamp": timestamp,
        "age_group": age_group
    }


    # Add Q01-Q36
    for q in QUESTIONS:

        question_id = q["id"]

        value = body.answers.get(question_id, "")

        if isinstance(value, list):
            value = "; ".join(map(str, value))

        row[question_id.lower()] = value


    # Insert into Supabase
    result = (
        supabase
        .table("responses")
        .insert(row)
        .execute()
    )


    return {
        "ok": True,
        "response_id": response_id
    }