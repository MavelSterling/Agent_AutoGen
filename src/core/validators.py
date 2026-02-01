from __future__ import annotations

from typing import Iterable

from src.core.schemas import SolutionProposal


def ensure_no_gateway(text: str) -> None:
    if "gateway" in text.lower():
        raise ValueError("La salida contiene la palabra prohibida 'gateway'.")


def ensure_no_gateway_in_lines(lines: Iterable[str]) -> None:
    for line in lines:
        ensure_no_gateway(line)


def ensure_no_gateway_in_proposal(proposal: SolutionProposal) -> None:
    ensure_no_gateway(proposal.diagram_mermaid)
    for component in proposal.components:
        ensure_no_gateway_in_lines(
            [
                component.name,
                component.purpose,
                *component.inputs,
                *component.outputs,
                *component.dependencies,
                *component.security_considerations,
            ]
        )
    for flow in proposal.flows:
        ensure_no_gateway_in_lines(
            [
                flow.name,
                *flow.steps,
                *flow.error_handling,
                *flow.timeouts,
                *flow.idempotency,
                *flow.fallback,
                *flow.happy_path,
            ]
        )
    for adr in proposal.adrs:
        ensure_no_gateway_in_lines(
            [adr.id, adr.title, adr.context, *adr.options, adr.decision, *adr.consequences]
        )
    for item in proposal.backlog:
        ensure_no_gateway_in_lines(
            [
                item.id,
                item.epic,
                item.story,
                item.priority,
                *item.acceptance_criteria,
                *item.definition_of_done,
            ]
        )
    for risk in proposal.risks:
        ensure_no_gateway_in_lines(
            [risk.id, risk.description, risk.impact, risk.mitigation, *risk.assumptions]
        )
    ensure_no_gateway_in_lines(
        [
            proposal.cost_estimate.range_low,
            proposal.cost_estimate.range_mid,
            proposal.cost_estimate.range_high,
            *proposal.cost_estimate.drivers,
            *proposal.cost_estimate.volume_assumptions,
        ]
    )
