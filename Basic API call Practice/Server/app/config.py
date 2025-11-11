from  pydantic_settings  import BaseSettings,SettingsConfigDict
import os

ROOT_BASE_URL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV_PATH = os.path.join(ROOT_BASE_URL,'.env')



class Settings(BaseSettings):

    GROQ_API_KEY :str
    SERVER_PORT : int
    SERVER_HOST_URL :str


    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        extra='ignore'
    )



settings = Settings()

