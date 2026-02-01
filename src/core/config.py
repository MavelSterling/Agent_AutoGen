from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field


class AzureLLMConfig(BaseModel):
    endpoint: str = ""
    deployment_name: str = ""
    api_version: str = "2024-02-01"
    api_key_env: str = "AZURE_OPENAI_API_KEY"


class LLMConfig(BaseModel):
    enabled: bool = False
    provider: str = "openai"
    model: str = "gpt-4o-mini"
    api_key_env: str = "OPENAI_API_KEY"
    api_base: str = ""
    azure: AzureLLMConfig = Field(default_factory=AzureLLMConfig)


class CostConfig(BaseModel):
    scrape_provider: str = ""


class PathsConfig(BaseModel):
    output_dir: str = "./docs"


class FeaturesConfig(BaseModel):
    enable_observability: bool = True


class AppConfig(BaseModel):
    llm: LLMConfig = Field(default_factory=LLMConfig)
    cost: CostConfig = Field(default_factory=CostConfig)
    paths: PathsConfig = Field(default_factory=PathsConfig)
    features: FeaturesConfig = Field(default_factory=FeaturesConfig)

    class Config:
        extra = "allow"


def load_config(path: str = "config/config.yml") -> AppConfig:
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(
            f"No se encontro el archivo de configuracion: {config_path}"
        )
    payload = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    return AppConfig(**payload)
