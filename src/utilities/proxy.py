import itertools

from config import config


class ProxyDispatcher():
    def __init__(self, proxy_file: str | None) -> None:
        if proxy_file is None:
            return

        with open(proxy_file, 'r') as file:
            self.proxies: list[str] = file.read().splitlines()

        self.proxy_counter: itertools.cycle[int] = itertools.cycle(range(len(self.proxies)))

    def get_proxy(self) -> str | None:
        if self.proxies is None:
            return None

        return self.proxies[next(self.proxy_counter) % len(self.proxies)]


proxy_dispatcher: ProxyDispatcher = ProxyDispatcher(config.PROXY_FILE)
