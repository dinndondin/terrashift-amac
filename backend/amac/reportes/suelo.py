"""Componente amac.reportes.suelo; lógica extraída de report_generator.py."""

from typing import Any
from typing import Dict
from typing import Optional


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
