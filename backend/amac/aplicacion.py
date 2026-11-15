"""Construcción de la aplicación Flask sin iniciar el servidor al importar."""

from flask import Flask
from flask_cors import CORS

from amac.http.salud import bp as salud_bp
from amac.http.clima import bp as clima_bp
from amac.http.cultivos import bp as cultivos_bp
from amac.http.analisis import bp as analisis_bp
from amac.http.reportes import bp as reportes_bp
from amac.http.regional import bp as regional_bp
from amac.http.suelos import bp as suelos_bp


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(salud_bp)
    app.register_blueprint(clima_bp)
    app.register_blueprint(cultivos_bp)
    app.register_blueprint(analisis_bp)
    app.register_blueprint(reportes_bp)
    app.register_blueprint(regional_bp)
    app.register_blueprint(suelos_bp)
    return app
