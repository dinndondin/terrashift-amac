"""Componente amac.reportes.resumen; lógica extraída de report_generator.py."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional


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
