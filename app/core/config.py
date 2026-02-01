from pydantic_settings import BaseSettings  

class Settings(BaseSettings):
    project_name: str = "ems"
    database_url: str = ""
    secret_key : str = ""
    access_token_expire_minutes: int = 60
    algorithm: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()
