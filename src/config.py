from typing import Any
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    BASE_KEYS: list[str] = Field(
        env='BASE_KEYS',
        default=[
            '4QSK31f5-gf7624vG-AK5E2c60',
            '158yuMs0-aQ0H84j9-85zCub93',
            'gP9iX803-238whB9q-754fVDF1',
            '15dqy8U9-21dG9EN4-7oEP0w34',
            'T0F95f3C-0b86Ki3w-93ZVp84O',
            'kxF8C975-7v2wQY65-Fl1wJ538',
            'Nf3JI195-6Ef8yx39-oR74y0E6',
            'y03c6Ez1-689c3pYk-4x68Ro2t',
            '9k78h5WA-46S5cuv3-518OnxP4',
            'Tw36cx85-4Vq5GA08-GP835x1k',
        ]
    )
    THREADS_COUNT: int = Field(env='THREADS_COUNT', default=1)
    PROXY_FILE: str | None = Field(env='PROXY_FILE', default=None)
    DEVICE_MODELS: list[str] = Field(env='DEVICE_MODELS', default=[])
    SAVE_WIREGUARD_VARIABLES: bool = Field(env='SAVE_WIREGUARD_VARIABLES', default=False)
    DELAY: int = Field(env='DELAY', default=25)
    OUTPUT_FILE: str = Field(env='OUTPUT_FILE', default='output.txt')
    OUTPUT_FORMAT: str = Field(env='OUTPUT_FORMAT', default='{key} | {referral_count}')
    RETRY_COUNT: int = Field(env='RETRY_COUNT', default=3)

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
