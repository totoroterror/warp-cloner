from itertools import count

from config import config


class KeyDispenser():
    def __init__(self, keys: list[str] = []) -> None:
        self.keys: list[str] = keys

        self.key_counter = iter(count())

    def add_key(self, key: str) -> None:
        self.keys.append(key)

    def get_key(self) -> str:
        if self.keys is None or len(self.keys) == 0:
            raise Exception('No keys available')

        return self.keys[next(self.key_counter) % len(self.keys)]


key_dispatcher: KeyDispenser = KeyDispenser(config.BASE_KEYS)
