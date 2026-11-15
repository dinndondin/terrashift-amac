"""Componente amac.nasa.tendencias; lógica extraída de nasa_api.py."""

from typing import Any
from typing import Dict
from typing import List
from amac.nasa.estadisticas import _safe_mean


def calculate_climate_trends(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcula tendencias a partir de datos climáticos históricos.

    Analiza la variación mensual y detecta meses extremos para cada parámetro.

    Args:
        data: Resultado de fetch_climate_data().

    Returns:
        Diccionario con tendencias mensuales y observaciones.
    """
    parameters = data.get("parameters", {})
    trends: Dict[str, Any] = {}

    for param_name, daily_values in parameters.items():
        # Agrupar valores por mes
        monthly_groups: Dict[int, List[float]] = {}
        for date_str, val in daily_values.items():
            if val is None:
                continue
            try:
                month = int(date_str[4:6])  # YYYYMMDD → MM
                monthly_groups.setdefault(month, []).append(val)
            except (ValueError, IndexError):
                continue

        monthly_means = {}
        for m in range(1, 13):
            vals = monthly_groups.get(m, [])
            monthly_means[m] = _safe_mean(vals)

        # Identificar meses extremos
        valid_months = {k: v for k, v in monthly_means.items() if v is not None}
        mes_max = max(valid_months, key=valid_months.get) if valid_months else None
        mes_min = min(valid_months, key=valid_months.get) if valid_months else None

        trends[param_name] = {
            "promedios_mensuales": monthly_means,
            "mes_valor_maximo": mes_max,
            "mes_valor_minimo": mes_min,
            "rango": (
                round(valid_months.get(mes_max, 0) - valid_months.get(mes_min, 0), 2)
                if mes_max and mes_min else None
            ),
        }

    return {
        "tendencias": trends,
        "observaciones": _generate_trend_observations(trends),
    }


def _generate_trend_observations(trends: Dict[str, Any]) -> List[str]:
    """Genera observaciones en español sobre las tendencias detectadas."""
    obs: List[str] = []

    # Temperatura
    if "T2M" in trends:
        t = trends["T2M"]
        if t["mes_valor_maximo"]:
            obs.append(
                f"El mes más cálido es el mes {t['mes_valor_maximo']} "
                f"con un promedio de {t['promedios_mensuales'].get(t['mes_valor_maximo'])}°C."
            )
        if t["mes_valor_minimo"]:
            obs.append(
                f"El mes más frío es el mes {t['mes_valor_minimo']} "
                f"con un promedio de {t['promedios_mensuales'].get(t['mes_valor_minimo'])}°C."
            )

    # Precipitación
    if "PRECTOTCORR" in trends:
        p = trends["PRECTOTCORR"]
        if p["mes_valor_maximo"]:
            obs.append(
                f"La mayor precipitación se concentra en el mes {p['mes_valor_maximo']}."
            )
        if p["mes_valor_minimo"]:
            obs.append(
                f"El mes más seco es el mes {p['mes_valor_minimo']}."
            )

    return obs
