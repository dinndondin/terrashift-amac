"""Rutas HTTP: salud."""

from flask import Blueprint
from datetime import datetime
from flask import jsonify

bp = Blueprint("salud", __name__)


@bp.route("/api/health", methods=["GET"])
def health():
    """Verificación de estado del servicio."""
    return jsonify({
        "status": "healthy",
        "service": "AMAC API - Asistente de Monitoreo Agrícola Climático",
        "nasa_source": "NASA POWER API (Agroclimatology Community)",
        "version": "versión 1 2026",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })
