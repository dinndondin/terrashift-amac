"""Componente amac.cultivos.consultas; lógica extraída de crop_database.py."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from amac.cultivos.catalogo import CROPS_DB


def get_all_crops() -> List[Dict[str, Any]]:
    """
    Retorna la lista completa de cultivos disponibles en la base de datos.

    Returns:
        Lista de diccionarios con la información de cada cultivo.
    """
    return CROPS_DB


def get_crop(name: str) -> Optional[Dict[str, Any]]:
    """
    Busca un cultivo por su nombre (case-insensitive).

    Args:
        name: Nombre del cultivo en español.

    Returns:
        Diccionario con la información del cultivo, o None si no se encuentra.
    """
    name_lower = name.lower().strip()
    for crop in CROPS_DB:
        if crop["name"].lower() == name_lower:
            return crop
    return None


def get_crops_by_category(category: str) -> List[Dict[str, Any]]:
    """
    Filtra cultivos por categoría.

    Args:
        category: Una de: cereal, leguminosa, hortaliza, forrajero, cobertura,
                  oleaginosa, tubérculo, pseudocereal.

    Returns:
        Lista de cultivos que pertenecen a la categoría indicada.
    """
    cat_lower = category.lower().strip()
    return [c for c in CROPS_DB if c["category"].lower() == cat_lower]


def get_compatible_crops(
    current_crop: str,
    soil_type: str,
    climate_data: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Filtra cultivos compatibles con el cultivo actual, tipo de suelo y clima.

    Criterios de filtrado:
        1. El cultivo aparece en la lista compatible_rotations del cultivo actual.
        2. Si hay datos climáticos, la temperatura promedio cae dentro del rango
           del cultivo candidato.
        3. Se ajusta según el tipo de suelo (ej. suelos arenosos favorecen
           cultivos tolerantes a sequía).

    Args:
        current_crop: Nombre del cultivo actual.
        soil_type: Tipo de suelo (arcilloso, arenoso, limoso, franco, etc.).
        climate_data: Datos climáticos (resultado de fetch_climate_data), opcional.

    Returns:
        Lista de cultivos compatibles ordenados por soil_improvement_score.
    """
    crop = get_crop(current_crop)
    if crop is None:
        # Si no encontramos el cultivo actual, devolvemos todos
        return CROPS_DB

    # Paso 1: filtrar por compatibilidad de rotación declarada
    compatible_names = {n.lower() for n in crop["compatible_rotations"]}
    candidates = [
        c for c in CROPS_DB
        if c["name"].lower() in compatible_names and c["name"] != crop["name"]
    ]

    # Paso 2: filtrar por temperatura si hay datos climáticos
    if climate_data:
        summary = climate_data.get("summary", {})
        t2m = summary.get("T2M", {})
        avg_temp = t2m.get("promedio")
        if avg_temp is not None:
            candidates = [
                c for c in candidates
                if c["temp_min"] <= avg_temp <= c["temp_max"]
            ]

    # Paso 3: ajuste por tipo de suelo
    soil_lower = soil_type.lower().strip()
    if soil_lower == "arenoso":
        # Priorizar cultivos tolerantes a sequía
        candidates = [
            c for c in candidates
            if c["drought_tolerance"] in ("medio", "alto")
        ]
    elif soil_lower == "arcilloso":
        # Priorizar cultivos con raíces que descompacten
        candidates.sort(
            key=lambda c: (
                0 if c["root_depth"] == "profunda"
                else 1 if c["root_depth"] == "media"
                else 2
            )
        )

    # Ordenar por puntaje de mejora de suelo (descendente)
    candidates.sort(key=lambda c: c["soil_improvement_score"], reverse=True)

    return candidates
