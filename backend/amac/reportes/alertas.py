"""Componente amac.reportes.alertas; lógica extraída de report_generator.py."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional


def _section_alerts(
    climate_data: Optional[Dict[str, Any]],
    rotation_data: Optional[List[Dict[str, Any]]],
) -> str:
    """Genera la sección de alertas y advertencias."""
    alerts: List[str] = []

    if climate_data:
        s = climate_data.get("summary", {})

        # Alerta de helada
        t2m_min = s.get("T2M_MIN", {})
        min_temp = t2m_min.get("minimo")
        if min_temp is not None and min_temp < 0:
            alerts.append(
                f'<div class="alert-box alert-danger">'
                f'❄️ <strong>Alerta de Helada:</strong> Se registraron temperaturas de '
                f'{min_temp}°C. Proteja cultivos sensibles al frío.'
                f'</div>'
            )

        # Alerta de estrés hídrico
        precip = s.get("PRECTOTCORR", {})
        avg_precip = precip.get("promedio")
        if avg_precip is not None and avg_precip < 1.5:
            alerts.append(
                f'<div class="alert-box alert-warning">'
                f'🏜️ <strong>Estrés Hídrico:</strong> Precipitación promedio de solo '
                f'{avg_precip} mm/día. Considere riego suplementario.'
                f'</div>'
            )

        # Alerta de exceso de agua
        if avg_precip is not None and avg_precip > 10:
            alerts.append(
                f'<div class="alert-box alert-warning">'
                f'🌊 <strong>Exceso de Agua:</strong> Precipitación promedio de '
                f'{avg_precip} mm/día. Riesgo de encharcamiento y enfermedades fúngicas.'
                f'</div>'
            )

        # Alerta de temperatura extrema
        t2m_max = s.get("T2M_MAX", {})
        max_temp = t2m_max.get("maximo")
        if max_temp is not None and max_temp > 40:
            alerts.append(
                f'<div class="alert-box alert-danger">'
                f'🔥 <strong>Calor Extremo:</strong> Temperaturas máximas de '
                f'{max_temp}°C registradas. Riesgo de estrés térmico en cultivos.'
                f'</div>'
            )

        # Alerta de viento fuerte
        ws = s.get("WS2M", {})
        max_wind = ws.get("maximo")
        if max_wind is not None and max_wind > 8:
            alerts.append(
                f'<div class="alert-box alert-warning">'
                f'💨 <strong>Viento Fuerte:</strong> Ráfagas de hasta '
                f'{max_wind} m/s registradas. Riesgo de daño mecánico y erosión eólica.'
                f'</div>'
            )

    if not alerts:
        alerts.append(
            '<div class="alert-box alert-success">'
            '✅ No se detectaron alertas críticas para el período analizado.'
            '</div>'
        )

    return f"""
    <div class="section">
        <h2>🔔 Alertas y Advertencias</h2>
        {''.join(alerts)}
    </div>
    """
