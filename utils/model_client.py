import os
from autogen_ext.models.openai import OpenAIChatCompletionClient
from utils.logger import setup_logger

logger = setup_logger("model_client")


def get_model_client():
    """
    Initialize and return the model client used by all agents.
    Reads configuration from environment variables.
    """
    api_key = os.getenv("API_KEY")
    model_name = os.getenv("MODEL_NAME")

    if not api_key:
        logger.error("❌ OPENAI_API_KEY is missing. Please set it in your environment.")
        raise ValueError("OPENAI_API_KEY not set")

    try:
        logger.info(f"🧠 Initializing model client with model: {model_name}")
        model_client = OpenAIChatCompletionClient(model=model_name, api_key=api_key)
        return model_client
    except Exception as e:
        logger.exception(f"❌ Failed to initialize model client: {e}")
        raise
