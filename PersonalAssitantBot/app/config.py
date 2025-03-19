from pydantic_settings import SettingsConfigDict,BaseSettings


class Settings(BaseSettings):
    PG_CONNECTION: str
    PG1_CONNECTION:str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int
    PG_COLLECTION_NAME : str
    CHAT_COLLECTION_NAME : str = "chat_vectors"
    CHAT_HISTORY_TABLE_NAME :str = "chat_history"
    model_config : SettingsConfigDict = SettingsConfigDict(env_file='.env',extra="ignore")

Config = Settings()
