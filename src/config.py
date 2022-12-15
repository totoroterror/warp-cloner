from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    BASE_KEYS: str = Field(
        env="BASE_KEYS",
        default=','.join([
            '0uPt219x-58dCy16I-50hnp1R2',
            'Rq781e4K-Jo0732qI-m0hD9r25',
            'er5D2y30-1dG205le-5RN86AX7',
            'M8zEo256-1Cw546av-QO0i371l',
            '5QyI96g4-DLe7941P-1If49k5B',
            '905URj6x-2I47b0cy-vDp2A839'
        ])
    )
    THREADS_COUNT: int = Field(env="THREADS_COUNT", default=1)
    PROXY_URL: str | None = Field(env="PROXY_URL")
    DELAY: int = Field(env="DELAY", default=25)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Settings()
