from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

class Settings(BaseSettings):
    model_config =  SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    BASE_KEYS: list[str] = Field(
        validation_alias='BASE_KEYS',
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
    THREADS_COUNT: int = Field(validation_alias='THREADS_COUNT', default=1)
    PROXY_FILE: str | None = Field(validation_alias='PROXY_FILE', default=None)
    DEVICE_MODELS: list[str] = Field(validation_alias='DEVICE_MODELS', default=[])
    SAVE_WIREGUARD_VARIABLES: bool = Field(validation_alias='SAVE_WIREGUARD_VARIABLES', default=False)
    DELAY: int = Field(validation_alias='DELAY', default=25)
    OUTPUT_FILE: str = Field(validation_alias='OUTPUT_FILE', default='output.txt')
    OUTPUT_FORMAT: str = Field(validation_alias='OUTPUT_FORMAT', default='{key} | {referral_count}')
    RETRY_COUNT: int = Field(validation_alias='RETRY_COUNT', default=3)


config = Settings()
