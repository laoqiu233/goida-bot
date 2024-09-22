from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfiguredSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=[".env", ".env.secrets"], extra="allow")
