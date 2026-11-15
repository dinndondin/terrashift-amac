"""
app.py - Servidor REST API Flask para AMAC
===========================================
Asistente de Monitoreo Agrícola Climático - NASA Space Apps Challenge 2026.
Provee endpoints para datos satelitales NASA POWER, catálogo agronómico,
evaluación de rotaciones y generación de reportes periódicos para agricultores.
"""

import os
import sys
from datetime import datetime
from flask import Flask, request, jsonify, Response
from flask_cors import CORS

from nasa_api import (
    fetch_climate_data,
    fetch_monthly_averages,
    assess_frost_risk,
    assess_water_stress,
    calculate_climate_trends,
)
from crop_database import (
    get_all_crops,
    get_crop,
    get_compatible_crops,
    get_crops_by_category,
)
from rotation_engine import (
    generate_rotation_strategies,
    score_rotation,
    identify_fallow_windows,
)
from report_generator import generate_report
from soilgrids_api import fetch_soilgrids
from regional_api import get_biobio_summary

app = Flask(__name__)
# Habilitar CORS para permitir peticiones desde el frontend en cualquier puerto/origen
CORS(app)


# --------------------------------------------------------------------------- #
#  Endpoints de Salud y Utilidades
# --------------------------------------------------------------------------- #

@app.route("/api/health", methods=["GET"])
def health():
    """Verificación de estado del servicio."""
    return jsonify({
        "status": "healthy",
        "service": "AMAC API - Asistente de Monitoreo Agrícola Climático",
        "nasa_source": "NASA POWER API (Agroclimatology Community)",
        "version": "versión 1 2026",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })


# --------------------------------------------------------------------------- #
#  Endpoints de Datos Satelitales NASA POWER
# --------------------------------------------------------------------------- #

@app.route("/api/climate-data", methods=["POST"])
def get_climate_data():
    """
    Obtiene datos agroclimáticos históricos de NASA POWER para una ubicación dada.
    Body JSON:
        - lat (float): Latitud (-90 a 90)
        - lon (float): Longitud (-180 a 180)
        - start (str, opcional): YYYYMMDD (def: hace 1 año)
        - end (str, opcional): YYYYMMDD (def: hoy)
        - params (list[str], opcional): Lista de parámetros NASA POWER
    """
    body = request.get_json(silent=True) or {}
    lat = body.get("lat")
    lon = body.get("lon")

    if lat is None or lon is None:
        return jsonify({"error": "Parámetros 'lat' y 'lon' son requeridos."}), 400

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return jsonify({"error": "'lat' y 'lon' deben ser números flotantes."}), 400

    start_date = body.get("start")
    end_date = body.get("end")
    params = body.get("params")

    data = fetch_climate_data(
        lat=lat,
        lon=lon,
        start_date=start_date,
        end_date=end_date,
        params=params,
    )

    if not data or not data.get("parameters"):
        return jsonify({
            "status": "warning",
            "message": "No se pudieron obtener datos satelitales en vivo de NASA POWER. Verifique coordenadas o conexión.",
            "data": data or {}
        }), 200

    return jsonify({
        "status": "success",
        "data": data
    })


@app.route("/api/climate-climatology", methods=["POST"])
def get_climate_climatology():
    """
    Obtiene promedios mensuales multianuales (climatología) de NASA POWER.
    """
    body = request.get_json(silent=True) or {}
    lat = body.get("lat")
    lon = body.get("lon")

    if lat is None or lon is None:
        return jsonify({"error": "Parámetros 'lat' y 'lon' son requeridos."}), 400

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return jsonify({"error": "'lat' y 'lon' deben ser válidos."}), 400

    data = fetch_monthly_averages(lat=lat, lon=lon)
    return jsonify({
        "status": "success",
        "data": data
    })


# --------------------------------------------------------------------------- #
#  Endpoints de Base de Datos de Cultivos
# --------------------------------------------------------------------------- #

