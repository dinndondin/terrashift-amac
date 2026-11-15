"""Componente amac.nasa.riesgos; lógica extraída de nasa_api.py."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional


def assess_frost_risk(temp_data: Dict[str, Optional[float]]) -> Dict[str, Any]:
    """
    Evalúa el riesgo de heladas a partir de datos de temperatura mínima diaria.

    Args:
        temp_data: Diccionario {fecha: temperatura_minima} (T2M_MIN).

    Returns:
        Evaluación del riesgo con nivel, conteo de días y meses afectados.
    """
    frost_days: List[str] = []
    frost_months: Dict[int, int] = {}

    for date_str, temp in temp_data.items():
        if temp is None:
            continue
        if temp <= 0:
            frost_days.append(date_str)
            try:
                month = int(date_str[4:6])
                frost_months[month] = frost_months.get(month, 0) + 1
            except (ValueError, IndexError):
                pass

    total_days = sum(1 for v in temp_data.values() if v is not None)
    frost_count = len(frost_days)
    frost_pct = round(frost_count / total_days * 100, 1) if total_days else 0

    # Clasificación del riesgo
    if frost_pct == 0:
        nivel = "bajo"
        descripcion = "No se registraron heladas en el período analizado."
    elif frost_pct < 5:
        nivel = "moderado"
        descripcion = (
            f"Se registraron {frost_count} días con helada ({frost_pct}% del período). "
            "Se recomienda usar cultivos con tolerancia moderada al frío."
        )
    elif frost_pct < 15:
        nivel = "alto"
        descripcion = (
            f"Se registraron {frost_count} días con helada ({frost_pct}% del período). "
            "Se recomienda priorizar cultivos tolerantes al frío y protección contra heladas."
        )
    else:
        nivel = "muy alto"
        descripcion = (
            f"Se registraron {frost_count} días con helada ({frost_pct}% del período). "
            "El riesgo de helada es severo. Considere cultivos altamente resistentes."
        )

    return {
        "nivel_riesgo": nivel,
        "descripcion": descripcion,
        "dias_con_helada": frost_count,
        "porcentaje_dias_helada": frost_pct,
        "meses_afectados": frost_months,
        "primeras_heladas": frost_days[:5] if frost_days else [],
    }


def assess_water_stress(
    precip_data: Dict[str, Optional[float]],
    evap_data: Optional[Dict[str, Optional[float]]] = None,
) -> Dict[str, Any]:
    """
    Evalúa el estrés hídrico comparando precipitación con la humedad del suelo.

    Si no se dispone de datos de evapotranspiración, se usa solo precipitación.

    Args:
        precip_data: Diccionario {fecha: precipitación_mm} (PRECTOTCORR).
        evap_data: Diccionario {fecha: humedad_zona_radicular} (GWETROOT), opcional.

    Returns:
        Evaluación del estrés hídrico con nivel y detalles mensuales.
    """
    # Agrupar precipitación por mes
    monthly_precip: Dict[int, List[float]] = {}
    for date_str, val in precip_data.items():
        if val is None:
            continue
        try:
            month = int(date_str[4:6])
            monthly_precip.setdefault(month, []).append(val)
        except (ValueError, IndexError):
            continue

    # Calcular precipitación mensual acumulada (promedio diario × ~30)
    monthly_totals: Dict[int, float] = {}
    for m, vals in monthly_precip.items():
        monthly_totals[m] = round(sum(vals), 1)

    # Meses con déficit hídrico (< 30 mm acumulados es muy seco)
    dry_months = [m for m, total in monthly_totals.items() if total < 30]
    wet_months = [m for m, total in monthly_totals.items() if total > 150]

    # Humedad del suelo (si disponible)
    soil_stress_months: List[int] = []
    if evap_data:
        monthly_gwet: Dict[int, List[float]] = {}
        for date_str, val in evap_data.items():
            if val is None:
                continue
            try:
                month = int(date_str[4:6])
                monthly_gwet.setdefault(month, []).append(val)
            except (ValueError, IndexError):
                continue

        for m, vals in monthly_gwet.items():
            avg = sum(vals) / len(vals)
            if avg < 0.3:  # Suelo seco si la humedad radicular es baja
                soil_stress_months.append(m)

    # Precipitación total del período
    total_precip = sum(monthly_totals.values())
    num_months = len(monthly_totals) if monthly_totals else 1
    avg_monthly = round(total_precip / num_months, 1)

    # Clasificación
    if avg_monthly < 30:
        nivel = "severo"
        descripcion = (
            f"Precipitación promedio mensual de solo {avg_monthly} mm. "
            "Se requieren cultivos altamente tolerantes a la sequía o riego suplementario."
        )
    elif avg_monthly < 60:
        nivel = "alto"
        descripcion = (
            f"Precipitación promedio mensual de {avg_monthly} mm. "
            "Estrés hídrico significativo. Considere técnicas de conservación de agua."
        )
    elif avg_monthly < 100:
        nivel = "moderado"
        descripcion = (
            f"Precipitación promedio mensual de {avg_monthly} mm. "
            "Condiciones aceptables, pero algunos cultivos pueden requerir riego."
        )
    else:
        nivel = "bajo"
        descripcion = (
            f"Precipitación promedio mensual de {avg_monthly} mm. "
            "Buena disponibilidad hídrica para la mayoría de cultivos."
        )

    return {
        "nivel_estres": nivel,
        "descripcion": descripcion,
        "precipitacion_total_mm": round(total_precip, 1),
        "precipitacion_mensual_promedio_mm": avg_monthly,
        "meses_secos": sorted(dry_months),
        "meses_humedos": sorted(wet_months),
        "meses_estres_suelo": sorted(soil_stress_months),
        "precipitacion_mensual": monthly_totals,
    }
