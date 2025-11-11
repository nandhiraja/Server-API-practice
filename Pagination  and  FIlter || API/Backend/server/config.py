from  pydantic_settings import BaseSettings , SettingsConfigDict


class Setting(BaseSettings):
    SQL_ROOT_NAME :str
    SQL_PASSWORD :str


setting = Setting()