import logging
import google.generativeai as genai
from config import Config

logger = logging.getLogger("ai_module")

def configure_gemini():
    """Configure the google-generativeai package with the validated API key."""
    if not Config.validate():
        raise ValueError("Invalid or missing Gemini API Key. Please configure it in your .env file.")
    logger.info("Configuring google.generativeai SDK with Config key.")
    genai.configure(api_key=Config.GEMINI_API_KEY)

def format_history_for_gemini(messages: list) -> list:
    """Format SQLite messages into standard google-generativeai chat history format, filtering out errors."""
    history = []
    for m in messages:
        # Filter out system/API error messages from model conversation context
        if m["content"].startswith("⚠️ [Error:"):
            continue
        # roles must be strictly 'user' and 'model'
        role = "user" if m["role"] == "user" else "model"
        history.append({
            "role": role,
            "parts": [m["content"]]
        })
    logger.info(f"Formatted {len(history)} messages into chat history structures.")
    return history

def create_chat_session(history: list, system_instruction: str, temperature: float):
    """Create a new GenerativeModel and start a chat session with the given history."""
    logger.info("Initializing google.generativeai chat session.")
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config={"temperature": temperature},
            system_instruction=system_instruction
        )
        return model.start_chat(history=history)
    except Exception as e:
        logger.error(f"Error starting GenerativeModel chat session: {e}", exc_info=True)
        raise

def generate_stream(chat_session, prompt: str):
    """
    Generator yielding response chunks from the model.
    Propagates exceptions to the caller for structured error handling in the UI.
    """
    logger.info(f"AI stream request: '{prompt[:30]}...'")
    try:
        response_stream = chat_session.send_message(prompt, stream=True)
        for chunk in response_stream:
            try:
                # Safely verify candidates and parts exist to avoid triggering quick accessor validation errors
                if chunk.candidates and chunk.candidates[0].content.parts:
                    text = chunk.text
                    if text:
                        yield text
            except (ValueError, AttributeError, IndexError) as val_err:
                # Chunks containing only metadata or safety ratings won't have text parts
                logger.debug(f"Skipping metadata-only stream chunk: {val_err}")
                continue
    except Exception as e:
        logger.error(f"GenerativeAI streaming API call failed: {e}", exc_info=True)
        raise e
