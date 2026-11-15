"""Componente amac.rotaciones.puntuacion; lógica extraída de rotation_engine.py."""

from amac.cultivos.consultas import get_crop
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from amac.rotaciones.config import DEFAULT_PRIORITIES, _LEVEL_MAP


def _level_to_score(level: str) -> int:
    """Convierte nivel cualitativo a puntaje numérico."""
    return _LEVEL_MAP.get(level.lower(), 2)


def _normalize(value: float, min_val: float = 0, max_val: float = 100) -> float:
    """Normaliza un valor al rango 0-100."""
    if max_val == min_val:
        return 50.0
    return max(0, min(100, round((value - min_val) / (max_val - min_val) * 100, 1)))


def _validate_priorities(priorities: Optional[Dict[str, float]]) -> Dict[str, float]:
    """Valida y completa las prioridades del agricultor."""
    if not priorities:
        return DEFAULT_PRIORITIES.copy()
    validated = DEFAULT_PRIORITIES.copy()
    for key, val in priorities.items():
        if key in validated:
            validated[key] = max(0.0, min(1.0, float(val)))
    return validated


def score_rotation(
    rotation: List[str],
    climate_data: Optional[Dict[str, Any]],
    soil_type: str,
    priorities: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """
    Evalúa una secuencia de rotación y genera puntajes multidimensionales.

    La puntuación se basa en:
        - Salud del suelo: diversidad de raíces, aporte de materia orgánica,
          fijación de N, puntaje de mejora de suelo.
        - Eficiencia hídrica: necesidades de agua vs. disponibilidad implícita.
        - Resiliencia climática: tolerancia a sequía, heladas, rango de
          temperaturas.
        - Potencial económico: valor de mercado de los cultivos.
        - Control de plagas: ruptura de ciclos, diversidad de familias.
        - Control de erosión: cobertura del suelo y raíces.

    Args:
        rotation: Lista de nombres de cultivos en secuencia.
        climate_data: Resultado de fetch_climate_data() o None.
        soil_type: Tipo de suelo.
        priorities: Pesos del agricultor (0-1 por categoría).

    Returns:
        Diccionario con puntajes individuales y puntaje general ponderado.
    """
    prios = _validate_priorities(priorities)

    # Obtener datos de cada cultivo en la rotación
    crops = []
    for name in rotation:
        crop = get_crop(name)
        if crop:
            crops.append(crop)

    if not crops:
        return {
            "soil_health": 0, "water_efficiency": 0,
            "climate_resilience": 0, "economic_potential": 0,
            "pest_management": 0, "erosion_control": 0,
            "overall": 0, "detalle": "No se encontraron cultivos válidos.",
        }

    n = len(crops)

    # --- Salud del suelo ---
    avg_soil_score = sum(c["soil_improvement_score"] for c in crops) / n
    n_fixers = sum(1 for c in crops if c["nitrogen_fixer"])
    om_score = sum(_level_to_score(c["organic_matter_contribution"]) for c in crops) / n
    depth_diversity = len(set(c["root_depth"] for c in crops))

    soil_health = _normalize(
        (avg_soil_score / 10 * 40) +
        (n_fixers / n * 25) +
        (om_score / 3 * 20) +
        (depth_diversity / 3 * 15),
        0, 100,
    )

    # --- Eficiencia hídrica ---
    water_scores = [_level_to_score(c["water_need"]) for c in crops]
    drought_scores = [_level_to_score(c["drought_tolerance"]) for c in crops]
    avg_water = sum(water_scores) / n
    avg_drought = sum(drought_scores) / n
    # Menor necesidad de agua + mayor tolerancia a sequía = mayor eficiencia
    water_efficiency = _normalize(
        ((3 - avg_water + 1) / 3 * 50) + (avg_drought / 3 * 50),
        0, 100,
    )

    # Ajuste por tipo de suelo
    if soil_type.lower() in ("arenoso", "franco-arenoso"):
        # Suelos arenosos drenan rápido → penalizar cultivos que requieren mucha agua
        water_efficiency = min(100, water_efficiency * 1.1 if avg_drought >= 2 else water_efficiency * 0.85)

    # --- Resiliencia climática ---
    frost_scores = [_level_to_score(c["frost_tolerance"]) for c in crops]
    temp_ranges = [c["temp_max"] - c["temp_min"] for c in crops]
    avg_frost = sum(frost_scores) / n
    avg_temp_range = sum(temp_ranges) / n

    climate_resilience = _normalize(
        (avg_frost / 3 * 35) +
        (avg_drought / 3 * 35) +
        (min(avg_temp_range / 30, 1) * 30),
        0, 100,
    )

    # Si hay datos climáticos reales, ajustar
    if climate_data:
        summary = climate_data.get("summary", {})
        t2m_min = summary.get("T2M_MIN", {}).get("minimo")
        if t2m_min is not None and t2m_min < 0:
            # Hay heladas → bonificar cultivos tolerantes
            if avg_frost >= 2.5:
                climate_resilience = min(100, climate_resilience + 10)
            else:
                climate_resilience = max(0, climate_resilience - 15)

    # --- Potencial económico ---
    market_scores = [_level_to_score(c["market_value"]) for c in crops]
    forage_scores = [_level_to_score(c["forage_value"]) for c in crops]
    avg_market = sum(market_scores) / n
    avg_forage = sum(forage_scores) / n
    economic_potential = _normalize(
        (avg_market / 3 * 70) + (avg_forage / 3 * 30),
        0, 100,
    )

    # --- Manejo de plagas ---
    pest_breakers = sum(1 for c in crops if c["pest_break"])
    category_diversity = len(set(c["category"] for c in crops))
    pest_management = _normalize(
        (pest_breakers / n * 50) +
        (min(category_diversity / 4, 1) * 50),
        0, 100,
    )

    # --- Control de erosión ---
    erosion_scores = [_level_to_score(c["erosion_control"]) for c in crops]
    avg_erosion = sum(erosion_scores) / n
    deep_roots = sum(1 for c in crops if c["root_depth"] == "profunda")
    erosion_control_score = _normalize(
        (avg_erosion / 3 * 60) + (deep_roots / n * 40),
        0, 100,
    )

    # --- Puntaje general ponderado ---
    total_weight = sum(prios.values())
    if total_weight == 0:
        total_weight = 1

    overall = round(
        (
            soil_health * prios["soil_health"] +
            water_efficiency * prios["water_conservation"] +
            climate_resilience * prios.get("water_conservation", 0.5) * 0.5 +  # clima contribuye parcialmente
            economic_potential * prios["economic_return"] +
            pest_management * prios["pest_management"] +
            erosion_control_score * prios["erosion_control"] +
            soil_health * prios["nitrogen_fixation"] * 0.5  # N-fixation se refleja en soil_health
        ) / (total_weight + 0.5 + 0.5),
        1,
    )

    return {
        "soil_health": round(soil_health, 1),
        "water_efficiency": round(water_efficiency, 1),
        "climate_resilience": round(climate_resilience, 1),
        "economic_potential": round(economic_potential, 1),
        "pest_management": round(pest_management, 1),
        "erosion_control": round(erosion_control_score, 1),
        "overall": round(overall, 1),
    }
