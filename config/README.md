# Configuracion

Este directorio contiene configuracion externa del proyecto. No se deben
almacenar secretos en el repositorio. Use variables de entorno o identidades
administradas para credenciales.

## Archivo base
- `config/config.yml` contiene parametros no sensibles para entorno local.

## Que NO va en config
- claves API, tokens, passwords
- cadenas de conexion completas

## Variables recomendadas
- `cost.scrape_provider`: `azure` | `aws` | `gcp` | vacio (para precios en Excel por scraping).
- `app.name`, `app.environment`, `app.log_level`
- `llm.enabled`, `llm.provider`, `llm.model`, `llm.api_key_env`, `llm.api_base`
- `llm.azure.endpoint`, `llm.azure.deployment_name`, `llm.azure.api_version`, `llm.azure.api_key_env`
- `paths.output_dir`
- `execution.timeouts_seconds`, `execution.retries`, `execution.max_concurrency`
- `features.enable_observability`
- `observability.metrics_endpoint`, `observability.tracing_sampling`
- `storage.backend`, `storage.bucket_name`
- `vector_index.provider`, `vector_index.top_k`
