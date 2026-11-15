"""Componente amac.rotaciones.constructores; lógica extraída de rotation_engine.py."""

from amac.cultivos.consultas import get_all_crops
from amac.cultivos.consultas import get_crop
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from amac.rotaciones.config import _DEPTH_MAP
from amac.rotaciones.puntuacion import _level_to_score


def _build_soil_health_rotation(
    current_crops: List[str],
    soil_type: str,
    climate_data: Optional[Dict[str, Any]],
) -> List[str]:
    """Construye una rotación orientada a mejorar la salud del suelo."""
    all_crops = get_all_crops()

    # Priorizar: alto soil_improvement_score, fijadores de N, raíces profundas
    scored = []
    for c in all_crops:
        s = (
            c["soil_improvement_score"] * 3 +
            (3 if c["nitrogen_fixer"] else 0) +
            _DEPTH_MAP.get(c["root_depth"], 1) +
            _level_to_score(c["organic_matter_contribution"]) * 2
        )
        scored.append((c["name"], s, c))

    scored.sort(key=lambda x: x[1], reverse=True)

    # Construir rotación diversa (alternar leguminosa/gramínea/cobertura)
    rotation: List[str] = []
    used_categories: set = set()

    # Mantener al menos un cultivo del agricultor si tiene valor
    for name in current_crops[:1]:
        crop = get_crop(name)
        if crop and crop["market_value"] in ("medio", "alto"):
            rotation.append(name)
            used_categories.add(crop["category"])

    # Agregar los mejores cultivos para suelo, diversificando categorías
    for name, score, crop in scored:
        if name in rotation:
            continue
        if len(rotation) >= 4:
            break
        # Diversificar categorías
        if crop["category"] not in used_categories or len(used_categories) >= 3:
            rotation.append(name)
            used_categories.add(crop["category"])

    # Asegurar al menos 3 cultivos
    if len(rotation) < 3:
        for name, _, crop in scored:
            if name not in rotation:
                rotation.append(name)
            if len(rotation) >= 3:
                break

    return rotation


def _build_economic_rotation(
    current_crops: List[str],
    soil_type: str,
    climate_data: Optional[Dict[str, Any]],
) -> List[str]:
    """Construye una rotación orientada al máximo retorno económico."""
    all_crops = get_all_crops()

    # Priorizar alto valor de mercado
    high_value = [c for c in all_crops if c["market_value"] == "alto"]
    high_value.sort(key=lambda c: c["soil_improvement_score"], reverse=True)

    rotation: List[str] = []

    # Siempre incluir un cultivo de alto valor
    for c in high_value:
        if len(rotation) >= 2:
            break
        rotation.append(c["name"])

    # Agregar un fijador de N para mantener fertilidad (reducir costos de fertilizante)
    n_fixers = [c for c in all_crops if c["nitrogen_fixer"] and c["name"] not in rotation]
    n_fixers.sort(key=lambda c: _level_to_score(c["market_value"]), reverse=True)
    if n_fixers:
        rotation.append(n_fixers[0]["name"])

    # Agregar un cultivo de cobertura económico si hay espacio
    if len(rotation) < 4:
        for c in all_crops:
            if (c["name"] not in rotation and
                c["category"] in ("cobertura", "forrajero") and
                c["soil_improvement_score"] >= 7):
                rotation.append(c["name"])
                break

    return rotation[:4]


def _build_climate_resilient_rotation(
    current_crops: List[str],
    soil_type: str,
    climate_data: Optional[Dict[str, Any]],
) -> List[str]:
    """Construye una rotación orientada a resiliencia climática."""
    all_crops = get_all_crops()

    # Evaluar resiliencia de cada cultivo
    scored = []
    for c in all_crops:
        resilience = (
            _level_to_score(c["drought_tolerance"]) * 3 +
            _level_to_score(c["frost_tolerance"]) * 2 +
            (c["temp_max"] - c["temp_min"]) / 10 +
            _DEPTH_MAP.get(c["root_depth"], 1)
        )
        scored.append((c["name"], resilience, c))

    scored.sort(key=lambda x: x[1], reverse=True)

    rotation: List[str] = []
    used_categories: set = set()

    for name, _, crop in scored:
        if len(rotation) >= 4:
            break
        if crop["category"] not in used_categories or len(rotation) < 2:
            rotation.append(name)
            used_categories.add(crop["category"])

    return rotation
