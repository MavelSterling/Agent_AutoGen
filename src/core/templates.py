from __future__ import annotations

from typing import List

import csv
import io

from src.core.schemas import ADR, BacklogItem, CostEstimate, Flow, Risk, SolutionProposal


def proposal_to_markdown(proposal: SolutionProposal) -> str:
    parts: List[str] = []
    parts.append("# Propuesta de arquitectura\n")
    parts.append("## 1) Diagrama logico (Mermaid)\n")
    parts.append("```mermaid\n")
    parts.append(proposal.diagram_mermaid.strip())
    parts.append("\n```\n")

    parts.append("## 2) Componentes y responsabilidades\n")
    for component in proposal.components:
        parts.append(f"### {component.name}\n")
        parts.append(f"- Proposito: {component.purpose}\n")
        parts.append(f"- Entradas: {', '.join(component.inputs)}\n")
        parts.append(f"- Salidas: {', '.join(component.outputs)}\n")
        parts.append(f"- Dependencias: {', '.join(component.dependencies)}\n")
        parts.append(
            f"- Seguridad: {', '.join(component.security_considerations)}\n"
        )

    parts.append("## 3) Flujos end-to-end\n")
    for flow in proposal.flows:
        parts.append(f"### {flow.name}\n")
        parts.append(f"- Pasos: {', '.join(flow.steps)}\n")
        parts.append(f"- Errores: {', '.join(flow.error_handling)}\n")
        parts.append(f"- Timeouts: {', '.join(flow.timeouts)}\n")
        parts.append(f"- Idempotencia: {', '.join(flow.idempotency)}\n")
        parts.append(f"- Fallback: {', '.join(flow.fallback)}\n")
        parts.append(f"- Happy path: {', '.join(flow.happy_path)}\n")

    parts.append("## 4) ADRs\n")
    for adr in proposal.adrs:
        parts.append(f"### {adr.id} - {adr.title}\n")
        parts.append(f"- Contexto: {adr.context}\n")
        parts.append(f"- Opciones: {', '.join(adr.options)}\n")
        parts.append(f"- Decision: {adr.decision}\n")
        parts.append(f"- Consecuencias: {', '.join(adr.consequences)}\n")

    parts.append("## 5) Backlog tecnico\n")
    for item in proposal.backlog:
        parts.append(f"### {item.id} - {item.epic}\n")
        parts.append(f"- Historia: {item.story}\n")
        parts.append(f"- Prioridad: {item.priority}\n")
        parts.append(
            f"- Criterios de aceptacion: {', '.join(item.acceptance_criteria)}\n"
        )
        parts.append(
            f"- Definition of done: {', '.join(item.definition_of_done)}\n"
        )

    parts.append("## 6) Riesgos, mitigaciones y supuestos\n")
    for risk in proposal.risks:
        parts.append(f"### {risk.id}\n")
        parts.append(f"- Riesgo: {risk.description}\n")
        parts.append(f"- Impacto: {risk.impact}\n")
        parts.append(f"- Mitigacion: {risk.mitigation}\n")
        parts.append(f"- Supuestos: {', '.join(risk.assumptions)}\n")

    parts.append("## 7) Estimacion de costos\n")
    parts.append(cost_estimate_to_markdown(proposal.cost_estimate, include_heading=False))

    return "\n".join(parts).strip() + "\n"


def adr_to_markdown(adr: ADR) -> str:
    return "\n".join(
        [
            f"# {adr.id} - {adr.title}",
            "",
            f"## Contexto\n{adr.context}",
            "",
            f"## Opciones\n- " + "\n- ".join(adr.options),
            "",
            f"## Decision\n{adr.decision}",
            "",
            f"## Consecuencias\n- " + "\n- ".join(adr.consequences),
            "",
        ]
    )


def backlog_to_markdown(items: List[BacklogItem]) -> str:
    lines: List[str] = ["# Backlog tecnico", ""]
    for item in items:
        lines.append(f"## {item.id} - {item.epic}")
        lines.append(f"- Historia: {item.story}")
        lines.append(f"- Prioridad: {item.priority}")
        lines.append("- Criterios de aceptacion:")
        lines.extend([f"  - {criterion}" for criterion in item.acceptance_criteria])
        lines.append("- Definition of done:")
        lines.extend([f"  - {done}" for done in item.definition_of_done])
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def backlog_to_csv(items: List[BacklogItem]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "id",
            "epic",
            "story",
            "priority",
            "acceptance_criteria",
            "definition_of_done",
        ]
    )
    for item in items:
        writer.writerow(
            [
                item.id,
                item.epic,
                item.story,
                item.priority,
                " | ".join(item.acceptance_criteria),
                " | ".join(item.definition_of_done),
            ]
        )
    return output.getvalue()

def risks_to_markdown(risks: List[Risk]) -> str:
    lines: List[str] = ["# Registro de riesgos", ""]
    for risk in risks:
        lines.append(f"## {risk.id}")
        lines.append(f"- Riesgo: {risk.description}")
        lines.append(f"- Impacto: {risk.impact}")
        lines.append(f"- Mitigacion: {risk.mitigation}")
        lines.append("- Supuestos:")
        lines.extend([f"  - {assumption}" for assumption in risk.assumptions])
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def cost_estimate_to_markdown(cost: CostEstimate, include_heading: bool = True) -> str:
    lines: List[str] = []
    if include_heading:
        lines.extend(["# Estimacion de costos", ""])
    lines.extend(
        [
            f"- Rango bajo: {cost.range_low}",
            f"- Rango medio: {cost.range_mid}",
            f"- Rango alto: {cost.range_high}",
            f"- Drivers: {', '.join(cost.drivers)}",
            f"- Supuestos de volumen: {', '.join(cost.volume_assumptions)}",
            "",
        ]
    )
    return "\n".join(lines)
