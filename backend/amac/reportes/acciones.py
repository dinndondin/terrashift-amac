"""Componente amac.reportes.acciones; lógica extraída de report_generator.py."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional


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
