try:
    from dotenv import load_dotenv

    load_dotenv()
except:
    pass
from os import environ

from app import app, logging, log_level
from api_endpoints import lm_studio
from api_endpoints import lm_studio_tts
from api_endpoints import ollama


if app.EMBEDDING_ENABLED:
    from api_endpoints import lm_studio_embedding
    from api_endpoints import ollama_embedding

if app.TRANSCRIPTION_ENABLED:
    from api_endpoints import lm_studio_transcription

import uvicorn

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.info("Starting the web server")
    is_debug = log_level in ["INFO", "DEBUG"]
    HOST = environ.get("HOST", "0.0.0.0")
    PORT = int(environ.get("PORT", "3214"))
    uvicorn.run(app, host=HOST, port=PORT, log_level=log_level.lower())
