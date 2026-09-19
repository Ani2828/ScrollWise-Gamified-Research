from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openpyxl import load_workbook
from pathlib import Path
from datetime import datetime, timezone
import uuid, json

ROOT=Path(__file__).resolve().parents[1]
BOOK=ROOT/"data"/"Social_Media_Research.xlsx"
QUESTIONS=json.loads((ROOT/"frontend"/"questions.json").read_text(encoding="utf-8"))
app=FastAPI(title="ScrollWise Survey API")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])

class Submission(BaseModel):
    answers: dict

@app.get("/api/health")
def health(): return {"ok":True}

@app.post("/api/submit")
def submit(body:Submission):
    wb=load_workbook(BOOK)
    ws=wb["Responses"]
    row=["R-"+uuid.uuid4().hex[:10].upper(),datetime.now(timezone.utc).isoformat(),body.answers.get("Q02","")]
    for q in QUESTIONS:
        v=body.answers.get(q["id"],"")
        row.append("; ".join(map(str,v)) if isinstance(v,list) else v)
    ws.append(row); wb.save(BOOK)
    return {"ok":True}
