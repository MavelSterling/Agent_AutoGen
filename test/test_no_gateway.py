from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.core.generator import generate_solution
from src.core.schemas import Requirements
from src.core.validators import ensure_no_gateway_in_proposal


def test_no_gateway_in_outputs() -> None:
    requirements = Requirements(
        functional_requirements=["Generar propuesta"],
        non_functional_requirements=["Seguridad"],
        constraints=["Sin API Gateway"],
    )
    proposal = generate_solution(requirements)
    ensure_no_gateway_in_proposal(proposal)
