from pydantic_settings import BaseSettings

class Config(BaseSettings):
    app_name: str = "grantbot"
    debug: bool = False

config = Config()