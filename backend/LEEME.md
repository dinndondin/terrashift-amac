# AMAC — Código dividido por responsabilidad

Esta copia reorganiza los siete módulos Python originales. Conserva las firmas, fórmulas, textos, respuestas y rutas HTTP existentes. No es una corrección funcional de los errores previamente detectados.

## Inicio

Descomprime el proyecto completo, abre una terminal en esa carpeta e instala las dependencias en tu entorno:

```bash
python -m pip install -r requirements.txt
python app.py
```

El puerto predeterminado sigue siendo 5000 y se puede configurar mediante PORT. No inicies los módulos internos por separado. No mezcles este paquete con la versión anterior del proyecto sin conservar antes una copia.

## Organización

| Ubicación | Contenido |
| --- | --- |
| app.py | Punto de entrada; crea e inicia Flask. |
| amac/aplicacion.py | Creación de la aplicación y registro de Blueprints. |
| amac/http/ | Rutas de salud, clima, cultivos, análisis, reportes, región y suelo. |
| amac/nasa/ | Configuración, consultas HTTP, estadísticas, tendencias y riesgos. |
| amac/cultivos/ | Catálogo de cultivos y funciones de consulta. |
| amac/rotaciones/ | Configuración, puntuación, constructores, análisis, calendario y estrategias. |
| amac/reportes/ | Estilos, formato, secciones y ensamblaje del informe. |
| amac/suelos/ | Configuración y cliente SoilGrids. |
| amac/regional/ | Perfil regional y servicio de consulta. |

Los seis archivos originales restantes en la raíz son adaptadores de compatibilidad: importan las funciones desde amac para que llamadas como `from nasa_api import fetch_climate_data` sigan funcionando. No mantienen una segunda copia de la lógica.

Se mantienen los datos estáticos y CSS dentro de módulos propios, evitando introducir lecturas de archivos adicionales en esta primera refactorización. No se convierten funciones en clases cuando no necesitan estado.

## Qué editar

Para cambiar una fórmula de puntuación, edita amac/rotaciones/puntuacion.py. Para cambiar un endpoint, edita su módulo dentro de amac/http. Para modificar el informe, edita la sección correspondiente dentro de amac/reportes. Los adaptadores de la raíz no necesitan cambios para esas modificaciones.

## Verificación realizada

- Todos los módulos compilan.
- Los 39 cuerpos de función extraídos conservan su estructura sintáctica original.
- Se realizaron 99 comparaciones de comportamiento y estructura: catálogo, clientes con transporte simulado, riesgos, tendencias, rotaciones, reportes completos y las diez rutas HTTP.
- Se importaron los componentes de dominio y sus dependencias internas sin ciclos.
- No se ejecutaron peticiones reales ni el servidor Flask. El entorno de revisión no tenía Flask, flask-cors ni requests; las comprobaciones de transporte usaron respuestas simuladas.
- No se actualizan versiones de requirements.txt en esta entrega.

## Problemas originales que siguen pendientes

1. analyze, report y rotation-strategies llaman a fetch_climate_data sin las fechas obligatorias.
2. analyze pasa la respuesta completa a los evaluadores que esperan series individuales.
3. Sin observaciones, los evaluadores pueden informar riesgo bajo de heladas o estrés hídrico severo.
4. El rango de fechas mostrado en los informes no se usa para consultar ni filtrar el clima.
5. La agrupación por mes combina meses de distintos años en series multianuales.
6. SoilGrids conserva el fallback regional estático y los valores predeterminados originales.
7. La validación de JSON, coordenadas, fechas y prioridades debe unificarse.
8. Los textos insertados en HTML deben pasar a plantillas con escape automático.

Estos puntos deben corregirse en una segunda etapa, con pruebas de las nuevas respuestas y de sus efectos en el frontend.
