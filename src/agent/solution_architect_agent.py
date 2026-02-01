from __future__ import annotations

import asyncio
import json
import re
from typing import Optional

from src.core.generator import generate_solution
from src.core.schemas import Requirements, SolutionProposal
from src.core.validators import ensure_no_gateway_in_proposal


class SolutionArchitectAgent:
    def __init__(
        self,
        enable_autogen: bool = False,
        model_client: Optional[object] = None,
    ) -> None:
        self._enable_autogen = enable_autogen
        self._model_client = model_client
        if self._enable_autogen and self._model_client is None:
            raise ValueError("model_client es requerido cuando enable_autogen=True.")

    def propose(self, requirements: Requirements) -> SolutionProposal:
        if self._enable_autogen:
            proposal = self._propose_with_llm(requirements)
        else:
            proposal = generate_solution(requirements)
        ensure_no_gateway_in_proposal(proposal)
        return proposal

    def _propose_with_llm(self, requirements: Requirements) -> SolutionProposal:
        prompt = self._build_prompt(requirements)
        response_text = self._call_model(prompt)
        payload = _extract_json(response_text)
        try:
            if hasattr(SolutionProposal, "model_validate_json"):
                return SolutionProposal.model_validate_json(payload)
            return SolutionProposal.parse_raw(payload)
        except Exception as exc:  # pragma: no cover - defensive
            raise ValueError("No se pudo parsear la respuesta del LLM.") from exc

    def _build_prompt(self, requirements: Requirements) -> str:
        return (
            "Eres un Arquitecto de Solucion. Genera una propuesta completa "
            "sin componentes de entrada gestionados. Devuelve SOLO un JSON "
            "que cumpla el schema SolutionProposal.\n\n"
            "Requerimientos:\n"
            f"{requirements.model_dump_json(indent=2)}\n\n"
            "El JSON debe incluir: diagram_mermaid, components, flows, adrs, "
            "backlog, risks, cost_estimate."
        )

    def _call_model(self, prompt: str) -> str:
        if self._model_client is None:
            raise RuntimeError("model_client no configurado.")

        messages = [
            {
                "role": "system",
                "content": (
                    "Responde solo con JSON valido. No incluyas texto extra."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        create_fn = getattr(self._model_client, "create", None)
        if create_fn is None:
            raise RuntimeError("model_client no tiene metodo create.")

        if asyncio.iscoroutinefunction(create_fn):
            response = asyncio.run(create_fn(messages=messages))
        else:
            response = create_fn(messages=messages)

        return _extract_content(response)


def _extract_content(response: object) -> str:
    if isinstance(response, dict):
        choices = response.get("choices") or []
        if choices:
            message = choices[0].get("message") or {}
            return message.get("content", "")
        return response.get("content", "")
    if hasattr(response, "choices"):
        choices = getattr(response, "choices", [])
        if choices:
            message = getattr(choices[0], "message", None)
            if message is not None:
                return getattr(message, "content", "")
    if hasattr(response, "content"):
        return getattr(response, "content")
    return str(response)


def _extract_json(text: str) -> str:
    fenced = re.findall(r"```(?:json)?\s*(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    if fenced:
        return fenced[0].strip()
    return text.strip()
