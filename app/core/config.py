from pydantic_settings import BaseSettings
# Esta clase va a cargar automáticamente las variables de entorno de nuestro fichero .env


class Setting(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Setting()