"""Compatibilidad: implementación organizada dentro de amac."""

from amac.nasa.cliente import (
    fetch_climate_data,
    fetch_monthly_averages,
)
from amac.nasa.config import (
    BASE_URL,
    DEFAULT_PARAMS,
    _FILL_VALUE,
)
from amac.nasa.estadisticas import (
    _clean_values,
    _safe_mean,
    _safe_min,
    _safe_max,
    _build_summary,
)
from amac.nasa.riesgos import (
    assess_frost_risk,
    assess_water_stress,
)
from amac.nasa.tendencias import (
    calculate_climate_trends,
    _generate_trend_observations,
)
