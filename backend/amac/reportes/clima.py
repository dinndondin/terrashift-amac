"""Componente amac.reportes.clima; lógica extraída de report_generator.py."""

from typing import Any
from typing import Dict


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
