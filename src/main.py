import asyncio
import signal
import random

from base64 import b64decode
from typing import Optional, Tuple

from loguru import logger
from aiohttp import ClientResponse, ClientSession, ClientTimeout

from config import config
from warp import RegisterData, clone_key, GetInfoData

from utilities import key_dispatcher, proxy_dispatcher


class SignalHandler:
    KEEP_PROCESSING: bool = True
    def __init__(self) -> None:
        signal.signal(signalnum=signal.SIGINT, handler=self.exit_gracefully)
        signal.signal(signalnum=signal.SIGTERM, handler=self.exit_gracefully)

    def exit_gracefully(self, signum, frame) -> None:
        logger.info('Received signal {}, stopping all threads...'.format(signum))
        self.KEEP_PROCESSING = False


signal_handler = SignalHandler()


def client_id_to_reserved(client_id: str) -> list[int]:
    decoded = b64decode(client_id)
    hex_string = decoded.hex()
    decValues = []

    for i in range(0, len(hex_string), 2):
        hexByte = hex_string[i:i+2]
        dec_value = int(hexByte, 16)
        decValues.append("{:03d}{:03d}{:03d}".format(dec_value // 100, (dec_value // 10) % 10, dec_value % 10))

    reserved = []
    for i in range(0, len(hex_string), 2):
        hexByte = hex_string[i:i+2]
        dec_value = int(hexByte, 16)
        reserved.append(dec_value)

    return reserved


async def custom_clone_key(key_to_clone: str, retry_count: int = 0) -> Optional[Tuple[GetInfoData, RegisterData, Optional[str], str]]:
    if retry_count > config.RETRY_COUNT or not signal_handler.KEEP_PROCESSING:
        return None

    try:
        key, register_data, private_key, client_id = await clone_key(
            key=key_to_clone,
            proxy_url=proxy_dispatcher.get_proxy(),
            device_model=len(config.DEVICE_MODELS) > 0 and random.choice(config.DEVICE_MODELS) or None,
        )

        key_dispatcher.add_key(key['license'])

        return key, register_data, private_key, client_id
    except Exception as e:
        logger.error('{} (key: {}, retry count: {})'.format(
            e,
            key_to_clone,
            retry_count
        ))

        if config.DELAY > 0 and signal_handler.KEEP_PROCESSING:
            sleep_time = config.DELAY

            while sleep_time > 0 and signal_handler.KEEP_PROCESSING:
                await asyncio.sleep(delay=1)
                sleep_time -= 1

        return await custom_clone_key(key_to_clone=key_to_clone, retry_count=retry_count + 1)


async def worker(id: int) -> None:
    logger.debug('Worker {} started'.format(id))

    while signal_handler.KEEP_PROCESSING:
        response = await custom_clone_key(
            key_to_clone=key_dispatcher.get_key(),
        )

        if response != None:
            key, register_data, private_key, client_id = response

            data = {
                'key': key['license'],
                'referral_count': key['referral_count'],
                'private_key': config.SAVE_WIREGUARD_VARIABLES and private_key or '',
                'peer_endpoint': config.SAVE_WIREGUARD_VARIABLES and register_data['config']['peers'][0]['endpoint']['host'] or '',
                'peer_public_key': config.SAVE_WIREGUARD_VARIABLES and register_data['config']['peers'][0]['public_key'] or '',
                'interface_addresses': config.SAVE_WIREGUARD_VARIABLES and (register_data['config']['interface']['addresses']['v4'] + '/32, ' + register_data['config']['interface']['addresses']['v6'] + '/128') or '',
                'reserved': client_id_to_reserved(client_id=client_id)
            }

            if config.WEBHOOK_KEY_URL:
                try:
                    async with ClientSession() as session:
                        await session.post(config.WEBHOOK_KEY_URL, json=data)
                except Exception as e:
                    logger.error('failed to send webhook, {}'.format(e))

            output: str = config.OUTPUT_FORMAT.format(
                key=data['key'],
                referral_count=data['referral_count'],
                private_key=data['private_key'],
                peer_endpoint=data['peer_endpoint'],
                peer_public_key=data['peer_public_key'],
                interface_addresses=data['interface_addresses'],
                reserved=data['reserved']
            )

            logger.success(output)

            with open(config.OUTPUT_FILE, 'a') as file:
                file.write(output + '\n')

        if signal_handler.KEEP_PROCESSING and config.DELAY > 0:
            sleep_time = config.DELAY

            while sleep_time > 0 and signal_handler.KEEP_PROCESSING:
                await asyncio.sleep(delay=1)
                sleep_time -= 1


async def main() -> None:
    tasks = []

    for i in range(config.THREADS_COUNT):
        tasks.append(
            asyncio.create_task(worker(i + 1))
        )

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
