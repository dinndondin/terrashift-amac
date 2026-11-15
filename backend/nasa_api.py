"""
nasa_api.py - Integración con la API NASA POWER
=================================================
Módulo encargado de obtener datos climáticos históricos y climatológicos
desde la API NASA POWER (https://power.larc.nasa.gov/).

Parámetros utilizados:
    - T2M: Temperatura promedio a 2m (°C)
    - T2M_MAX: Temperatura máxima a 2m (°C)
    - T2M_MIN: Temperatura mínima a 2m (°C)
    - PRECTOTCORR: Precipitación corregida (mm/día)
    - RH2M: Humedad relativa a 2m (%)
    - GWETROOT: Humedad del suelo en zona radicular (fracción 0-1)
    - ALLSKY_SFC_SW_DWN: Radiación solar incidente (MJ/m²/día)
    - WS2M: Velocidad del viento a 2m (m/s)
    - T2MDEW: Punto de rocío a 2m (°C)
"""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime

# --------------------------------------------------------------------------- #
#  Constantes
# --------------------------------------------------------------------------- #

BASE_URL = "https://power.larc.nasa.gov/api/temporal"

# Parámetros climáticos que solicitamos a NASA POWER
DEFAULT_PARAMS = [
    "T2M", "T2M_MAX", "T2M_MIN",
    "PRECTOTCORR",
    "RH2M",
    "GWETROOT",
    "ALLSKY_SFC_SW_DWN",
    "WS2M",
    "T2MDEW",
]

# Valor centinela que NASA POWER usa para datos faltantes
_FILL_VALUE = -999.0


# --------------------------------------------------------------------------- #
#  Funciones auxiliares
# --------------------------------------------------------------------------- #

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


# --------------------------------------------------------------------------- #
#  Obtención de datos
# --------------------------------------------------------------------------- #

def fetch_climate_data(
    lat: float,
    lon: float,
    start_date: str,
    end_date: str,
    params: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Obtiene datos climáticos diarios de NASA POWER para un punto geográfico.

    Args:
        lat: Latitud del punto (-90 a 90).
        lon: Longitud del punto (-180 a 180).
        start_date: Fecha de inicio en formato 'YYYYMMDD'.
        end_date: Fecha de fin en formato 'YYYYMMDD'.
        params: Lista de parámetros NASA POWER (usa DEFAULT_PARAMS si no se indica).

    Returns:
        Diccionario con:
            - parameters: datos diarios por parámetro
            - summary: resumen estadístico
            - metadata: información de la solicitud

    Raises:
        ValueError: Si las coordenadas o fechas son inválidas.
        ConnectionError: Si no se puede contactar la API.
    """
    if params is None:
        params = DEFAULT_PARAMS

    # Validaciones básicas
    if not (-90 <= lat <= 90):
        raise ValueError(f"Latitud fuera de rango: {lat}")
    if not (-180 <= lon <= 180):
        raise ValueError(f"Longitud fuera de rango: {lon}")

    params_str = ",".join(params)
    url = (
        f"{BASE_URL}/daily/point"
        f"?parameters={params_str}"
        f"&community=AG"
        f"&longitude={lon}"
        f"&latitude={lat}"
        f"&start={start_date}"
        f"&end={end_date}"
        f"&format=JSON"
    )

    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise ConnectionError(
            "La solicitud a NASA POWER excedió el tiempo de espera. "
            "Intente de nuevo más tarde."
        )
    except requests.exceptions.HTTPError as exc:
        raise ConnectionError(
            f"Error HTTP al contactar NASA POWER: {exc.response.status_code} - "
            f"{exc.response.text[:300]}"
        )
    except requests.exceptions.RequestException as exc:
        raise ConnectionError(f"No se pudo contactar la API NASA POWER: {exc}")

    raw = response.json()

    # Extraer propiedades de la respuesta
    properties = raw.get("properties", {})
    parameter_data = properties.get("parameter", {})

    # Limpiar valores centinela en cada parámetro
    cleaned: Dict[str, Dict[str, Optional[float]]] = {}
    for param_name, daily_values in parameter_data.items():
        cleaned[param_name] = _clean_values(daily_values)

    # Generar resumen estadístico
    summary = _build_summary(cleaned)

    return {
        "parameters": cleaned,
        "summary": summary,
        "metadata": {
            "lat": lat,
            "lon": lon,
            "start_date": start_date,
            "end_date": end_date,
            "source": "NASA POWER API v2",
            "requested_params": params,
            "fetched_at": datetime.utcnow().isoformat() + "Z",
        },
    }


def fetch_monthly_averages(
    lat: float,
    lon: float,
    params: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Obtiene promedios mensuales climatológicos (largo plazo) de NASA POWER.

    Args:
        lat: Latitud del punto.
        lon: Longitud del punto.
        params: Lista de parámetros (usa DEFAULT_PARAMS si no se indica).

    Returns:
        Diccionario con promedios mensuales por parámetro y un resumen anual.
    """
    if params is None:
        params = DEFAULT_PARAMS

    params_str = ",".join(params)
    url = (
        f"{BASE_URL}/climatology/point"
        f"?parameters={params_str}"
        f"&community=AG"
        f"&longitude={lon}"
        f"&latitude={lat}"
        f"&format=JSON"
    )

    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise ConnectionError(
            f"No se pudieron obtener promedios climatológicos: {exc}"
        )

    raw = response.json()
    properties = raw.get("properties", {})
    parameter_data = properties.get("parameter", {})

    # Organizar datos por mes (las claves son "JAN", "FEB", … o "1", "2", …)
    months_map = {
        "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4,
        "MAY": 5, "JUN": 6, "JUL": 7, "AUG": 8,
        "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12,
    }

    monthly: Dict[str, Dict[int, Optional[float]]] = {}
    for param_name, month_values in parameter_data.items():
        monthly[param_name] = {}
        for key, val in month_values.items():
            month_num = months_map.get(key.upper())
            if month_num is not None:
                monthly[param_name][month_num] = val if val != _FILL_VALUE else None

    return {
        "monthly_averages": monthly,
        "metadata": {
            "lat": lat,
            "lon": lon,
            "source": "NASA POWER Climatology API v2",
            "fetched_at": datetime.utcnow().isoformat() + "Z",
        },
    }


# --------------------------------------------------------------------------- #
#  Análisis de datos climáticos
# --------------------------------------------------------------------------- #

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
