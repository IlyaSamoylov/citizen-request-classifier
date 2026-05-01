from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
	"""Класс для чтения конфигурации"""
	model_config = SettingsConfigDict(env_file=".env", env_prefix="")

	APP_NAME: str = "request-classifier"
	APP_ENV: str = "local"
	APP_HOST: str = "0.0.0.0"
	APP_PORT: str = "8000"
	LOG_LEVEL: str = "INFO"

	CLASSIFIER_MODEL_PATH: str ="./artifacts/classifier.pkl"
	CLASSIFIER_THRESHOLD: float = 0.60
	CLASSIFIER_MARGIN_THRESHOLD: float = 0.15

	LLM_PROVIDER: str = "local"
	LLM_MODEL_NAME: str = "saiga-or-vikhr"
	LLM_TIMEOUT_SECONDS: int = 30
	LLM_MAX_RETRIES: int = 2

	# TODO: собирать и возвращать url подключения к базе здесь через @property или использовать sqlalchemy.engine import URL?

settings = Settings()