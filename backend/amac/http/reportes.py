"""Rutas HTTP: reportes."""

from flask import Blueprint
from flask import request
from flask import jsonify
from flask import Response
from nasa_api import fetch_climate_data
from rotation_engine import generate_rotation_strategies
from report_generator import generate_report

bp = Blueprint("reportes", __name__)


@bp.route("/api/report", methods=["POST"])
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
