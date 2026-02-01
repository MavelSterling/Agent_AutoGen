"""Web scraping de precios de Azure, AWS y Google Cloud para estimación de costos.

Solo se usan datos obtenidos por web scraping a las URLs de precios de cada proveedor.
Si el scraping no obtiene datos (p. ej. página vacía por JS, error de red o sin tablas
parseables), se devuelve lista vacía. Para sitios muy dinámicos podría requerirse
Playwright/Selenium (no incluido aquí).
"""

from __future__ import annotations

import logging
from typing import Any, List

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# URLs de páginas de precios (objetivo del scraping; muchas son JS-heavy).
AZURE_PRICING_URL = "https://azure.microsoft.com/en-us/pricing/calculator/"
AWS_PRICING_URL = "https://aws.amazon.com/pricing/"
GCP_PRICING_URL = "https://cloud.google.com/pricing"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"
)
HTML_PARSER = "html.parser"


def fetch_cloud_pricing(provider: str) -> List[dict[str, Any]]:
    """Obtiene precios por web scraping a la página del proveedor (azure, aws, gcp).

    Devuelve lista vacía si no hay datos (error de red, página vacía o sin tablas parseables).
    """
    provider = (provider or "").strip().lower()
    try:
        if provider == "azure":
            return _scrape_azure()
        if provider == "aws":
            return _scrape_aws()
        if provider in ("gcp", "google", "google cloud"):
            return _scrape_gcp()
        return []
    except Exception as e:
        logger.warning("Error en scraping de precios para %s: %s", provider, e)
        return []


def _get_html(url: str) -> str:
    try:
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=15)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        logger.warning("No se pudo obtener %s: %s", url, e)
        return ""


def _parse_pricing_tables(soup: BeautifulSoup, provider: str, fuente: str) -> List[dict[str, Any]]:
    """Extrae filas de tablas con clase que contenga 'pricing'."""
    rows: List[dict[str, Any]] = []
    for table in soup.find_all("table", class_=lambda c: c and "pricing" in str(c).lower()):
        for tr in table.find_all("tr")[1:]:
            cells = tr.find_all(["td", "th"])
            if len(cells) >= 2:
                servicio = (cells[0].get_text() or "").strip()
                precio = (cells[1].get_text() or "").strip()
                if servicio and precio:
                    rows.append({
                        "provider": provider,
                        "servicio": servicio,
                        "unidad": "variable",
                        "precio": precio,
                        "region": "",
                        "fuente": fuente,
                    })
    return rows


def _parse_any_tables_with_prices(soup: BeautifulSoup, provider: str, fuente: str) -> List[dict[str, Any]]:
    """Intento secundario: cualquier tabla con al menos 2 columnas; filtra filas que parezcan precio."""
    rows: List[dict[str, Any]] = []
    for table in soup.find_all("table")[:5]:
        for tr in table.find_all("tr")[1:]:
            cells = tr.find_all(["td", "th"])
            if len(cells) >= 2:
                servicio = (cells[0].get_text() or "").strip()
                precio = (cells[1].get_text() or "").strip()
                if not servicio or not precio:
                    continue
                if len(servicio) > 100:
                    continue
                if any(c in precio for c in ("$", "USD", "€", "EUR", "price", "per ")):
                    rows.append({
                        "provider": provider,
                        "servicio": servicio[:80],
                        "unidad": "variable",
                        "precio": precio[:60],
                        "region": "",
                        "fuente": fuente,
                    })
    return rows[:30]


def _scrape_azure() -> List[dict[str, Any]]:
    html = _get_html(AZURE_PRICING_URL)
    if not html:
        return []
    soup = BeautifulSoup(html, HTML_PARSER)
    rows = _parse_pricing_tables(soup, "Azure", AZURE_PRICING_URL)
    if not rows:
        rows = _parse_any_tables_with_prices(soup, "Azure", AZURE_PRICING_URL)
    return rows


def _scrape_aws() -> List[dict[str, Any]]:
    html = _get_html(AWS_PRICING_URL)
    if not html:
        return []
    soup = BeautifulSoup(html, HTML_PARSER)
    rows = []
    for a in soup.find_all("a", href=True):
        if "/pricing/" in a["href"] and a.get_text(strip=True):
            servicio = a.get_text(strip=True)
            if len(servicio) < 80:
                rows.append({
                    "provider": "AWS",
                    "servicio": servicio,
                    "unidad": "variable",
                    "precio": "(ver enlace)",
                    "region": "",
                    "fuente": AWS_PRICING_URL,
                })
    if len(rows) > 20:
        rows = rows[:20]
    if not rows:
        rows = _parse_any_tables_with_prices(soup, "AWS", AWS_PRICING_URL)
    return rows


def _scrape_gcp() -> List[dict[str, Any]]:
    html = _get_html(GCP_PRICING_URL)
    if not html:
        return []
    soup = BeautifulSoup(html, HTML_PARSER)
    rows = []
    for link in soup.find_all("a", href=True):
        if "pricing" in link["href"] and link.get_text(strip=True):
            servicio = link.get_text(strip=True)
            if 3 < len(servicio) < 80:
                rows.append({
                    "provider": "GCP",
                    "servicio": servicio,
                    "unidad": "variable",
                    "precio": "(ver enlace)",
                    "region": "",
                    "fuente": GCP_PRICING_URL,
                })
    if len(rows) > 20:
        rows = rows[:20]
    if not rows:
        rows = _parse_any_tables_with_prices(soup, "GCP", GCP_PRICING_URL)
    return rows
