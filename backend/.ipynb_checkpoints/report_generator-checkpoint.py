"""
report_generator.py - Generador de Reportes para AMAC
======================================================
Genera reportes HTML estructurados y legibles para el agricultor.

Tipos de reporte:
    - daily: Resumen diario de condiciones y alertas.
    - weekly: Resumen semanal con tendencias y acciones.
    - monthly: Reporte mensual completo con recomendaciones de rotación.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime

# --------------------------------------------------------------------------- #
#  Estilos CSS base
# --------------------------------------------------------------------------- #

_CSS = """
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        color: #333;
        background: #f5f7fa;
        padding: 20px;
    }
    .report-container {
        max-width: 900px;
        margin: 0 auto;
        background: #fff;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        overflow: hidden;
    }
    .header {
        background: linear-gradient(135deg, #1a7a3a 0%, #2d9b4e 100%);
        color: white;
        padding: 30px 40px;
    }
    .header h1 {
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .header .subtitle {
        font-size: 14px;
        opacity: 0.9;
    }
    .header .meta {
        margin-top: 15px;
        font-size: 13px;
        opacity: 0.8;
    }
    .content { padding: 30px 40px; }
    .section {
        margin-bottom: 30px;
        border-bottom: 1px solid #eee;
        padding-bottom: 25px;
    }
    .section:last-child { border-bottom: none; }
    .section h2 {
        color: #1a7a3a;
        font-size: 20px;
        margin-bottom: 15px;
        padding-bottom: 8px;
        border-bottom: 2px solid #e8f5e9;
    }
    .section h3 {
        color: #444;
        font-size: 16px;
        margin: 12px 0 8px 0;
    }
    .summary-box {
        background: #e8f5e9;
        border-left: 4px solid #1a7a3a;
        padding: 15px 20px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 15px;
    }
    .alert-box {
        padding: 12px 18px;
        border-radius: 8px;
        margin-bottom: 10px;
        font-size: 14px;
    }
    .alert-warning {
        background: #fff3e0;
        border-left: 4px solid #ff9800;
        color: #e65100;
    }
    .alert-danger {
        background: #ffebee;
        border-left: 4px solid #f44336;
        color: #c62828;
    }
    .alert-info {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
        color: #0d47a1;
    }
    .alert-success {
        background: #e8f5e9;
        border-left: 4px solid #4caf50;
        color: #1b5e20;
    }
    .data-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 12px;
        margin: 15px 0;
    }
    .data-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
    }
    .data-card .value {
        font-size: 24px;
        font-weight: 700;
        color: #1a7a3a;
    }
    .data-card .label {
        font-size: 12px;
        color: #666;
        margin-top: 4px;
    }
    .score-bar {
        width: 100%;
        height: 8px;
        background: #e0e0e0;
        border-radius: 4px;
        overflow: hidden;
        margin: 4px 0;
    }
    .score-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.3s;
    }
    .score-high { background: #4caf50; }
    .score-medium { background: #ff9800; }
    .score-low { background: #f44336; }
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0;
    }
    th, td {
        padding: 10px 12px;
        text-align: left;
        border-bottom: 1px solid #eee;
        font-size: 14px;
    }
    th {
        background: #f8f9fa;
        font-weight: 600;
        color: #555;
    }
    ul { padding-left: 20px; margin: 8px 0; }
    li { margin-bottom: 4px; font-size: 14px; }
    .footer {
        background: #f8f9fa;
        padding: 20px 40px;
        font-size: 12px;
        color: #888;
        text-align: center;
    }
    .action-item {
        display: flex;
        align-items: flex-start;
        padding: 10px 0;
        border-bottom: 1px dashed #e0e0e0;
    }
    .action-number {
        background: #1a7a3a;
        color: white;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 700;
        margin-right: 12px;
        flex-shrink: 0;
    }
</style>
"""


# --------------------------------------------------------------------------- #
#  Función principal
# --------------------------------------------------------------------------- #

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


# --------------------------------------------------------------------------- #
#  Secciones del reporte
# --------------------------------------------------------------------------- #

def _section_executive_summary(
    report_type: str,
    climate_data: Optional[Dict[str, Any]],
    rotation_data: Optional[List[Dict[str, Any]]],
) -> str:
    """Genera la sección de resumen ejecutivo."""
    summary_text = ""

    if climate_data:
        s = climate_data.get("summary", {})
        t2m = s.get("T2M", {})
        precip = s.get("PRECTOTCORR", {})
        rh = s.get("RH2M", {})

        summary_text += (
            f"Temperatura promedio: <strong>{t2m.get('promedio', 'N/D')}°C</strong> "
            f"(mín: {t2m.get('minimo', 'N/D')}°C, máx: {t2m.get('maximo', 'N/D')}°C). "
        )
        summary_text += (
            f"Precipitación promedio diaria: <strong>{precip.get('promedio', 'N/D')} mm</strong>. "
        )
        summary_text += (
            f"Humedad relativa promedio: <strong>{rh.get('promedio', 'N/D')}%</strong>."
        )
    else:
        summary_text = (
            "No se dispone de datos climáticos para este período. "
            "Las recomendaciones se basan en información general."
        )

    # Mejor estrategia
    strategy_note = ""
    if rotation_data and len(rotation_data) > 1:
        best = max(rotation_data[1:], key=lambda r: r.get("scores", {}).get("overall", 0))
        strategy_note = (
            f"<br><br>La estrategia recomendada es "
            f"<strong>{best.get('name', 'N/D')}</strong> con un puntaje general de "
            f"<strong>{best.get('scores', {}).get('overall', 0)}/100</strong>."
        )

    return f"""
    <div class="section">
        <h2>📋 Resumen Ejecutivo</h2>
        <div class="summary-box">
            {summary_text}{strategy_note}
        </div>
    </div>
    """


def _section_climate(climate_data: Dict[str, Any], report_type: str) -> str:
    """Genera la sección de condiciones climáticas."""
    s = climate_data.get("summary", {})

    # Tarjetas de datos principales
    cards = []
    param_config = [
        ("T2M", "Temperatura", "°C", "🌡️"),
        ("T2M_MAX", "Temp. Máx.", "°C", "🔺"),
        ("T2M_MIN", "Temp. Mín.", "°C", "🔻"),
        ("PRECTOTCORR", "Precipitación", "mm/día", "🌧️"),
        ("RH2M", "Humedad Rel.", "%", "💧"),
        ("GWETROOT", "Humedad Suelo", "", "🌱"),
        ("ALLSKY_SFC_SW_DWN", "Radiación Solar", "MJ/m²/día", "☀️"),
        ("WS2M", "Viento", "m/s", "💨"),
    ]

    for param, label, unit, icon in param_config:
        info = s.get(param, {})
        avg = info.get("promedio")
        if avg is not None:
            cards.append(
                f'<div class="data-card">'
                f'<div class="value">{icon} {avg}</div>'
                f'<div class="label">{label} ({unit})</div>'
                f'</div>'
            )

    cards_html = "\n".join(cards)

    return f"""
    <div class="section">
        <h2>🌤️ Condiciones Climáticas</h2>
        <div class="data-grid">
            {cards_html}
        </div>
        <p style="font-size: 12px; color: #888; margin-top: 10px;">
            Fuente: NASA POWER API · Comunidad agrícola (AG)
        </p>
    </div>
    """


def _section_soil_health(climate_data: Optional[Dict[str, Any]]) -> str:
    """Genera la sección de indicadores de salud del suelo."""
    if not climate_data:
        return """
        <div class="section">
            <h2>🌱 Indicadores de Salud del Suelo</h2>
            <div class="alert-box alert-info">
                ℹ️ No se dispone de datos suficientes para evaluar indicadores de suelo.
                Se recomienda realizar un análisis de suelo de laboratorio.
            </div>
        </div>
        """

    s = climate_data.get("summary", {})
    gwet = s.get("GWETROOT", {})
    avg_moisture = gwet.get("promedio")

    moisture_html = ""
    if avg_moisture is not None:
        # GWETROOT va de 0 a 1
        pct = round(avg_moisture * 100, 1) if avg_moisture <= 1 else avg_moisture
        if pct < 30:
            status = "Bajo"
            color = "score-low"
            note = "El suelo muestra déficit de humedad. Considere riego o cultivos tolerantes a sequía."
        elif pct < 60:
            status = "Adecuado"
            color = "score-medium"
            note = "Humedad del suelo en rango aceptable para la mayoría de cultivos."
        else:
            status = "Óptimo"
            color = "score-high"
            note = "Buenas condiciones de humedad en zona radicular."

        moisture_html = f"""
        <h3>Humedad en Zona Radicular</h3>
        <p><strong>{status}</strong> ({pct}%)</p>
        <div class="score-bar"><div class="score-fill {color}" style="width:{min(pct, 100)}%"></div></div>
        <p style="font-size: 13px; color: #666;">{note}</p>
        """

    return f"""
    <div class="section">
        <h2>🌱 Indicadores de Salud del Suelo</h2>
        {moisture_html}
        <div class="alert-box alert-info" style="margin-top: 15px;">
            ℹ️ Para una evaluación completa, se recomienda complementar con un
            análisis de suelo de laboratorio (pH, materia orgánica, N-P-K, CIC).
        </div>
    </div>
    """


def _section_rotation_recommendations(rotation_data: List[Dict[str, Any]]) -> str:
    """Genera la sección de recomendaciones de rotación."""
    rows = ""
    detail_blocks = ""

    for i, strategy in enumerate(rotation_data):
        scores = strategy.get("scores", {})
        overall = scores.get("overall", 0)
        crop_seq = " → ".join(strategy.get("crop_sequence", []))

        # Color según puntaje
        if overall >= 70:
            badge_color = "#4caf50"
        elif overall >= 45:
            badge_color = "#ff9800"
        else:
            badge_color = "#f44336"

        rows += f"""
        <tr>
            <td><strong>{strategy.get('name', f'Estrategia {i+1}')}</strong></td>
            <td style="font-size: 13px;">{crop_seq}</td>
            <td style="text-align: center;">
                <span style="background:{badge_color}; color:white; padding:2px 10px;
                border-radius: 12px; font-weight: 600;">{overall}</span>
            </td>
        </tr>
        """

        # Bloque de detalle
        benefits_html = "".join(f"<li>{b}</li>" for b in strategy.get("benefits", []))
        risks_html = "".join(f"<li>{r}</li>" for r in strategy.get("risks", []))

        score_bars = ""
        score_labels = [
            ("soil_health", "Salud del Suelo"),
            ("water_efficiency", "Eficiencia Hídrica"),
            ("climate_resilience", "Resiliencia Climática"),
            ("economic_potential", "Potencial Económico"),
            ("pest_management", "Manejo de Plagas"),
            ("erosion_control", "Control de Erosión"),
        ]
        for key, label in score_labels:
            val = scores.get(key, 0)
            css_class = "score-high" if val >= 70 else "score-medium" if val >= 45 else "score-low"
            score_bars += f"""
            <div style="margin: 4px 0;">
                <div style="display: flex; justify-content: space-between; font-size: 12px;">
                    <span>{label}</span><span>{val}/100</span>
                </div>
                <div class="score-bar"><div class="score-fill {css_class}" style="width:{val}%"></div></div>
            </div>
            """

        detail_blocks += f"""
        <div style="background: #f8f9fa; border-radius: 8px; padding: 15px; margin: 10px 0;">
            <h3>{strategy.get('name', f'Estrategia {i+1}')}</h3>
            <p style="font-size: 13px; color: #666; margin-bottom: 10px;">
                {strategy.get('description', '')}
            </p>
            {score_bars}
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 10px;">
                <div>
                    <strong style="color: #4caf50; font-size: 13px;">✅ Beneficios</strong>
                    <ul style="font-size: 13px;">{benefits_html}</ul>
                </div>
                <div>
                    <strong style="color: #f44336; font-size: 13px;">⚠️ Riesgos</strong>
                    <ul style="font-size: 13px;">{risks_html}</ul>
                </div>
            </div>
        </div>
        """

    return f"""
    <div class="section">
        <h2>🔄 Estrategias de Rotación</h2>
        <table>
            <thead>
                <tr>
                    <th>Estrategia</th>
                    <th>Secuencia</th>
                    <th>Puntaje</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
        {detail_blocks}
    </div>
    """


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


def _section_action_items(
    report_type: str,
    climate_data: Optional[Dict[str, Any]],
    rotation_data: Optional[List[Dict[str, Any]]],
) -> str:
    """Genera la sección de acciones recomendadas para el agricultor."""
    actions: List[str] = []

    if climate_data:
        s = climate_data.get("summary", {})

        # Acciones basadas en clima
        t2m_min = s.get("T2M_MIN", {})
        min_temp = t2m_min.get("minimo")
        if min_temp is not None and min_temp < 5:
            actions.append(
                "Preparar protección contra heladas para cultivos sensibles "
                "(coberturas, riego anti-helada, cortinas rompevientos)."
            )

        precip = s.get("PRECTOTCORR", {})
        avg_precip = precip.get("promedio")
        if avg_precip is not None and avg_precip < 2:
            actions.append(
                "Implementar técnicas de conservación de agua: mulching, "
                "riego por goteo, captación de agua de lluvia."
            )

        gwet = s.get("GWETROOT", {})
        avg_gwet = gwet.get("promedio")
        if avg_gwet is not None and avg_gwet < 0.3:
            actions.append(
                "La humedad del suelo es baja. Priorizar siembras de "
                "cultivos tolerantes a sequía."
            )

    # Acciones basadas en rotación
    if rotation_data and len(rotation_data) > 1:
        best = max(rotation_data[1:], key=lambda r: r.get("scores", {}).get("overall", 0))
        actions.append(
            f"Evaluar la implementación de la estrategia "
            f"'{best.get('name', 'recomendada')}' para el próximo ciclo."
        )

        # Verificar si falta fijador de N en la rotación actual
        if rotation_data[0].get("scores", {}).get("soil_health", 0) < 50:
            actions.append(
                "La rotación actual tiene bajo puntaje de salud del suelo. "
                "Incorporar al menos un cultivo leguminoso fijador de nitrógeno."
            )

    # Acciones generales
    actions.append("Realizar análisis de suelo si no se ha hecho en los últimos 12 meses.")

    if report_type == "monthly":
        actions.append(
            "Revisar el plan de rotación para la próxima temporada "
            "considerando las tendencias climáticas observadas."
        )

    items_html = ""
    for i, action in enumerate(actions, 1):
        items_html += f"""
        <div class="action-item">
            <div class="action-number">{i}</div>
            <div style="font-size: 14px;">{action}</div>
        </div>
        """

    return f"""
    <div class="section">
        <h2>✅ Acciones Recomendadas</h2>
        {items_html}
    </div>
    """


# --------------------------------------------------------------------------- #
#  Utilidades
# --------------------------------------------------------------------------- #

def _format_date(date_str: str) -> str:
    """Formatea una fecha YYYYMMDD a DD/MM/YYYY."""
    try:
        dt = datetime.strptime(date_str, "%Y%m%d")
        return dt.strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        return date_str


def _score_color_class(value: float) -> str:
    """Retorna la clase CSS según el puntaje."""
    if value >= 70:
        return "score-high"
    elif value >= 45:
        return "score-medium"
    return "score-low"
