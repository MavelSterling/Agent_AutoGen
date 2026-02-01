from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.core.generator import generate_solution
from src.core.schemas import Requirements


def test_solution_has_required_sections() -> None:
    proposal = generate_solution(Requirements())
    assert proposal.diagram_mermaid
    assert proposal.components
    assert proposal.flows
    assert proposal.adrs
    assert proposal.backlog
    assert proposal.risks
    assert proposal.cost_estimate


def test_mermaid_diagram_format() -> None:
    proposal = generate_solution(Requirements())
    assert proposal.diagram_mermaid.startswith("flowchart")
