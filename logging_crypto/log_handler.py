import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
handler = RotatingFileHandler(
    'monitor_bot_activity.logs', maxBytes=50000000, backupCount=5,
)
logger.addHandler(handler)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
