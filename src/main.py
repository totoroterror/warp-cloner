import asyncio
import random

from typing import NoReturn
from loguru import logger

from config import config
from warp import clone_key, GetInfoData


async def worker(id: int) -> NoReturn:
    logger.debug('Worker {} started'.format(id))

    keys = config.BASE_KEYS.split(',')

    while True:
        try:
            key: GetInfoData = await clone_key(
                random.choice(keys)
            )

            keys.append(key['license'])

            output = config.OUTPUT_FORMAT.format(
                key=key['license'],
                referral_count=key['referral_count'],
            )

            logger.success(output)

            with open(config.OUTPUT_FILE, 'a') as file:
                file.write(output + '\n')
        except Exception as e:
            logger.error(e)
            pass

        await asyncio.sleep(config.DELAY)

async def main() -> None:
    tasks = []

    for i in range(config.THREADS_COUNT):
        tasks.append(
            asyncio.create_task(worker(i + 1))
        )

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
