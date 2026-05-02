from pydantic_settings import BaseSettings, SettingsConfigDict
from openai import OpenAI


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    llm_tier: str = "flash"

    # DeepSeek
    deepseek_api_key: str = ""
    deepseek_model: str = "deepseek-v4-flash"
    deepseek_model_pro: str = "deepseek-v4-pro"
    deepseek_base_url: str = "https://api.deepseek.com/v1"

    # Kimi
    kimi_api_key: str = ""
    kimi_model: str = "kimi-k2.5"
    kimi_model_pro: str = "kimi-k2.6"
    kimi_base_url: str = "https://api.moonshot.ai/v1"


settings = Settings()


def get_model_config(tier: str = None):
    """Devuelve (client, model_name) según el tier."""
    tier = tier or settings.llm_tier

    if tier == "flash":
        return OpenAI(api_key=settings.deepseek_api_key, base_url=settings.deepseek_base_url), settings.deepseek_model
    elif tier == "pro":
        return OpenAI(api_key=settings.deepseek_api_key, base_url=settings.deepseek_base_url), settings.deepseek_model_pro
    elif tier == "backup":
        return OpenAI(api_key=settings.kimi_api_key, base_url=settings.kimi_base_url), settings.kimi_model
    elif tier == "backup_pro":
        return OpenAI(api_key=settings.kimi_api_key, base_url=settings.kimi_base_url), settings.kimi_model_pro
    else:
        raise ValueError(f"Tier desconocido: {tier}")