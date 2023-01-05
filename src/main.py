import asyncio
import signal
import random

from loguru import logger

from config import config
from warp import clone_key, GetInfoData

from utilities import key_dispatcher, proxy_dispatcher


class SignalHandler:
    KEEP_PROCESSING: bool = True
    def __init__(self) -> None:
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame) -> None:
        logger.info('Received signal {}, stopiing all threads...'.format(signum))
        self.KEEP_PROCESSING = False


signal_handler = SignalHandler()


async def worker(id: int) -> None:
    logger.debug('Worker {} started'.format(id))

    while signal_handler.KEEP_PROCESSING:
        try:
            key: GetInfoData = await clone_key(
                key_dispatcher.get_key(),
                proxy_dispatcher.get_proxy(),
                len(config.DEVICE_MODELS) > 0 and random.choice(config.DEVICE_MODELS) or None,
            )

            key_dispatcher.add_key(key['license'])

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
    asyncio.run(main())
