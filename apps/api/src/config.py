from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str
    groq_api_key: str
    groq_model: str = "openai/gpt-oss-120b"
    supabase_url: str
    supabase_secret_key: str
    supabase_jwks_url: str
    registration_access_code: str


settings = Settings()