"""Rutas HTTP: analisis."""

from flask import Blueprint
from flask import request
from flask import jsonify
from nasa_api import fetch_climate_data
from nasa_api import assess_frost_risk
from nasa_api import assess_water_stress
from nasa_api import calculate_climate_trends
from rotation_engine import generate_rotation_strategies
from rotation_engine import identify_fallow_windows

bp = Blueprint("analisis", __name__)


@bp.route("/api/rotation-strategies", methods=["POST"])
def calculate_rotations():
    """
    Genera y compara al menos 3 estrategias de rotación personalizadas.
    Body JSON:
        - location: {"lat": float, "lon": float, "name": str}
        - current_crops: list[str] (cultivos actuales, ej: ["Soja", "Maíz"])
        - soil_type: str ("arcilloso", "arenoso", "limoso", "franco", etc.)
        - priorities: dict con pesos (water_conservation, soil_health, etc.)
        - climate_data: dict opcional de datos NASA previos
    """
    body = request.get_json(silent=True) or {}
    location = body.get("location", {"lat": -34.6037, "lon": -58.3816, "name": "Buenos Aires"})
    current_crops = body.get("current_crops", ["Soja", "Maíz"])
    soil_type = body.get("soil_type", "franco")
    priorities = body.get("priorities", {})
    climate_data = body.get("climate_data")

    # Si no se pasó climate_data, intentamos obtenerlo de NASA POWER
    if not climate_data and "lat" in location and "lon" in location:
        climate_data = fetch_climate_data(location["lat"], location["lon"])

    strategies = generate_rotation_strategies(
        location_data=location,
        climate_data=climate_data,
        current_crops=current_crops,
        soil_type=soil_type,
        farmer_priorities=priorities,
    )

    fallow_windows = identify_fallow_windows(climate_data, current_crops)

    return jsonify({
        "status": "success",
        "strategies": strategies,
        "fallow_windows": fallow_windows,
        "soil_type": soil_type,
        "current_crops": current_crops
    })


@bp.route("/api/analyze", methods=["POST"])
def analyze_farm():
    """
    Análisis integral 360° de la finca:
    Combina Clima NASA + Evaluación Agronómica + 3+ Estrategias de Rotación + Alertas.
    """
    body = request.get_json(silent=True) or {}
    lat = body.get("lat", -34.6037)
    lon = body.get("lon", -58.3816)
    soil_type = body.get("soil_type", "franco")
    current_crops = body.get("current_crops", ["Soja", "Maíz"])
    priorities = body.get("priorities", {})
    farm_name = body.get("name", "Finca Demostración")

    location = {"lat": lat, "lon": lon, "name": farm_name}

    # 1. Obtener datos satelitales NASA POWER
    climate_data = fetch_climate_data(lat, lon)

    # 2. Evaluación de riesgos agroclimáticos
    frost_risk = assess_frost_risk(climate_data) if climate_data else {"risk_level": "desconocido"}
    water_stress = assess_water_stress(climate_data) if climate_data else {"stress_level": "desconocido"}
    trends = calculate_climate_trends(climate_data) if climate_data else {}

    # 3. Generar estrategias de rotación comparativas
    strategies = generate_rotation_strategies(
        location_data=location,
        climate_data=climate_data,
        current_crops=current_crops,
        soil_type=soil_type,
        farmer_priorities=priorities,
    )

    # 4. Detectar ventanas de barbecho (suelo descubierto)
    fallow = identify_fallow_windows(climate_data, current_crops)

    return jsonify({
        "status": "success",
        "location": location,
        "climate_summary": climate_data.get("summary") if climate_data else {},
        "agro_risks": {
            "frost_risk": frost_risk,
            "water_stress": water_stress,
            "trends": trends
        },
        "strategies": strategies,
        "fallow_windows": fallow,
        "soil_type": soil_type
    })
