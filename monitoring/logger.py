from __future__ import annotations

import logging
import uuid
from typing import Optional


class TraceFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        trace_id = getattr(record, "trace_id", "-")
        record.trace_id = trace_id
        return super().format(record)


def get_logger(name: str, request_id: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = TraceFormatter(
            fmt="%(asctime)s %(levelname)s [%(trace_id)s] %(name)s %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    extra = {"trace_id": request_id or "-"}
    logger = logging.LoggerAdapter(logger, extra=extra)
    return logger


def new_trace_id() -> str:
    """Genera un identificador de trazabilidad para la ejecucion."""
    return str(uuid.uuid4())[:8]
