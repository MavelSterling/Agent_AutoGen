from __future__ import annotations

import os

from src.core.config import LLMConfig


def build_model_client(config: LLMConfig) -> object | None:
    if not config.enabled:
        return None

    provider = config.provider.lower()
    if provider == "openai":
        from autogen_ext.models.openai import OpenAIChatCompletionClient

        api_key = os.getenv(config.api_key_env)
        if not api_key:
            raise ValueError(
                f"Falta la variable de entorno {config.api_key_env} para OpenAI."
            )
        kwargs = {"model": config.model, "api_key": api_key}
        if config.api_base:
            kwargs["base_url"] = config.api_base
        return OpenAIChatCompletionClient(**kwargs)

    if provider == "azure":
        from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

        azure = config.azure
        api_key = os.getenv(azure.api_key_env)
        if not api_key:
            raise ValueError(
                f"Falta la variable de entorno {azure.api_key_env} para Azure OpenAI."
            )
        if not azure.endpoint or not azure.deployment_name:
            raise ValueError(
                "Configura azure.endpoint y azure.deployment_name en config.yml."
            )
        return AzureOpenAIChatCompletionClient(
            api_key=api_key,
            azure_endpoint=azure.endpoint,
            azure_deployment=azure.deployment_name,
            api_version=azure.api_version,
        )

    raise ValueError(f"Proveedor LLM no soportado: {config.provider}")
