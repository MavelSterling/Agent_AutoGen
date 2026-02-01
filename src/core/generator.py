from __future__ import annotations

from typing import List

from src.core.schemas import (
    ADR,
    BacklogItem,
    Component,
    CostEstimate,
    Flow,
    Requirements,
    Risk,
    SolutionProposal,
)


def generate_solution(requirements: Requirements) -> SolutionProposal:
    diagram_mermaid = _build_mermaid(requirements)
    components = _build_components(requirements)
    flows = _build_flows(requirements)
    adrs = _build_adrs(requirements)
    backlog = _build_backlog(requirements)
    risks = _build_risks(requirements)
    cost_estimate = _build_cost_estimate(requirements)

    return SolutionProposal(
        diagram_mermaid=diagram_mermaid,
        components=components,
        flows=flows,
        adrs=adrs,
        backlog=backlog,
        risks=risks,
        cost_estimate=cost_estimate,
    )


def _build_mermaid(requirements: Requirements) -> str:
    return "\n".join(
        [
            "flowchart LR",
            "    client[Client Apps]",
            "    auth[AuthN/AuthZ - JWT/OAuth2]",
            "    api[API Runtime]",
            "    orchestrator[Agent Orchestrator]",
            "    storage[Object Storage]",
            "    metadata[Metadata DB]",
            "    vector[Vector Index]",
            "    obs[Observability]",
            "",
            "    client --> auth --> api --> orchestrator",
            "    orchestrator --> storage",
            "    orchestrator --> metadata",
            "    orchestrator --> vector",
            "    api --> obs",
            "    orchestrator --> obs",
        ]
    )


def _build_components(requirements: Requirements) -> List[Component]:
    return [
        Component(
            name="Client Apps",
            purpose="Canal de entrada para solicitudes de arquitectura.",
            inputs=["Requerimientos funcionales y no funcionales"],
            outputs=["Solicitud validada"],
            dependencies=["API Runtime"],
            security_considerations=["TLS", "Token JWT"],
        ),
        Component(
            name="AuthN/AuthZ",
            purpose="Validar identidad y permisos en la capa API.",
            inputs=["Credenciales", "Tokens"],
            outputs=["Token firmado", "Claims"],
            dependencies=["API Runtime"],
            security_considerations=["Rotacion de llaves", "Auditoria"],
        ),
        Component(
            name="API Runtime",
            purpose="Exponer endpoints y orquestar el agente.",
            inputs=["Solicitud autenticada"],
            outputs=["Respuesta estructurada"],
            dependencies=["Agent Orchestrator", "Observability"],
            security_considerations=["Rate limit en aplicacion", "Validacion"],
        ),
        Component(
            name="Agent Orchestrator",
            purpose="Construir propuesta de arquitectura con entregables.",
            inputs=["Requerimientos normalizados"],
            outputs=["Propuesta completa"],
            dependencies=["Object Storage", "Metadata DB", "Vector Index"],
            security_considerations=["No exponer secretos", "Trazabilidad"],
        ),
        Component(
            name="Object Storage",
            purpose="Guardar documentos y artefactos.",
            inputs=["Archivos y plantillas"],
            outputs=["Versiones de documentos"],
            dependencies=[],
            security_considerations=["Cifrado en reposo", "RBAC"],
        ),
        Component(
            name="Metadata DB",
            purpose="Guardar metadatos y estados de ejecucion.",
            inputs=["Metadatos"],
            outputs=["Consultas", "Estados"],
            dependencies=[],
            security_considerations=["RBAC", "Backups"],
        ),
        Component(
            name="Vector Index",
            purpose="Indexar contexto para recuperacion semantica.",
            inputs=["Embeddings"],
            outputs=["Resultados de retrieval"],
            dependencies=[],
            security_considerations=["Scope por tenant", "TTL"],
        ),
        Component(
            name="Observability",
            purpose="Logs, metricas y trazas del flujo.",
            inputs=["Eventos", "Metricas"],
            outputs=["Dashboards", "Alertas"],
            dependencies=[],
            security_considerations=["No PII", "Redaccion"],
        ),
    ]


def _build_flows(requirements: Requirements) -> List[Flow]:
    return [
        Flow(
            name="Ingesta y generacion",
            steps=[
                "Ingreso de requerimientos",
                "Validacion y normalizacion",
                "Orquestacion del agente",
                "Generacion de entregables",
                "Persistencia y respuesta",
                "Observabilidad",
            ],
            error_handling=[
                "Reintento con backoff",
                "Errores validacion 4xx",
                "Errores internos 5xx",
            ],
            timeouts=["Timeout por etapa", "Cancelacion segura"],
            idempotency=["Idempotency key por solicitud"],
            fallback=["Respuesta parcial con advertencias"],
            happy_path=["Respuesta completa con 7 entregables"],
        )
    ]


def _build_adrs(requirements: Requirements) -> List[ADR]:
    return [
        ADR(
            id="ADR-0001",
            title="Arquitectura sin servicio de entrada gestionado",
            context="El alcance prohibe componentes de entrada API gestionados.",
            options=["Servicio gestionado de entrada API", "Control en runtime", "Reverse proxy"],
            decision="Usar controles en la capa de aplicacion y red.",
            consequences=[
                "La API implementa autenticacion, autorizacion y rate limit.",
                "Se debe observar trafico directamente en runtime.",
            ],
        )
    ]


def _build_backlog(requirements: Requirements) -> List[BacklogItem]:
    return [
        BacklogItem(
            id="BL-001",
            epic="Implementacion del agente",
            story="Crear generador de entregables y validaciones sin servicio gestionado de entrada.",
            priority="P0",
            acceptance_criteria=[
                "Genera 7 entregables requeridos",
                "Cumple restricciones de componentes",
            ],
            definition_of_done=[
                "Tests unitarios verdes",
                "Documentacion actualizada",
            ],
        ),
        BacklogItem(
            id="BL-002",
            epic="Observabilidad",
            story="Agregar logs y metricas por etapa.",
            priority="P1",
            acceptance_criteria=["Incluye request_id y tiempos por etapa"],
            definition_of_done=["Metricas en monitoring", "Trazas activas"],
        ),
    ]


def _build_risks(requirements: Requirements) -> List[Risk]:
    return [
        Risk(
            id="R-001",
            description="Sobrecosto por uso de LLM y almacenamiento.",
            impact="Alto",
            mitigation="Limites de cuota y cache de resultados.",
            assumptions=["Volumen mensual moderado", "Cache reutilizable"],
        ),
        Risk(
            id="R-002",
            description="Calidad variable en entregables.",
            impact="Medio",
            mitigation="Validaciones y revisiones automatizadas.",
            assumptions=["Plantillas estables", "Requerimientos claros"],
        ),
    ]


def _build_cost_estimate(requirements: Requirements) -> CostEstimate:
    return CostEstimate(
        range_low="USD 300",
        range_mid="USD 1500",
        range_high="USD 5000",
        drivers=["Tokens LLM", "Storage", "Compute", "Traffic"],
        volume_assumptions=[
            "100-500 solicitudes/mes",
            "Documentos medianos",
            "Retencion 30 dias",
        ],
    )
