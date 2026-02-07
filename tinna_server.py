import os
import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from openai import OpenAI

# =====================
# CONFIG
# =====================
load_dotenv()

MEMORY_FILE = "memory.json"

def save_memory():
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(conversation_history, f, ensure_ascii=False, indent=2)

# cargar memoria
try:
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            conversation_history = json.load(f)
    else:
        conversation_history = []
except json.JSONDecodeError:
    conversation_history = []

# =====================
# IA DE TINNA
# =====================
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

SYSTEM_PROMPT = """
You are Tinna, a virtual pet girl.
Speak in short sentences.
Show emotions clearly.
Never mention being an AI.
"""

def Tinna_AI(user_text: str):
    global conversation_history

    conversation_history.append({
        "role": "user",
        "content": user_text
    })

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *conversation_history
    ]

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        temperature=0.8
    )

    ai_response = response.choices[0].message.content.strip()

    conversation_history.append({
        "role": "assistant",
        "content": ai_response
    })

    save_memory()
    return ai_response

# =====================
# FASTAPI
# =====================
app = FastAPI()

@app.get("/")
def root():
    return {"status": "Tinna is online 🐰🔥"}

@app.post("/talk")
def talk(data: dict):
    user_text = data.get("text", "").strip()

    if not user_text:
        return {"reply": ""}

    reply = Tinna_AI(user_text)

    return JSONResponse(
        content={"reply": reply},
        media_type="application/json; charset=utf-8"
    )
