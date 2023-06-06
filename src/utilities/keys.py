from config import config
from .mutable_cycle import mutable_cycle


class KeyDispenser():
    def __init__(self, keys: list[str] = []) -> None:
        self.keys: list[str] = keys

        self.key_cycle = mutable_cycle(self.keys)

    def add_key(self, key: str) -> None:
        self.keys.append(key)

    def get_key(self) -> str:
        if self.keys is None or len(self.keys) == 0:
            raise Exception('No keys available')

        return next(self.key_cycle)


key_dispatcher: KeyDispenser = KeyDispenser(config.BASE_KEYS)
