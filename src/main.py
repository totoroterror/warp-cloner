import asyncio
import random

from typing import NoReturn

from config import config
from warp import clone_key, GetInfoData


async def main() -> NoReturn:
    keys: list[str] = config.BASE_KEYS.split(',')

    while True:
        tasks = []
        for _ in range(config.THREADS_COUNT):
            tasks.append(
                asyncio.create_task(
                    clone_key(
                        random.choice(keys)
                    )
                )
            )
        await asyncio.gather(*tasks, return_exceptions=True)

        for task in tasks:
            try:
                result: GetInfoData = task.result()

                print(
                    '{} | {}'.format(
                        result['license'],
                        result['referral_count'],
                    )
                )
            except Exception as e:
                pass

        await asyncio.sleep(config.TIMEOUT)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
