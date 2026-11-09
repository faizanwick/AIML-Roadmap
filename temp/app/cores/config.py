# from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    APP_NAME : str = "Task Manager"
    APP_VERSION : str = "2.0.0"
    DEBUG : bool = False

    # DATA_FILE : Path = BASE_DIR / "data" / "tasks.json"

    DATABASE_URL : str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()