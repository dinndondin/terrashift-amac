"""
rotation_engine.py - Motor de Estrategias de Rotación de Cultivos
==================================================================
Genera, evalúa y compara estrategias de rotación basadas en datos climáticos
de NASA POWER, las características de los cultivos y las prioridades del
agricultor.

Prioridades del agricultor (pesos de 0.0 a 1.0):
    - water_conservation: conservación de agua
    - soil_health: salud del suelo
    - economic_return: retorno económico
    - pest_management: manejo de plagas
    - erosion_control: control de erosión
    - nitrogen_fixation: fijación de nitrógeno
"""

from typing import Dict, List, Optional, Any
from crop_database import get_crop, get_all_crops, get_compatible_crops

# --------------------------------------------------------------------------- #
#  Constantes
# --------------------------------------------------------------------------- #

# Nombres legibles de los meses en español
MONTH_NAMES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
}

# Tipos de suelo válidos
VALID_SOIL_TYPES = [
    "arcilloso", "arenoso", "limoso", "franco",
    "franco-arcilloso", "franco-arenoso",
]

# Pesos por defecto si el agricultor no los especifica
DEFAULT_PRIORITIES: Dict[str, float] = {
    "water_conservation": 0.5,
    "soil_health": 0.5,
    "economic_return": 0.5,
    "pest_management": 0.5,
    "erosion_control": 0.5,
    "nitrogen_fixation": 0.5,
}

# Mapeos de atributos cualitativos a valores numéricos
_LEVEL_MAP = {"bajo": 1, "medio": 2, "alto": 3}
_DEPTH_MAP = {"superficial": 1, "media": 2, "profunda": 3}


# --------------------------------------------------------------------------- #
#  Funciones auxiliares
# --------------------------------------------------------------------------- #

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


# --------------------------------------------------------------------------- #
#  Puntuación de rotaciones
# --------------------------------------------------------------------------- #

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


# --------------------------------------------------------------------------- #
#  Generación de estrategias
# --------------------------------------------------------------------------- #

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


# --------------------------------------------------------------------------- #
#  Constructores de rotaciones específicas
# --------------------------------------------------------------------------- #

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


# --------------------------------------------------------------------------- #
#  Análisis y evidencia
# --------------------------------------------------------------------------- #

def _analyze_rotation(crop_names: List[str]) -> tuple:
    """
    Analiza una rotación y genera listas de beneficios y riesgos.

    Returns:
        Tupla (beneficios, riesgos) como listas de strings.
    """
    benefits: List[str] = []
    risks: List[str] = []

    crops = [get_crop(n) for n in crop_names]
    crops = [c for c in crops if c is not None]

    if not crops:
        return (["No se pudieron evaluar los cultivos"], ["Datos insuficientes"])

    n = len(crops)
    n_fixers = sum(1 for c in crops if c["nitrogen_fixer"])
    categories = set(c["category"] for c in crops)
    depths = set(c["root_depth"] for c in crops)

    # Beneficios
    if n_fixers > 0:
        benefits.append(
            f"Incluye {n_fixers} cultivo(s) fijador(es) de nitrógeno, reduciendo "
            "necesidad de fertilización nitrogenada."
        )

    if len(categories) >= 3:
        benefits.append(
            f"Alta diversidad de familias ({len(categories)} categorías), "
            "lo que favorece la ruptura de ciclos de plagas."
        )

    if len(depths) >= 2:
        benefits.append(
            "Diversidad de profundidades radiculares que mejora la estructura "
            "del suelo en múltiples capas."
        )

    pest_breakers = sum(1 for c in crops if c["pest_break"])
    if pest_breakers >= n / 2:
        benefits.append(
            "La mayoría de los cultivos en la secuencia rompen ciclos de plagas."
        )

    high_market = [c for c in crops if c["market_value"] == "alto"]
    if high_market:
        names = ", ".join(c["name"] for c in high_market)
        benefits.append(f"Cultivos de alto valor comercial: {names}.")

    # Riesgos
    if n_fixers == 0:
        risks.append(
            "No incluye fijadores de nitrógeno. Se requerirá fertilización "
            "nitrogenada en todos los ciclos."
        )

    if len(categories) == 1:
        risks.append(
            "Todos los cultivos son de la misma familia, lo que puede "
            "incrementar presión de plagas y enfermedades."
        )

    high_water = [c for c in crops if c["water_need"] == "alto"]
    if len(high_water) > n / 2:
        risks.append(
            "Más de la mitad de los cultivos tienen alta demanda de agua. "
            "Puede ser insostenible en zonas con estrés hídrico."
        )

    low_erosion = [c for c in crops if c["erosion_control"] == "bajo"]
    if len(low_erosion) > n / 2:
        risks.append(
            "Bajo control de erosión en la mayoría de los cultivos. "
            "Considere incluir cultivos de cobertura."
        )

    return (benefits, risks)


