import json
import logging
import os

logger = logging.getLogger(__name__)

CONFIG_ENV_KEY = "SRVC_CONFIG"


def read_config():
    path = os.environ.get(CONFIG_ENV_KEY)
    if not os.path.exists(path):
        logger.error(f'Config file not found at {path}')
        return None
    with open(path, 'r') as fd:
        return json.load(fd)
