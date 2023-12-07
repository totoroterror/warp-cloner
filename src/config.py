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
            'W32Zg5F7-V92mt68f-1dep203B',
            'ka3E672R-1574KThz-nM40Jh15',
            'L4or30z8-MA6w1y30-r0GP8f52',
            '1r2JN79T-b1vm364s-B79N3g4l',
            '9Z84YMf1-Ci731e5K-743NlOZ0',
            'X3ZY91n5-S0at385w-170NF2ge',
            'd9vT20K5-RL6I08W1-0X1zM48S',
            '3fwe4E78-4ua83qA7-kP061T4t',
            'm1Jdh478-1h63O5fo-1i8QR07U',
            '5hD6f0W8-Xz08g43W-w43F1Ug2',
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
