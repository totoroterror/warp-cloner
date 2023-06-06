from itertools import cycle

from config import config


class ProxyDispatcher():
    proxies: list[str] | None = None

    def __init__(self, proxy_file: str | None) -> None:
        if proxy_file is None or proxy_file == '':
            return

        with open(proxy_file, 'r') as file:
            self.proxies = file.read().splitlines()

        self.proxy_cycle = cycle(self.proxies)

    def get_proxy(self) -> str | None:
        if self.proxies is None:
            return None

        return next(self.proxy_cycle)


proxy_dispatcher: ProxyDispatcher = ProxyDispatcher(config.PROXY_FILE)