@app.route("/api/crops", methods=["GET"])
def list_crops():
    """Retorna el catálogo agronómico completo con sus 26 cultivos y atributos."""
    category = request.args.get("category")
    if category:
        crops = get_crops_by_category(category)
    else:
        crops = get_all_crops()

    return jsonify({
        "status": "success",
        "total": len(crops),
        "crops": crops
    })


@app.route("/api/crops/<crop_name>", methods=["GET"])
def get_single_crop(crop_name):
    """Retorna ficha técnica agronómica de un cultivo específico."""
    crop = get_crop(crop_name)
    if not crop:
        return jsonify({"error": f"Cultivo '{crop_name}' no encontrado en la base de datos."}), 404
    return jsonify({
        "status": "success",
        "crop": crop
    })


# --------------------------------------------------------------------------- #
#  Motor de Análisis y Recomendación de Rotaciones
# --------------------------------------------------------------------------- #

@app.route("/api/rotation-strategies", methods=["POST"])
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


@app.route("/api/analyze", methods=["POST"])
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


# --------------------------------------------------------------------------- #
#  Endpoints de Generación de Reportes Periódicos
# --------------------------------------------------------------------------- #

@app.route("/api/report", methods=["POST"])
def build_report():
    """
    Genera un reporte periódico profesional (Diario, Semanal, Mensual).
    Body JSON:
        - report_type: 'daily', 'weekly', 'monthly'
        - location: {"lat": float, "lon": float, "name": str}
        - soil_type: str
        - current_crops: list[str]
        - priorities: dict
        - date_range: {"start": "YYYYMMDD", "end": "YYYYMMDD"}
    """
    body = request.get_json(silent=True) or {}
    report_type = body.get("report_type", "weekly")
    location = body.get("location", {"lat": -34.6037, "lon": -58.3816, "name": "Finca AMAC"})
    soil_type = body.get("soil_type", "franco")
    current_crops = body.get("current_crops", ["Soja", "Maíz"])
    priorities = body.get("priorities", {})
    date_range = body.get("date_range")

    # Clima
    lat = location.get("lat", -34.6037)
    lon = location.get("lon", -58.3816)
    climate_data = fetch_climate_data(lat, lon)

    # Estrategias
    rotation_data = generate_rotation_strategies(
        location_data=location,
        climate_data=climate_data,
        current_crops=current_crops,
        soil_type=soil_type,
        farmer_priorities=priorities,
    )

    # Generación de HTML
    report_html = generate_report(
        report_type=report_type,
        location=location,
        climate_data=climate_data,
        rotation_data=rotation_data,
        date_range=date_range,
    )

    # Si se pide formato JSON o HTML
    format_type = request.args.get("format", "html")
    if format_type == "json":
        return jsonify({
            "status": "success",
            "report_type": report_type,
            "html": report_html
        })
    else:
        return Response(report_html, mimetype="text/html")


# --------------------------------------------------------------------------- #
#  Endpoints de API Regional B2B y SoilGrids (ISRIC)
# --------------------------------------------------------------------------- #

@app.route("/api/v1/regional/biobio", methods=["GET"])
def get_regional_biobio():
    """Endpoint B2B para INDAP, PRODESAL, Municipalidades y Cooperativas del Biobío."""
    return jsonify(get_biobio_summary())


@app.route("/api/v1/soilgrids", methods=["POST", "GET"])
def get_soilgrids_data():
    """Consulta de propiedades del suelo desde SoilGrids REST v2.0."""
    if request.method == "POST":
        body = request.get_json(silent=True) or {}
        lat = body.get("lat", -37.47)
        lon = body.get("lon", -72.35)
    else:
        lat = float(request.args.get("lat", -37.47))
        lon = float(request.args.get("lon", -72.35))

    data = fetch_soilgrids(lat, lon)
    return jsonify(data)


# --------------------------------------------------------------------------- #
#  Punto de Entrada
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 AMAC Backend corriendo en http://localhost:{port}")
    print("📡 Integrado con NASA POWER API & Base Agronómica")
    app.run(host="0.0.0.0", port=port, debug=False)
