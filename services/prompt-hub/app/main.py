import os, json
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Prompt Hub API", version="0.1.0")

# In-memory stub; replace with SQLAlchemy/real DB in production.
PROMPTS: Dict[str, Dict[int, Dict[str, Any]]] = {}

class Prompt(BaseModel):
    id: str
    version: int
    owner: str
    description: Optional[str] = None
    metadata: Dict[str, Any] = {}

@app.get("/healthz")
def health():
    return {"ok": True}

@app.post("/prompts", status_code=201)
def create_prompt(p: Prompt):
    versions = PROMPTS.setdefault(p.id, {})
    if p.version in versions:
        raise HTTPException(409, "Version exists")
    versions[p.version] = p.model_dump()
    return p

@app.get("/prompts/{pid}/{version}")
def get_prompt(pid: str, version: int):
    v = PROMPTS.get(pid, {}).get(version)
    if not v:
        raise HTTPException(404)
    return v

@app.get("/prompts/{pid}")
def list_versions(pid: str):
    return sorted(list(PROMPTS.get(pid, {}).keys()))
