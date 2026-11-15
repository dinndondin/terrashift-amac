"""Componente amac.rotaciones.estrategias; lógica extraída de rotation_engine.py."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from amac.rotaciones.analisis import _analyze_rotation, _gather_evidence, _identify_gaps
from amac.rotaciones.calendario import _recommend_periods
from amac.rotaciones.constructores import _build_climate_resilient_rotation, _build_economic_rotation, _build_soil_health_rotation
from amac.rotaciones.puntuacion import _validate_priorities, score_rotation


def generate_rotation_strategies(
    location_data: Dict[str, Any],
    climate_data: Optional[Dict[str, Any]],
    current_crops: List[str],
    soil_type: str,
    farmer_priorities: Optional[Dict[str, float]] = None,
) -> List[Dict[str, Any]]:
    """
    Genera al menos 3 estrategias de rotación para las condiciones dadas.

    Estrategias generadas:
        1. Rotación actual del agricultor (evaluada con puntajes).
        2. Rotación optimizada para salud del suelo.
        3. Rotación optimizada para retorno económico.
        4. (Opcional) Rotación optimizada para resiliencia climática.

    Args:
        location_data: {"lat": float, "lon": float, "name": str (opcional)}.
        climate_data: Resultado de fetch_climate_data() o None.
        current_crops: Lista de cultivos que el agricultor usa actualmente.
        soil_type: Tipo de suelo.
        farmer_priorities: Pesos de prioridad del agricultor.

    Returns:
        Lista de diccionarios, cada uno representando una estrategia completa.
    """
    prios = _validate_priorities(farmer_priorities)
    strategies: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------- #
    #  Estrategia 1: Rotación actual
    # ------------------------------------------------------------------- #
    current_scores = score_rotation(current_crops, climate_data, soil_type, prios)
    current_benefits, current_risks = _analyze_rotation(current_crops)

    strategies.append({
        "name": "Rotación Actual",
        "description": (
            "Evaluación de la rotación que el agricultor utiliza actualmente. "
            "Sirve como línea base para comparar las alternativas propuestas."
        ),
        "crop_sequence": current_crops,
        "scores": current_scores,
        "benefits": current_benefits,
        "risks": current_risks,
        "evidence": _gather_evidence(current_crops, climate_data),
        "information_gaps": _identify_gaps(climate_data, soil_type),
        "recommended_period": _recommend_periods(current_crops),
    })

    # ------------------------------------------------------------------- #
    #  Estrategia 2: Optimizada para salud del suelo
    # ------------------------------------------------------------------- #
    soil_rotation = _build_soil_health_rotation(current_crops, soil_type, climate_data)
    soil_scores = score_rotation(soil_rotation, climate_data, soil_type, prios)
    soil_benefits, soil_risks = _analyze_rotation(soil_rotation)

    strategies.append({
        "name": "Rotación para Salud del Suelo",
        "description": (
            "Rotación diseñada para maximizar la salud y fertilidad del suelo. "
            "Incluye cultivos fijadores de nitrógeno, diversidad de profundidades "
            "radiculares y alto aporte de materia orgánica."
        ),
        "crop_sequence": soil_rotation,
        "scores": soil_scores,
        "benefits": soil_benefits,
        "risks": soil_risks,
        "evidence": _gather_evidence(soil_rotation, climate_data),
        "information_gaps": _identify_gaps(climate_data, soil_type),
        "recommended_period": _recommend_periods(soil_rotation),
    })

    # ------------------------------------------------------------------- #
    #  Estrategia 3: Optimizada para retorno económico
    # ------------------------------------------------------------------- #
    econ_rotation = _build_economic_rotation(current_crops, soil_type, climate_data)
    econ_scores = score_rotation(econ_rotation, climate_data, soil_type, prios)
    econ_benefits, econ_risks = _analyze_rotation(econ_rotation)

    strategies.append({
        "name": "Rotación para Máximo Retorno Económico",
        "description": (
            "Rotación que prioriza cultivos de alto valor de mercado manteniendo "
            "un mínimo de diversidad para la sostenibilidad del sistema."
        ),
        "crop_sequence": econ_rotation,
        "scores": econ_scores,
        "benefits": econ_benefits,
        "risks": econ_risks,
        "evidence": _gather_evidence(econ_rotation, climate_data),
        "information_gaps": _identify_gaps(climate_data, soil_type),
        "recommended_period": _recommend_periods(econ_rotation),
    })

    # ------------------------------------------------------------------- #
    #  Estrategia 4: Optimizada para resiliencia climática
    # ------------------------------------------------------------------- #
    resilient_rotation = _build_climate_resilient_rotation(
        current_crops, soil_type, climate_data
    )
    resilient_scores = score_rotation(resilient_rotation, climate_data, soil_type, prios)
    resilient_benefits, resilient_risks = _analyze_rotation(resilient_rotation)

    strategies.append({
        "name": "Rotación para Resiliencia Climática",
        "description": (
            "Rotación diseñada para resistir condiciones climáticas adversas. "
            "Prioriza cultivos tolerantes a sequía y heladas, con bajo riesgo "
            "ante variabilidad climática."
        ),
        "crop_sequence": resilient_rotation,
        "scores": resilient_scores,
        "benefits": resilient_benefits,
        "risks": resilient_risks,
        "evidence": _gather_evidence(resilient_rotation, climate_data),
        "information_gaps": _identify_gaps(climate_data, soil_type),
        "recommended_period": _recommend_periods(resilient_rotation),
    })

    # Ordenar por puntaje general (descendente), manteniendo la actual primero
    strategies[1:] = sorted(strategies[1:], key=lambda s: s["scores"]["overall"], reverse=True)

    return strategies