def _gather_evidence(
    crop_names: List[str],
    climate_data: Optional[Dict[str, Any]],
) -> List[str]:
    """Genera lista de evidencias basadas en datos NASA que soportan la rotación."""
    evidence: List[str] = []

    if not climate_data:
        evidence.append(
            "Sin datos climáticos disponibles. Las recomendaciones se basan "
            "en características generales de los cultivos."
        )
        return evidence

    summary = climate_data.get("summary", {})

    # Temperatura
    t2m = summary.get("T2M", {})
    avg_temp = t2m.get("promedio")
    if avg_temp is not None:
        evidence.append(
            f"Temperatura promedio registrada: {avg_temp}°C "
            f"(datos NASA POWER)."
        )
        crops = [get_crop(n) for n in crop_names if get_crop(n)]
        suitable = [c for c in crops if c["temp_min"] <= avg_temp <= c["temp_max"]]
        evidence.append(
            f"{len(suitable)} de {len(crops)} cultivos están dentro del rango "
            f"de temperatura óptimo para la zona."
        )

    # Precipitación
    precip = summary.get("PRECTOTCORR", {})
    avg_precip = precip.get("promedio")
    if avg_precip is not None:
        evidence.append(
            f"Precipitación diaria promedio: {avg_precip} mm/día "
            f"(datos NASA POWER)."
        )

    # Heladas
    t2m_min = summary.get("T2M_MIN", {})
    min_temp = t2m_min.get("minimo")
    if min_temp is not None:
        if min_temp < 0:
            evidence.append(
                f"Se registraron temperaturas mínimas de {min_temp}°C. "
                "Riesgo de heladas confirmado por datos satelitales."
            )
        else:
            evidence.append(
                f"Temperatura mínima registrada: {min_temp}°C. "
                "Sin registro de heladas en el período analizado."
            )

    # Radiación solar
    solar = summary.get("ALLSKY_SFC_SW_DWN", {})
    avg_solar = solar.get("promedio")
    if avg_solar is not None:
        evidence.append(
            f"Radiación solar promedio: {avg_solar} MJ/m²/día."
        )

    return evidence


def _identify_gaps(
    climate_data: Optional[Dict[str, Any]],
    soil_type: str,
) -> List[str]:
    """Identifica brechas de información que podrían mejorar las recomendaciones."""
    gaps: List[str] = []

    if not climate_data:
        gaps.append("No se dispone de datos climáticos para la ubicación.")
    else:
        summary = climate_data.get("summary", {})
        # Verificar datos faltantes
        for param in ["T2M", "PRECTOTCORR", "GWETROOT"]:
            info = summary.get(param, {})
            missing = info.get("dias_sin_datos", 0)
            if missing > 10:
                gaps.append(
                    f"Faltan {missing} días de datos para {param}. "
                    "Las estimaciones pueden ser menos precisas."
                )

    gaps.append(
        "No se dispone de análisis de suelo de laboratorio. Un análisis de "
        "pH, materia orgánica y nutrientes mejoraría significativamente las recomendaciones."
    )
    gaps.append(
        "No se cuenta con historial de plagas y enfermedades de la parcela."
    )
    gaps.append(
        "Los rendimientos estimados no incluyen factores de manejo agronómico local."
    )

    return gaps


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


# --------------------------------------------------------------------------- #
#  Identificación de ventanas de barbecho
# --------------------------------------------------------------------------- #

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
