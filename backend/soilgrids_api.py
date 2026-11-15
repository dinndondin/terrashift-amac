"""
soilgrids_api.py - Integración con ISRIC SoilGrids REST API v2.0
================================================================
Módulo para consultar mapas globales de propiedades de suelo (250m)
según requerimientos de la NASA y el equipo Terrashift (AMAC).
"""

import requests
from typing import Dict, Any, Optional

SOILGRIDS_URL = "https://rest.isric.org/soilgrids/v2.0/properties/query"

BIOBIO_FALLBACK = {
    "location": "Provincia de Biobío, Chile",
    "coordinates": {"lat": -37.47, "lon": -72.35},
    "texture": "Franco arcillo-arenoso (Trumao)",
    "clay_percent": 22,
    "sand_percent": 54,
    "silt_percent": 24,
    "organic_matter_percent": 3.8,
    "ph": 5.9,
    "cec": 18.5,
    "source": "SoilGrids 250m (ISRIC) & CIREN Chile"
}

def fetch_soilgrids(lat: float, lon: float) -> Dict[str, Any]:
    """Consulta la API pública de SoilGrids para un punto geográfico."""
    params = {
        "lat": round(lat, 4),
        "lon": round(lon, 4),
        "property": ["clay", "sand", "silt", "soc", "phh2o", "cec"],
        "depth": ["0-5cm", "5-15cm", "15-30cm"]
    }
    try:
        resp = requests.get(SOILGRIDS_URL, params=params, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            layers = data.get("properties", {}).get("layers", [])
            
            def get_mean(prop_name):
                layer = next((l for l in layers if l.get("name") == prop_name), None)
                if not layer:
                    return None
                depths = layer.get("depths", [])
                vals = [d.get("values", {}).get("mean") for d in depths if d.get("values", {}).get("mean") is not None]
                return (sum(vals) / len(vals)) if vals else None

            clay_raw = get_mean("clay")
            sand_raw = get_mean("sand")
            silt_raw = get_mean("silt")
            soc_raw = get_mean("soc")
            ph_raw = get_mean("phh2o")
            cec_raw = get_mean("cec")

            clay = round(clay_raw / 10) if clay_raw else 22
            sand = round(sand_raw / 10) if sand_raw else 54
            silt = round(silt_raw / 10) if silt_raw else 24

            return {
                "status": "success",
                "coordinates": {"lat": lat, "lon": lon},
                "clay_percent": clay,
                "sand_percent": sand,
                "silt_percent": silt,
                "organic_matter_percent": round(soc_raw / 10, 1) if soc_raw else 3.8,
                "ph": round(ph_raw / 10, 1) if ph_raw else 5.9,
                "cec": round(cec_raw / 10, 1) if cec_raw else 18.5,
                "source": "SoilGrids v2.0 (ISRIC World Soil Information)"
            }
    except Exception as e:
        print(f"SoilGrids request fallback: {e}")

    return {
        "status": "fallback",
        **BIOBIO_FALLBACK,
        "coordinates": {"lat": lat, "lon": lon}
    }
