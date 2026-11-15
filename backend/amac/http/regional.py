"""Rutas HTTP: regional."""

from flask import Blueprint
from flask import jsonify
from regional_api import get_biobio_summary

bp = Blueprint("regional", __name__)


@bp.route("/api/v1/regional/biobio", methods=["GET"])
def get_regional_biobio():
    """Endpoint B2B para INDAP, PRODESAL, Municipalidades y Cooperativas del Biobío."""
    return jsonify(get_biobio_summary())
