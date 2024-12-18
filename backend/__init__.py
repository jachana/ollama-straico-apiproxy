from os import environ
from app import logging

logger = logging.getLogger(__name__)

STRAICO_API_KEY = environ["STRAICO_API_KEY"]
logger.debug(f"STRAICO_API_KEY={STRAICO_API_KEY}")

if STRAICO_API_KEY.strip().upper() == "TEST":
    from .test import prompt_completion, list_model, user_detail

    logger.info("Using Test Backend")
else:
    from .straico import (
        prompt_completion,
        list_model,
        list_agents,
        delete_agent,
        user_detail,
        image_generation,
        list_rags,
        delete_rag,
        create_rag,
        get_model_mapping,
        create_agent,
        update_agent,
    )

    logger.info("Using Straico Backend")
