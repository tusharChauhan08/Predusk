from pydantic_settings import BaseSettings
from typing import List, ClassVar


class Settings(BaseSettings):
    PROJECT_NAME: str = "Book Api"
    API_V1_STR: str = "/api"

    # Database
    DATABASE_URL: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_HOST: str = ""
    DB_PORT: str = ""
    DB_NAME: str = ""
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]

    # System messages
    INTERNAL_SERVER_ERROR: ClassVar[str] = "Internal Server Error"
    USER_NOT_FOUND: ClassVar[str] = "User not found"
    NOT_AUTHORIZED: ClassVar[str] = "you are not authorized"

    # Cascading value
    CASCADE: ClassVar[str] = "all, delete-orphan"

    class Config:
        env_file = ".env"

settings = Settings()
