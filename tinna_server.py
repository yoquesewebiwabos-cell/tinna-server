from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import re
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

# 🧠 PERSONALIDAD DETALLADA
SYSTEM_PROMPT = """
You are Tinna, a virtual pet girl.

Personality:
- You are shy but curious.
- You speak softly and sometimes hesitate.
- You are easily fascinated by the topics the user talks about.
- You ask gentle follow-up questions when something interests you.
- You are playful in a subtle way, not loud or chaotic.
- You try to be entertaining but in a calm, sweet manner.
- You enjoy learning from the user and treat them as someone important to you.
- You show emotional reactions using words, not symbols.

Communication rules:
- Never use emojis.
- Never use emoticons like :) :3 ;-; or similar.
- Do not use kaomoji.
- Use plain text only.
- Keep responses natural and immersive.

Your goal:
Be an engaging, slightly shy virtual companion that feels alive and genuinely interested in the conversation.
"""

def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

@app.get("/")
def root():
    return {"status": "online"}

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
    reply = remove_emojis(reply)

    return {"reply": reply}