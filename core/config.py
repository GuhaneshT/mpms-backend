from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Machine Management PMS"
    API_V1_STR: str = "/api/v1"

    # Supabase Configuration
    SUPABASE_URL: str = "https://example.supabase.co"
    SUPABASE_KEY: str = "your-anon-key"
    SUPABASE_JWT_SECRET: str = "your-jwt-secret"

    # Application URLs
    BACKEND_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore")


settings = Settings()
