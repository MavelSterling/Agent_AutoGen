# Documentacion

En esta carpeta va la **explicacion de cada proceso** que hace el agente y la referencia a los entregables.

## Explicacion de procesos del agente

- **[procesos-del-agente.md](procesos-del-agente.md)** — Describe paso a paso: inicio y trazabilidad, carga de config, carga de requerimientos, construccion del cliente LLM, generacion de la propuesta (determinista o LLM), validacion "sin gateway", y escritura de la salida (architecture, ADR, backlog, riesgo, costos con scraping y costos por recurso).

## Donde se escriben los entregables

Los archivos generados por el agente se escriben en `data/`:

- `data/architecture/solution-proposal.md` — Propuesta principal.
- `data/adr/` — ADRs.
- `data/backlog/backlog.csv` — Backlog tecnico.
- `data/cost/cost-estimate.xlsx` — Estimacion de costos (Excel; precios por scraping y costos por recurso).
- `data/risk/risk-register.md` — Registro de riesgos.
