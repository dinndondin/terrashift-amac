"""Compatibilidad: implementación organizada dentro de amac."""

from amac.reportes.acciones import (
    _section_action_items,
)
from amac.reportes.alertas import (
    _section_alerts,
)
from amac.reportes.clima import (
    _section_climate,
)
from amac.reportes.estilos import (
    _CSS,
)
from amac.reportes.formato import (
    _format_date,
    _score_color_class,
)
from amac.reportes.generador import (
    generate_report,
)
from amac.reportes.resumen import (
    _section_executive_summary,
)
from amac.reportes.rotaciones import (
    _section_rotation_recommendations,
)
from amac.reportes.suelo import (
    _section_soil_health,
)
