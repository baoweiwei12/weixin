from pydantic import BaseModel
import yaml

class MYSQLSettings(BaseModel):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    DATABASE: str

class JWTSettings(BaseModel):
    SECRET_KEY: str
    ALGORITHM: str
    EXPIRE_MINUTES: int

class AppSettings(BaseModel):
    NAME: str
    VERSION: str
    DESCRIPTION: str

class AppConfig(BaseModel):
    APP: AppSettings
    MYSQL: MYSQLSettings
    JWT: JWTSettings

def _load_config_from_file(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return AppConfig(**config)

CONFIG = _load_config_from_file('config.yaml')


