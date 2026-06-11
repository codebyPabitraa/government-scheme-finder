# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
# pyrefly: ignore [missing-import]
from pydantic import BaseModel
from typing import Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.retriever import rag_pipeline

app = FastAPI(title="Sarkar Yojana Finder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserQuery(BaseModel):
    age: int
    gender: str
    income: int
    caste: str
    state: str
    occupation: str
    extra: str = ""
    lang: Optional[str] = "en"  # "en", "hi", or "bn"

LANG_INSTRUCTIONS = {
    "hi": "Respond entirely in Hindi (Devanagari script).",
    "bn": "Respond entirely in Bengali (বাংলা script).",
}

@app.get("/")
def root():
    return {"status": "Sarkar Yojana Finder API is running 🇮🇳"}

@app.post("/find-schemes")
def find_schemes(data: UserQuery):
    lang_note = LANG_INSTRUCTIONS.get(data.lang, "")
    query = f"""
    I am a {data.age} year old {data.gender} from {data.state}.
    My annual family income is Rs {data.income}.
    I belong to {data.caste} category.
    My occupation is {data.occupation}.
    {f'I am looking for: {data.extra}' if data.extra else ''}
    What government schemes am I eligible for?
    {lang_note}
    """
    # rag_pipeline returns {"result": text, "links": [...]}
    pipeline_output = rag_pipeline(query)
    return {
        "result": pipeline_output.get("result", ""),
        "links": pipeline_output.get("links", [])
    }