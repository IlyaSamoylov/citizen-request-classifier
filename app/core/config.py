from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl

class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file=".env", env_prefix="")

	APP_NAME: str = "request-classifier"
	APP_ENV: str = "local"

	APP_HOST: str = "0.0.0.0"
	APP_PORT: int = 8000
	LOG_LEVEL: str = "INFO"
	APP_DEBUG: bool = True

	DB_USER: str
	DB_PASSWORD: str
	DB_HOST: str = "db"
	DB_PORT: int = 5432
	DB_NAME: str = "app_db"

	CATEGORIES_FILE: str = "app/core/categories.yaml"

	OPENROUTER_API_KEY: str
	OPENROUTER_BASE_URL: AnyUrl = "https://openrouter.ai/api/v1"
	OPENROUTER_MODEL: str = "openrouter/free"
	OPENROUTER_SITE_URL: AnyUrl = "https://example.com"
	OPENROUTER_APP_NAME: str = "request-classifier"

	LLM_TIMEOUT_SECONDS: int = 30
	LLM_MAX_RETRIES: int = 2

	@property
	def db_url(self) -> str:
		return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
		        f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")


settings = Settings()