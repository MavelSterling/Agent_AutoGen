from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from src.core.cost_excel import cost_estimate_to_excel
from src.core.schemas import SolutionProposal
from src.core.scraping import fetch_cloud_pricing
from src.core.templates import (
    adr_to_markdown,
    backlog_to_csv,
    proposal_to_markdown,
    risks_to_markdown,
)


def write_docs(
    base_path: Path,
    proposal: SolutionProposal,
    scrape_provider: Optional[str] = None,
    resources: Optional[list[str]] = None,
    logger: Optional[logging.Logger] = None,
) -> None:
    log = logger or logging.getLogger("solution-architect.write_docs")
    output_path = base_path
    log.info("Creando directorios en %s", output_path)
    (output_path / "architecture").mkdir(parents=True, exist_ok=True)
    (output_path / "adr").mkdir(parents=True, exist_ok=True)
    (output_path / "backlog").mkdir(parents=True, exist_ok=True)
    (output_path / "risk").mkdir(parents=True, exist_ok=True)
    (output_path / "cost").mkdir(parents=True, exist_ok=True)

    architecture_path = output_path / "architecture" / "solution-proposal.md"
    log.info("Escribiendo propuesta en %s", architecture_path)
    architecture_path.write_text(proposal_to_markdown(proposal), encoding="utf-8")

    if proposal.adrs:
        adr = proposal.adrs[0]
        adr_path = output_path / "adr" / f"{adr.id}-{_slugify(adr.title)}.md"
        log.info("Escribiendo ADR en %s", adr_path)
        adr_path.write_text(adr_to_markdown(adr), encoding="utf-8")

    backlog_path = output_path / "backlog" / "backlog.csv"
    log.info("Escribiendo backlog en %s", backlog_path)
    backlog_path.write_text(backlog_to_csv(proposal.backlog), encoding="utf-8")

    risk_path = output_path / "risk" / "risk-register.md"
    log.info("Escribiendo registro de riesgos en %s", risk_path)
    risk_path.write_text(risks_to_markdown(proposal.risks), encoding="utf-8")

    cost_path = output_path / "cost" / "cost-estimate.xlsx"
    scraped_rows: list = []
    if scrape_provider and scrape_provider.strip():
        log.info("Obteniendo precios por scraping: provider=%s", scrape_provider)
        scraped_rows = fetch_cloud_pricing(scrape_provider.strip())
        log.info("Scraping completado: %d filas de precios", len(scraped_rows))
    log.info("Escribiendo estimacion de costos en %s", cost_path)
    cost_estimate_to_excel(
        proposal.cost_estimate,
        cost_path,
        scraped_rows=scraped_rows or None,
        resources=resources,
    )


def _slugify(value: str) -> str:
    return (
        value.lower()
        .replace(" ", "-")
        .replace("/", "-")
        .replace(".", "")
        .replace(",", "")
    )
