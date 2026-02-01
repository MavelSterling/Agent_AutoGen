from __future__ import annotations

import argparse
import json
from pathlib import Path

from monitoring.logger import get_logger, new_trace_id
from src.agent import SolutionArchitectAgent, write_docs
from src.core.config import load_config
from src.core.llm import build_model_client
from src.core.schemas import Requirements


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Arquitecto de Solucion (AutoGen)")
    parser.add_argument(
        "--input",
        type=str,
        default="data/requirements.json",
        help="Ruta a un JSON con requerimientos (por defecto data/requirements.json).",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yml",
        help="Ruta a config.yml (por defecto config/config.yml).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Directorio base donde se generan los docs.",
    )
    return parser.parse_args()


def _load_requirements(path: str) -> Requirements:
    input_path = Path(path)
    if not input_path.exists():
        raise FileNotFoundError(
            f"No se encontro el archivo de entrada: {input_path}. "
            "Coloca el JSON en data/requirements.json o usa --input."
        )
    raw = input_path.read_text(encoding="utf-8")
    payload = json.loads(raw)
    return Requirements(**payload)


def main() -> None:
    args = _parse_args()
    trace_id = new_trace_id()
    logger = get_logger("solution-architect", request_id=trace_id)
    logger.info("Inicio de ejecucion (input=%s, config=%s)", args.input, args.config)

    logger.info("Cargando configuracion desde %s", args.config)
    config = load_config(args.config)
    logger.info("Configuracion cargada; LLM habilitado=%s", config.llm.enabled)

    logger.info("Cargando requerimientos desde %s", args.input)
    requirements = _load_requirements(args.input)
    logger.info("Requerimientos cargados: project_name=%s, cloud_provider=%s", requirements.project_name, requirements.cloud_provider)

    logger.info("Construyendo cliente de modelo (si aplica)")
    model_client = build_model_client(config.llm)
    agent = SolutionArchitectAgent(
        enable_autogen=config.llm.enabled,
        model_client=model_client,
    )
    logger.info("Agente listo; modo=%s", "LLM" if config.llm.enabled else "determinista")

    logger.info("Generando propuesta de arquitectura")
    proposal = agent.propose(requirements)
    logger.info("Propuesta generada: %d componentes, %d flujos, %d ADRs, %d items backlog", len(proposal.components), len(proposal.flows), len(proposal.adrs), len(proposal.backlog))

    output_dir = args.output or config.paths.output_dir or "data"
    base_path = Path(output_dir).resolve()
    scrape_provider = (config.cost.scrape_provider or "").strip() or (requirements.cloud_provider or "").strip()
    logger.info("Escribiendo salida en %s (scrape_provider=%s)", base_path, scrape_provider or "ninguno")
    write_docs(
        base_path,
        proposal,
        scrape_provider=scrape_provider or None,
        resources=requirements.resources or None,
        logger=logger,
    )
    logger.info("Salida generada en %s", base_path)


if __name__ == "__main__":
    main()
