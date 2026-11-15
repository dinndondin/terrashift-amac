"""Componente amac.reportes.generador; lógica extraída de report_generator.py."""

from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from amac.reportes.acciones import _section_action_items
from amac.reportes.alertas import _section_alerts
from amac.reportes.clima import _section_climate
from amac.reportes.estilos import _CSS
from amac.reportes.formato import _format_date
from amac.reportes.resumen import _section_executive_summary
from amac.reportes.rotaciones import _section_rotation_recommendations
from amac.reportes.suelo import _section_soil_health


def generate_report(
    report_type: str,
    location: Dict[str, Any],
    climate_data: Optional[Dict[str, Any]],
    rotation_data: Optional[List[Dict[str, Any]]],
    date_range: Optional[Dict[str, str]] = None,
) -> str:
    """
    Genera un reporte HTML completo para el agricultor.

    Args:
        report_type: 'daily', 'weekly' o 'monthly'.
        location: {"lat": float, "lon": float, "name": str (opcional)}.
        climate_data: Resultado de fetch_climate_data().
        rotation_data: Lista de estrategias de rotación.
        date_range: {"start": "YYYYMMDD", "end": "YYYYMMDD"} (opcional).

    Returns:
        String HTML del reporte completo.
    """
    type_labels = {
        "daily": "Reporte Diario",
        "weekly": "Reporte Semanal",
        "monthly": "Reporte Mensual",
    }
    report_title = type_labels.get(report_type, "Reporte")
    now = datetime.utcnow()

    location_name = location.get("name", f"Lat {location.get('lat', '?')}, Lon {location.get('lon', '?')}")

    # Construir secciones
    sections: List[str] = []

    # 1. Resumen ejecutivo
    sections.append(_section_executive_summary(report_type, climate_data, rotation_data))

    # 2. Condiciones climáticas
    if climate_data:
        sections.append(_section_climate(climate_data, report_type))

    # 3. Indicadores de salud del suelo
    sections.append(_section_soil_health(climate_data))

    # 4. Recomendaciones de rotación (solo weekly/monthly)
    if report_type in ("weekly", "monthly") and rotation_data:
        sections.append(_section_rotation_recommendations(rotation_data))

    # 5. Alertas y advertencias
    sections.append(_section_alerts(climate_data, rotation_data))

    # 6. Acciones para el agricultor
    sections.append(_section_action_items(report_type, climate_data, rotation_data))

    # Ensamblar HTML
    date_range_str = ""
    if date_range:
        start = date_range.get("start", "")
        end = date_range.get("end", "")
        if start and end:
            date_range_str = f" | Período: {_format_date(start)} – {_format_date(end)}"

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AMAC - {report_title}</title>
    {_CSS}
</head>
<body>
    <div class="report-container">
        <div class="header">
            <h1>🌾 AMAC - {report_title}</h1>
            <div class="subtitle">Asistente de Monitoreo Agrícola Climático</div>
            <div class="meta">
                📍 {location_name}{date_range_str}<br>
                📅 Generado: {now.strftime('%d/%m/%Y %H:%M')} UTC
            </div>
        </div>
        <div class="content">
            {''.join(sections)}
        </div>
        <div class="footer">
            Reporte generado por AMAC · Datos climáticos: NASA POWER API ·
            NASA Space Apps Challenge 2026 · versión 1 2026<br>
            Este reporte es una herramienta de apoyo a la decisión. Consulte
            siempre con un profesional agrónomo local.
        </div>
    </div>
</body>
</html>"""

    return html
