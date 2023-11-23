import asyncio
import signal
import random
import aiohttp
from typing import Optional, Tuple

from loguru import logger

from config import config
from warp import RegisterData, clone_key, GetInfoData

from utilities import key_dispatcher, proxy_dispatcher


class SignalHandler:
    KEEP_PROCESSING: bool = True
    def __init__(self) -> None:
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame) -> None:
        logger.info('Received signal {}, stopping all threads...'.format(signum))
        self.KEEP_PROCESSING = False


signal_handler = SignalHandler()


async def custom_clone_key(key_to_clone: str, retry_count: int = 0) -> Optional[Tuple[GetInfoData, RegisterData, Optional[str]]]:
    if retry_count > config.RETRY_COUNT or not signal_handler.KEEP_PROCESSING:
        return None

    try:
        key, register_data, private_key = await clone_key(
            key_to_clone,
            proxy_dispatcher.get_proxy(),
            len(config.DEVICE_MODELS) > 0 and random.choice(config.DEVICE_MODELS) or None,
        )

        key_dispatcher.add_key(key['license'])

        return key, register_data, private_key
    except Exception as e:
        logger.error('{} (key: {}, retry count: {})'.format(
            e,
            key_to_clone,
            retry_count
        ))

        if config.DELAY > 0 and signal_handler.KEEP_PROCESSING:
            await asyncio.sleep(config.DELAY)

        return await custom_clone_key(key_to_clone, retry_count + 1)


async def worker(id: int) -> None:
    logger.debug('Worker {} started'.format(id))

    while signal_handler.KEEP_PROCESSING:
        response = await custom_clone_key(
            key_dispatcher.get_key(),
        )

        if response != None:
            key, register_data, private_key = response
            
            if config.PUSH_API:
                try:
                    async with aiohttp.ClientSession() as session:
                        await session.post(config.PUSH_API, json={'license': key['license']})
                        logger.success('License key pushed to API')
                except Exception as e:
                    logger.error(f'Failed to push license key to API: {e}')

            output: str = config.OUTPUT_FORMAT.format(
                key=key['license'],
                referral_count=key['referral_count'],
                private_key=config.SAVE_WIREGUARD_VARIABLES and private_key or '',
                peer_endpoint=config.SAVE_WIREGUARD_VARIABLES and register_data['config']['peers'][0]['endpoint']['host'] or '',
                peer_public_key=config.SAVE_WIREGUARD_VARIABLES and register_data['config']['peers'][0]['public_key'] or '',
                interface_addresses=config.SAVE_WIREGUARD_VARIABLES and (register_data['config']['interface']['addresses']['v4'] + '/32, ' + register_data['config']['interface']['addresses']['v6'] + '/128') or '',
            )

            logger.success(output)

            with open(config.OUTPUT_FILE, 'a') as file:
                file.write(output + '\n')

        if signal_handler.KEEP_PROCESSING and config.DELAY > 0:
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
