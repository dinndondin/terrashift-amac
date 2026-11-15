"""Componente amac.regional.servicio; lógica extraída de regional_api.py."""

from typing import Any
from typing import Dict
from amac.regional.perfiles import BIOBIO_REGIONAL_PROFILE


def get_biobio_summary() -> Dict[str, Any]:
    """Retorna el resumen consolidado de la cuenca/provincia del Biobío."""
    return {
        "status": "success",
        "service": "Terrashift Regional API (B2B2C)",
        "model": "NASA Earth Observation + SoilGrids Data Fusion",
        "data": BIOBIO_REGIONAL_PROFILE
    }
