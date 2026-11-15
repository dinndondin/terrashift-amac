"""Componente amac.nasa.cliente; lógica extraída de nasa_api.py."""

from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
import requests
from amac.nasa.config import BASE_URL, DEFAULT_PARAMS, _FILL_VALUE
from amac.nasa.estadisticas import _build_summary, _clean_values


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
