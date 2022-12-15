import asyncio
import random

from typing import NoReturn

from config import config
from warp import clone_key, GetInfoData


async def worker() -> NoReturn:
    keys = config.BASE_KEYS.split(',')

    while True:
        try:
            key: GetInfoData = await clone_key(
                random.choice(keys)
            )

            keys.append(key['license'])

            print(
                '{} | {}'.format(
                    key['license'],
                    key['referral_count'],
                )
            )
        except Exception as e:
            pass

        await asyncio.sleep(config.DELAY)

async def main() -> None:
    tasks = []

    for _ in range(config.THREADS_COUNT):
        tasks.append(
            asyncio.create_task(worker())
        )

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
