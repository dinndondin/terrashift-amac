"""Compatibilidad: implementación organizada dentro de amac."""

from amac.rotaciones.analisis import (
    _analyze_rotation,
    _gather_evidence,
    _identify_gaps,
)
from amac.rotaciones.calendario import (
    _recommend_periods,
    identify_fallow_windows,
)
from amac.rotaciones.config import (
    MONTH_NAMES,
    VALID_SOIL_TYPES,
    DEFAULT_PRIORITIES,
    _LEVEL_MAP,
    _DEPTH_MAP,
)
from amac.rotaciones.constructores import (
    _build_soil_health_rotation,
    _build_economic_rotation,
    _build_climate_resilient_rotation,
)
from amac.rotaciones.estrategias import (
    generate_rotation_strategies,
)
from amac.rotaciones.puntuacion import (
    _level_to_score,
    _normalize,
    _validate_priorities,
    score_rotation,
)
