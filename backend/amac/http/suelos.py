"""Rutas HTTP: suelos."""

from flask import Blueprint
from flask import request
from flask import jsonify
from soilgrids_api import fetch_soilgrids

bp = Blueprint("suelos", __name__)


@bp.route("/api/v1/soilgrids", methods=["POST", "GET"])
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
