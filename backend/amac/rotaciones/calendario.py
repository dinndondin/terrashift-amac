"""Componente amac.rotaciones.calendario; lógica extraída de rotation_engine.py."""

from amac.cultivos.consultas import get_all_crops
from amac.cultivos.consultas import get_crop
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from amac.rotaciones.config import MONTH_NAMES


def _recommend_periods(crop_names: List[str]) -> List[Dict[str, Any]]:
    """Genera recomendaciones de períodos de siembra para cada cultivo."""
    periods: List[Dict[str, Any]] = []

    for name in crop_names:
        crop = get_crop(name)
        if not crop:
            continue

        planting = crop.get("planting_months", [])
        month_names = [MONTH_NAMES.get(m, str(m)) for m in planting]

        periods.append({
            "cultivo": name,
            "meses_siembra": month_names,
            "duracion_ciclo_dias": crop.get("growing_season_days", 0),
            "nota": (
                f"Ciclo de {crop.get('growing_season_days', '?')} días. "
                f"Siembra recomendada: {', '.join(month_names)}."
            ),
        })

    return periods


def identify_fallow_windows(
    climate_data: Optional[Dict[str, Any]],
    current_crops: List[str],
) -> Dict[str, Any]:
    """
    Identifica ventanas de barbecho (suelo descubierto) y sugiere cultivos
    de cobertura para esos períodos.

    Args:
        climate_data: Datos climáticos de la ubicación.
        current_crops: Cultivos que el agricultor planta actualmente.

    Returns:
        Diccionario con meses de barbecho detectados y coberturas recomendadas.
    """
    # Determinar meses ocupados por los cultivos actuales
    occupied_months: set = set()
    for name in current_crops:
        crop = get_crop(name)
        if not crop:
            continue
        planting = crop.get("planting_months", [])
        season_days = crop.get("growing_season_days", 120)
        season_months = max(1, season_days // 30)

        for start_month in planting:
            for offset in range(season_months):
                m = ((start_month - 1 + offset) % 12) + 1
                occupied_months.add(m)

    # Meses libres
    all_months = set(range(1, 13))
    fallow_months = sorted(all_months - occupied_months)

    if not fallow_months:
        return {
            "meses_barbecho": [],
            "coberturas_recomendadas": [],
            "mensaje": "No se detectaron ventanas de barbecho significativas.",
        }

    fallow_names = [MONTH_NAMES[m] for m in fallow_months]

    # Recomendar cultivos de cobertura para esos meses
    cover_crops = [
        c for c in get_all_crops()
        if c["category"] in ("cobertura", "forrajero")
        and c["soil_improvement_score"] >= 7
    ]

    recommendations: List[Dict[str, str]] = []
    for cc in cover_crops:
        # Verificar que el cultivo se pueda plantar en algún mes de barbecho
        overlap = set(cc["planting_months"]) & set(fallow_months)
        if overlap:
            months_str = ", ".join(MONTH_NAMES[m] for m in sorted(overlap))
            recommendations.append({
                "cultivo": cc["name"],
                "meses_posibles": months_str,
                "beneficio_principal": cc["benefits"][0] if cc["benefits"] else "",
                "puntaje_mejora_suelo": cc["soil_improvement_score"],
            })

    recommendations.sort(key=lambda x: x["puntaje_mejora_suelo"], reverse=True)

    return {
        "meses_barbecho": fallow_names,
        "meses_barbecho_num": fallow_months,
        "coberturas_recomendadas": recommendations[:5],
        "mensaje": (
            f"Se detectaron {len(fallow_months)} meses con suelo potencialmente "
            f"descubierto: {', '.join(fallow_names)}. "
            "Se recomienda implementar cultivos de cobertura para proteger "
            "el suelo y mejorar su fertilidad."
        ),
    }
