import os
import logging
from dotenv import load_dotenv

# Initialize logging for configuration module
logger = logging.getLogger("config_module")

# Load environment variables strictly from .env
load_dotenv()

class Config:
    """Class holding system configurations and validation logic."""
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    @classmethod
    def validate(cls) -> bool:
        """Ensure GEMINI_API_KEY exists and satisfies format boundaries."""
        key = cls.GEMINI_API_KEY
        if not key or not isinstance(key, str) or len(key.strip()) < 10:
            logger.warning("Configuration Check: GEMINI_API_KEY is not defined or is invalid.")
            return False
        logger.info("Configuration Check: GEMINI_API_KEY loaded and verified.")
        return True
