import pathlib
import pydantic
import decouple

ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.parent.parent.parent.resolve()


class BackendBaseSettings(pydantic.BaseSettings):
    # General
    SERVER_HOST: str = decouple.config("BACKEND_SERVER_HOST", cast=str)
    SERVER_PORT: int = decouple.config("BACKEND_SERVER_PORT", cast=int)
    SERVER_WORKERS: int = decouple.config("BACKEND_SERVER_WORKERS", cast=int)
    DEBUG: bool = decouple.config("BACKEND_DEBUG", cast=bool)
    LOGGING_LEVEL: str = decouple.config("BACKEND_LOGGING_LEVEL", cast=str)

    # Middleware
    CORS_HOSTS: str = decouple.config("BACKEND_HOST", default="", cast=str)
    CORS_ORIGINS: list[str] = decouple.config("BACKEND_CORS_ALLOW_ORIGIN", default="", cast=str).split(",")
    CORS_CREDENTIALS: bool = decouple.config("BACKEND_CORS_CREDENTIALS", cast=bool)
    CORS_METHODS: list[str] = decouple.config("BACKEND_CORS_METHODS", default="", cast=str).split(",")
    CORS_HEADERS: list[str] = decouple.config("BACKEND_CORS_HEADERS", default="", cast=str).split(",")
    CORS_MAXAGE: int = decouple.config("BACKEND_CORS_MAXAGE", cast=int)

    # Line
    LINE_CHANNEL_ACCESS_TOKEN: str = decouple.config("LINE_CHANNEL_ACCESS_TOKEN", cast=str)
    LINEBOT_CHANNEL_SECRET: str = decouple.config("LINEBOT_CHANNEL_SECRET", cast=str)

    # OPEN AI
    OPENAI_API_KEY: str = decouple.config("OPEN_AI_API_KEY", cast=str)

    class Config:
        env_file = ROOT_DIR / ".env"
        env_file_encoding = "utf-8"


settings = BackendBaseSettings()
