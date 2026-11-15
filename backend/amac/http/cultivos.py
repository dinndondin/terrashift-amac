"""Rutas HTTP: cultivos."""

from flask import Blueprint
from flask import request
from flask import jsonify
from crop_database import get_all_crops
from crop_database import get_crop
from crop_database import get_crops_by_category

bp = Blueprint("cultivos", __name__)


@bp.route("/api/crops", methods=["GET"])
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


@bp.route("/api/crops/<crop_name>", methods=["GET"])
def get_single_crop(crop_name):
    """Retorna ficha técnica agronómica de un cultivo específico."""
    crop = get_crop(crop_name)
    if not crop:
        return jsonify({"error": f"Cultivo '{crop_name}' no encontrado en la base de datos."}), 404
    return jsonify({
        "status": "success",
        "crop": crop
    })
