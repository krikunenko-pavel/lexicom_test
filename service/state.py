from typing import Optional
from misc.redis import Connection


class State:
    def __init__(self, conf: dict):
        self.conf: dict = conf
        self.redis: Optional[Connection] = None
