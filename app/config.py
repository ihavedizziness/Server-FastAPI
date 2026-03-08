from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Stats Server"
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False

    # Stream chunk size for download tests
    chunk_size_bytes: int = 256 * 1024  # 256 KB

    # Safety caps
    max_download_mb: int = 1000
    max_upload_mb: int = 500

    # speedtest-cli parallelism
    speedtest_threads: int = 4

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
