"""Componente amac.rotaciones.analisis; lógica extraída de rotation_engine.py."""

from amac.cultivos.consultas import get_crop
from typing import Any
from typing import Dict
from typing import List
from typing import Optional


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
