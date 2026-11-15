"""Componente amac.rotaciones.config; lógica extraída de rotation_engine.py."""

from typing import Dict


MONTH_NAMES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
}


VALID_SOIL_TYPES = [
    "arcilloso", "arenoso", "limoso", "franco",
    "franco-arcilloso", "franco-arenoso",
]


DEFAULT_PRIORITIES: Dict[str, float] = {
    "water_conservation": 0.5,
    "soil_health": 0.5,
    "economic_return": 0.5,
    "pest_management": 0.5,
    "erosion_control": 0.5,
    "nitrogen_fixation": 0.5,
}


_LEVEL_MAP = {"bajo": 1, "medio": 2, "alto": 3}


_DEPTH_MAP = {"superficial": 1, "media": 2, "profunda": 3}
