from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
import traceback

from app.pii_filter import create_analyzer, redact_pii
from app.openai_proxy import forward_to_openai

# Configure logging to DEBUG level to see detailed logs
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize FastAPI app and analyzer
app = FastAPI()
analyzer = create_analyzer()

# Global exception handler (catches any unhandled exceptions)
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception occurred", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"}
    )

# Health check endpoint
@app.get("/")
async def root():
    return {"status": "GDPR Proxy Service is running."}

# Main endpoint: redact user message and forward it to OpenAI
@app.post("/v1/chat/completions")
async def proxy_openai(request: Request):
    try:
        # Parse incoming JSON body
        original_payload = await request.json()
        logger.debug(f"Incoming payload: {original_payload}")

        # Redact user messages before sending to OpenAI
        messages = original_payload.get("messages", [])
        for message in messages:
            if message.get("role") == "user":
                original_content = message.get("content", "")
                redacted = redact_pii(original_content, analyzer)
                logger.debug(f"Original: {original_content}")
                logger.debug(f"Redacted: {redacted}")
                message["content"] = redacted

        # Ensure required model field is set
        if "model" not in original_payload:
            original_payload["model"] = "gpt-3.5-turbo"
            logger.debug("Model not specified — defaulting to gpt-3.5-turbo")

        # Send redacted payload to OpenAI
        logger.debug(f"Forwarding payload to OpenAI: {original_payload}")
        openai_response = await forward_to_openai(original_payload)
        logger.debug(f"Response from OpenAI: {openai_response}")

        return openai_response

    except Exception as e:
        # If anything goes wrong, log full stack trace
        logger.error("Error in /v1/chat/completions", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal Server Error",
                "details": str(e)  # Optional: remove in production
            }
        )

# Endpoint to test redaction separately
@app.post("/analyze")
async def analyze(request: Request):
    payload = await request.json()
    text = payload.get("text", "")
    redacted_text = redact_pii(text, analyzer)
    return {"redacted_text": redacted_text}
