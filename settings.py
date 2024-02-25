#get the setting from env
import os
from dotenv import load_dotenv
from typing import List, Dict
load_dotenv()
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    LIB_MAGIC_VALIDATION: bool
    CONTEST_SUPPORTED_LANGUAGES: Dict[str, str]
    KAFKA_SERVER: str
    KAFKA_PORT: int
    KAFKA_USERNAME: str
    KAFKA_PASSWORD: str
    KAFKA_TOPIC: str
    KAFKA_GROUP_ID: str
        

def get_settings():
    return Settings(_env_file=".env")
