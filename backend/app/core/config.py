from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+psycopg2://noc:noc_password@db:5432/noc_vision"

    # Security
    SECRET_KEY: str = "change-me-to-a-random-64-char-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    # Application
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # Plugins
    ENABLED_PLUGINS: str = ""

    # Default admin
    DEFAULT_ADMIN_USERNAME: str = "admin"
    DEFAULT_ADMIN_PASSWORD: str = "admin"
    DEFAULT_ADMIN_EMAIL: str = "admin@nocvision.local"

    # NetBox API Configuration
    NETBOX_URL: str = "http://10.100.22.11:8000/api"
    NETBOX_TOKEN: str = ""
    NETBOX_API_VERSION: str = "v2"

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
    }

    @classmethod
    def parse_env_var(cls, field_name: str, raw_val: str):
        if field_name == "ALLOWED_ORIGINS":
            return [origin.strip() for origin in raw_val.split(",")]
        return cls.json_loads(raw_val)


settings = Settings()
