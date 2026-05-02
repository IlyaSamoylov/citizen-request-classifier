from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
	"""Класс для чтения конфигурации"""
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

	CLASSIFIER_MODEL_PATH: str ="./artifacts/classifier.pkl"
	CLASSIFIER_THRESHOLD: float = 0.60
	CLASSIFIER_MARGIN_THRESHOLD: float = 0.15

	LLM_PROVIDER: str = "local"
	LLM_MODEL_NAME: str = "saiga-or-vikhr"
	LLM_TIMEOUT_SECONDS: int = 30
	LLM_MAX_RETRIES: int = 2

	@property
	def db_url(self) -> str:
		return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
		        f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")


settings = Settings()