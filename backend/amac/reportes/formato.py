"""Componente amac.reportes.formato; lógica extraída de report_generator.py."""

from datetime import datetime


def _format_date(date_str: str) -> str:
    """Formatea una fecha YYYYMMDD a DD/MM/YYYY."""
    try:
        dt = datetime.strptime(date_str, "%Y%m%d")
        return dt.strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        return date_str


def _score_color_class(value: float) -> str:
    """Retorna la clase CSS según el puntaje."""
    if value >= 70:
        return "score-high"
    elif value >= 45:
        return "score-medium"
    return "score-low"
