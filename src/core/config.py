from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, EmailStr, Field, PostgresDsn
from pathlib import Path
from typing import Annotated

class Settings(BaseSettings):
    database_url: PostgresDsn
    app_name: str = "Default Application Name"
    model_config = SettingsConfigDict(env_file=".env")

    #Path Objects
    upload_directory:Path = Path('uploads')
    
    admin_email: EmailStr = "admin@example.com"

    api_key: SecretStr = "test"

    port: Annotated[int, Field(ge=1, le=65535)] = 8000


settings = Settings()