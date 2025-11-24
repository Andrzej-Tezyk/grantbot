from typing import List, Dict, Any
from app.utils import settings
import logging


log = logging.getLogger("grantbot-api")


class TextGeneratorService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER