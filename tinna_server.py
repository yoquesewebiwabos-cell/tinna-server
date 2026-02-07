from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os, json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = FastAPI()

# 🔥 CORS (Unity lo agradece)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_KEY = os.environ.get("GROQ_KEY")

client = OpenAI(
    api_key=GROQ_KEY,
    base_url="https://api.groq.com/openai/v1"
)

SYSTEM_PROMPT = "You are Tinna, a virtual pet girl."

@app.get("/")
def root():
    return {"status": "online"}

# ✅ ENDPOINT CLARO
@app.post("/chat")
def chat(data: dict):
    text = data.get("text", "").strip()
    if not text:
        return {"reply": ""}

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ]
    )

    reply = response.choices[0].message.content
    return {"reply": reply}