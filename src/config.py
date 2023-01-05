from typing import Any
from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    BASE_KEYS: list[str] = Field(
        env='BASE_KEYS',
        default=[
            '0uPt219x-58dCy16I-50hnp1R2',
            'Rq781e4K-Jo0732qI-m0hD9r25',
            'er5D2y30-1dG205le-5RN86AX7',
            'M8zEo256-1Cw546av-QO0i371l',
            '5QyI96g4-DLe7941P-1If49k5B',
            '905URj6x-2I47b0cy-vDp2A839'
        ]
    )
    THREADS_COUNT: int = Field(env='THREADS_COUNT', default=1)
    PROXY_FILE: str | None = Field(env='PROXY_FILE', default=None)
    DEVICE_MODELS: list[str] = Field(env='DEVICE_MODELS', default=[])
    DELAY: int = Field(env='DELAY', default=25)
    OUTPUT_FILE: str = Field(env='OUTPUT_FILE', default='output.txt')
    OUTPUT_FORMAT: str = Field(env='OUTPUT_FORMAT', default='{key} | {referral_count}')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

        @classmethod
        def parse_env_var(cls, field: str, raw_val: str) -> Any:
            if field == 'BASE_KEYS' or field == 'DEVICE_MODELS':
                if isinstance(raw_val, str):
                    return str(raw_val).split(',')

            return cls.json_loads(raw_val) # type: ignore

config = Settings()
