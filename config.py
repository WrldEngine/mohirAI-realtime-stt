import os

from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()


@dataclass(frozen=True)
class Settings:
    API_KEY: str = os.getenv("API_KEY")
    API_URL: str = os.getenv("API_URL")
    LANGUAGE: str = os.getenv("LANGUAGE")


settings = Settings()
