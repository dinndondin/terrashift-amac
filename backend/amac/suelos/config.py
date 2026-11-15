"""Componente amac.suelos.config; lógica extraída de soilgrids_api.py."""




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
