"""Rutas HTTP: clima."""

from flask import Blueprint
from flask import request
from flask import jsonify
from nasa_api import fetch_climate_data
from nasa_api import fetch_monthly_averages

bp = Blueprint("clima", __name__)


@bp.route("/api/climate-data", methods=["POST"])
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


@bp.route("/api/climate-climatology", methods=["POST"])
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
