"""Componente amac.regional.perfiles; lógica extraída de regional_api.py."""




BIOBIO_REGIONAL_PROFILE = {
    "region_id": "CL-BI",
    "name": "Región del Biobío",
    "country": "Chile",
    "target_focus": "Provincia de Biobío (Cuna cerealera: 45.7% de trigo candeal nacional)",
    "institutional_partners": [
        "INDAP Región del Biobío (Plan Regional 2023-2026: 11.810 usuarios)",
        "PRODESAL (58% de cobertura comunal)",
        "PDTI (35.2% comunidades rurales)",
        "SAT (4.5% asistencia especializada)"
    ],
    "comunas_monitoreadas": [
        {
            "comuna": "Los Ángeles",
            "lat": -37.47, "lon": -72.35,
            "soilgrids_texture": "Franco arcillo-arenoso (Trumao)",
            "soil_ph": 5.9,
            "soil_organic_matter": "3.8%",
            "nasa_climate": {"temp_media": "14.2°C", "precip_anual": "1050 mm"},
            "estres_hidrico": "Moderado (Déficit en enero-febrero)",
            "rotacion_recomendada": "Trigo Candeal -> Vicia villosa (cobertura fijadora N) -> Maíz"
        },
        {
            "comuna": "Mulchén",
            "lat": -37.72, "lon": -72.24,
            "soilgrids_texture": "Franco volcánico aluvial",
            "soil_ph": 5.8,
            "soil_organic_matter": "4.2%",
            "nasa_climate": {"temp_media": "13.8°C", "precip_anual": "1120 mm"},
            "estres_hidrico": "Bajo",
            "rotacion_recomendada": "Trigo Harinero -> Lenteja o Vicia -> Cebada"
        },
        {
            "comuna": "Cabrero / Yumbel",
            "lat": -37.03, "lon": -72.40,
            "soilgrids_texture": "Areno-francoso (Arenales)",
            "soil_ph": 6.2,
            "soil_organic_matter": "2.4%",
            "nasa_climate": {"temp_media": "14.6°C", "precip_anual": "980 mm"},
            "estres_hidrico": "Alto (Baja retención de agua)",
            "rotacion_recomendada": "Sorgo forrajero -> Centeno cobertura -> Girasol (Raíces profundas)"
        },
        {
            "comuna": "Santa Bárbara / Quilaco",
            "lat": -37.67, "lon": -72.02,
            "soilgrids_texture": "Franco trumao precordillerano",
            "soil_ph": 5.6,
            "soil_organic_matter": "5.1%",
            "nasa_climate": {"temp_media": "13.1°C", "precip_anual": "1280 mm"},
            "estres_hidrico": "Moderado (Riesgo heladas tardías)",
            "rotacion_recomendada": "Avena forrajera -> Vicia -> Trigo"
        }
    ]
}
