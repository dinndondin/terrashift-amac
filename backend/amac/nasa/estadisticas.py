"""Componente amac.nasa.estadisticas; lógica extraída de nasa_api.py."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from amac.nasa.config import _FILL_VALUE


def _clean_values(data: Dict[str, float]) -> Dict[str, float]:
    """Reemplaza valores centinela (-999) por None para un manejo limpio."""
    return {k: (v if v != _FILL_VALUE else None) for k, v in data.items()}


def _safe_mean(values: List[Optional[float]]) -> Optional[float]:
    """Calcula la media ignorando valores None."""
    clean = [v for v in values if v is not None]
    return round(sum(clean) / len(clean), 2) if clean else None


def _safe_min(values: List[Optional[float]]) -> Optional[float]:
    clean = [v for v in values if v is not None]
    return min(clean) if clean else None


def _safe_max(values: List[Optional[float]]) -> Optional[float]:
    clean = [v for v in values if v is not None]
    return max(clean) if clean else None


def _build_summary(cleaned: Dict[str, Dict[str, Optional[float]]]) -> Dict[str, Any]:
    """Genera resumen estadístico a partir de datos diarios limpiados."""
    summary: Dict[str, Any] = {}
    for param_name, daily in cleaned.items():
        values = list(daily.values())
        summary[param_name] = {
            "promedio": _safe_mean(values),
            "minimo": _safe_min(values),
            "maximo": _safe_max(values),
            "dias_con_datos": sum(1 for v in values if v is not None),
            "dias_sin_datos": sum(1 for v in values if v is None),
        }
    return summary
