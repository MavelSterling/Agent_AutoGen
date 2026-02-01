from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.core.generator import generate_solution
from src.core.schemas import Requirements
from src.core.templates import proposal_to_markdown


def test_proposal_to_markdown() -> None:
    proposal = generate_solution(Requirements())
    content = proposal_to_markdown(proposal)
    assert "Diagrama logico" in content
    assert "Componentes" in content
    assert "ADRs" in content
