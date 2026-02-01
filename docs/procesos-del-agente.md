# Procesos del agente "Arquitecto de Solución"

Este documento describe cada proceso que ejecuta el agente cuando se invoca con `python -m src.main`.

---

## 1. Inicio y trazabilidad

- Se genera un **trace_id** (identificador único de la ejecución) para correlacionar todos los logs.
- Se registra el inicio con los parámetros de entrada: ruta del archivo de requerimientos (`--input`) y ruta del archivo de configuración (`--config`).
- **Código:** `src/main.py` → `new_trace_id()`, `get_logger(..., request_id=trace_id)`.

---

## 2. Carga de configuración

- Se lee el archivo YAML de configuración (por defecto `config/config.yml`).
- Se obtienen: habilitación del LLM, proveedor y modelo, directorio de salida, proveedor de scraping de costos, etc.
- Si el archivo no existe, se lanza un error.
- **Código:** `src/main.py` → `load_config(args.config)`; `src/core/config.py` → `load_config()`.

---

## 3. Carga de requerimientos

- Se lee el archivo JSON de entrada (por defecto `data/requirements.json`).
- Se parsea y se valida contra el esquema `Requirements`: nombre del proyecto, dominio, proveedor de nube, requerimientos funcionales y no funcionales, restricciones, fuentes de datos, **recursos**, perfil de tráfico, regiones, cumplimiento, supuestos.
- Si el archivo no existe o el JSON es inválido, se lanza un error.
- **Código:** `src/main.py` → `_load_requirements(args.input)`; `src/core/schemas.py` → `Requirements`.

---

## 4. Construcción del cliente de modelo (LLM)

- Si en la configuración `llm.enabled` es `true`, se construye un cliente para el proveedor indicado (OpenAI o Azure) usando variables de entorno para las claves.
- Si `llm.enabled` es `false`, no se usa ningún cliente y el agente trabajará en modo determinista.
- **Código:** `src/main.py` → `build_model_client(config.llm)`; `src/core/llm.py` → `build_model_client()`.

---

## 5. Creación del agente y generación de la propuesta

- Se instancia `SolutionArchitectAgent` con la opción de usar LLM y el cliente de modelo (si aplica).
- Se llama a `agent.propose(requirements)`:
  - **Modo determinista:** se usa el generador interno (`generate_solution`) para producir la propuesta a partir de los requerimientos, sin llamar a ningún LLM.
  - **Modo LLM:** se construye un prompt con los requerimientos, se llama al modelo y se parsea la respuesta JSON para obtener la propuesta.
- Se valida que la propuesta **no contenga la palabra "gateway"** en ninguno de los entregables (diagrama, componentes, flujos, ADRs, backlog, riesgos, costos). Si aparece, se lanza un error.
- **Código:** `src/main.py` → `SolutionArchitectAgent`, `agent.propose()`; `src/agent/solution_architect_agent.py`; `src/core/generator.py`; `src/core/validators.py`.

---

## 6. Escritura de la documentación (salida)

La salida se escribe en el directorio configurado (por defecto `data/`). Cada paso crea o actualiza archivos.

### 6.1 Directorios

- Se crean (si no existen) las carpetas: `architecture`, `adr`, `backlog`, `risk`, `cost` dentro del directorio de salida.
- **Código:** `src/agent/tools.py` → `write_docs()` al inicio.

### 6.2 Propuesta de arquitectura

- Se genera el markdown de la propuesta completa (diagrama Mermaid, componentes, flujos, ADRs, backlog, riesgos, estimación de costos) y se escribe en `architecture/solution-proposal.md`.
- **Código:** `src/agent/tools.py` → `proposal_to_markdown()`; `src/core/templates.py`.

### 6.3 ADRs

- Por cada ADR de la propuesta se escribe un archivo en `adr/` con el formato `{id}-{titulo-slug}.md`.
- **Código:** `src/agent/tools.py` → `adr_to_markdown()`; `src/core/templates.py`.

### 6.4 Backlog técnico

- Se exporta el backlog de la propuesta a CSV y se escribe en `backlog/backlog.csv`.
- **Código:** `src/agent/tools.py` → `backlog_to_csv()`; `src/core/templates.py`.

### 6.5 Registro de riesgos

- Se genera el markdown del registro de riesgos y se escribe en `risk/risk-register.md`.
- **Código:** `src/agent/tools.py` → `risks_to_markdown()`; `src/core/templates.py`.

### 6.6 Estimación de costos (Excel)

- Se escribe un archivo Excel en `cost/cost-estimate.xlsx` con:
  - **Hoja "Estimacion":** rangos (bajo/medio/alto), drivers y supuestos de volumen.
  - **Hoja "Precios_nube":** si está configurado un proveedor de nube (`cloud_provider` en el input o `cost.scrape_provider` en config), se obtienen precios por **web scraping** a las páginas oficiales de Azure, AWS o GCP; si el scraping falla o no devuelve datos, se usan precios de referencia (fallback).
  - **Hoja "Costos_por_recurso":** si en el input hay una lista de `resources`, se crea una fila por recurso y se asocia un precio estimado cuando hay coincidencia con los precios obtenidos (scraping o fallback).
- **Código:** `src/agent/tools.py` → `fetch_cloud_pricing()`, `get_fallback_pricing()`, `cost_estimate_to_excel()`; `src/core/scraping.py`; `src/core/cost_excel.py`.

---

## 7. Finalización

- Se registra en log que la salida fue generada en el directorio de salida.
- Todos los logs de la ejecución comparten el mismo `trace_id` para facilitar el seguimiento.

---

## Resumen del flujo

```
Inicio (trace_id)
  → Cargar config (config.yml)
  → Cargar requerimientos (requirements.json)
  → Construir cliente LLM (si llm.enabled)
  → Crear agente y generar propuesta (determinista o LLM)
  → Validar “sin gateway”
  → Escribir salida en data/ (architecture, adr, backlog, risk, cost)
      → Opcional: scraping de precios (Azure/AWS/GCP) y hoja Costos_por_recurso
  → Fin
```
