"""Componente amac.reportes.rotaciones; lógica extraída de report_generator.py."""

from typing import Any
from typing import Dict
from typing import List


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
