"""Utils"""

from app.utils.config import Settings
from app.utils.logging import get_custom_logger

settings = Settings()

log = get_custom_logger(__name__, "grantbot-api")
