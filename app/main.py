from fastapi import FastAPI, Request
from app.pii_filter import create_analyzer, redact_pii
from app.openai_proxy import forward_to_openai

app = FastAPI()
analyzer = create_analyzer()

@app.get("/")
async def root():
    return {"status": "GDPR Proxy Service is running."}

@app.post("/v1/chat/completions")
async def proxy_openai(request: Request):
    original_payload = await request.json()
    # Redact user messages before forwarding to OpenAI
    messages = original_payload.get("messages", [])
    for message in messages:
        if message.get("role") == "user":
            original_content = message.get("content", "")
            message["content"] = redact_pii(original_content, analyzer)
    openai_response = await forward_to_openai(original_payload)
    return openai_response

@app.post("/analyze")
async def analyze(request: Request):
    payload = await request.json()
    text = payload.get("text", "")
    redacted_text = redact_pii(text, analyzer)
    return {"redacted_text": redacted_text}