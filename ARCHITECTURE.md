# 🏛️ Especificación de Arquitectura de Software y Diseño de Sistemas
## Plataforma Terrashift — Asistente de Monitoreo Agrícola Climático (AMAC)
**NASA Space Apps Challenge 2026** — *Desafío: Field Shift: Adapting Farms with NASA Data*  
**Autoría Técnica:** Equipo AMAC (Documento de Ingeniería para Ingeniero Civil en Informática)  
**Versión:** 2.0.0 (Release Regional Biobío)

---

## 1. Resumen Ejecutivo y Alcance del Sistema

**Terrashift** es un Sistema de Soporte a la Toma de Decisiones Agronómicas (*Agro-Decision Support System*, DSS) basado en una arquitectura híbrida desacoplada (*Decoupled Hybrid Architecture*). El sistema fusiona en tiempo real observaciones satelitales de la Tierra de la **NASA** (NASA POWER, SMAP, GPM IMERG, Landsat/MODIS, ECOSTRESS) con telemetría edafológica global de **ISRIC SoilGrids (250m)** y bases de conocimiento agronómico local de la **Región del Biobío, Chile**.

### Propósito del Diseño
1. **Resiliencia Operativa ("Zero-Failure Architecture")**: La plataforma opera en modalidad autónoma del lado del cliente (*Local First / Client-Side Evaluation*) y cuenta con un microservicio backend RESTful en Python (Flask 3.0) para computación analítica avanzada y consumo directo de APIs satelitales en vivo.
2. **Modelo de Negocio B2B2C Escalable**:
   - **B2B (Cliente Pagador)**: Entidades gubernamentales y gremiales (INDAP, PRODESAL, PDTI, Municipalidades de Biobío, Cooperativas Cerealeras) mediante endpoints territoriales consolidados (`/api/v1/regional/biobio`).
   - **Copiloto / Facilitador**: Ingeniero Agrónomo o Extensionista Técnico (acceso a parámetros edáficos, pesos MCDA, descargas estructuradas).
   - **Beneficiario Final**: Agricultor de campo (interfaz simplificada, decisiones visuales de alto contraste y reporte físico ejecutivo de 1 página).

---

## 2. Diagrama de Topología del Sistema (C4 Level 2)

```
+----------------------------------------------------------------------------------------------------+
|                                    CAPA DE CLIENTE (FRONTEND SPA)                                   |
|                                                                                                    |
|   +--------------------+     +---------------------+     +--------------------+                    |
|   |   HTML5 Semantic   |     |    CSS3 Tokens      |     |  Leaflet 1.9.4     |                    |
|   |   Layout (7 Vistas)|     |    Palette System   |     |  + ESRI Satellite  |                    |
|   +---------+----------+     +----------+----------+     +---------+----------+                    |
|             |                           |                          |                               |
|   +---------v---------------------------v--------------------------v----------+                    |
|   |                          Controlador Maestro (app.js)                     |                    |
|   |         - Dispatcher de navegación          - Sincronizador de fechas     |                    |
|   |         - Gestión de estado global (Store)  - Telemetría en vivo          |                    |
|   +----+---------------+----------------+--------------------+----------------+                    |
|        |               |                |                    |                                     |
|        v               v                v                    v                                     |
|   +---------+    +-----------+    +-----------+        +-------------+                             |
|   | auth.js |    |   map.js  |    | reports.js|        | rotation.js |                             |
|   | (RBAC   |    | (Polígonos|    | (Reporte  |        | (MCDA Engine|                             |
|   | B2B2C)  |    | Prediales)|    | 1 Página) |        | Ponderador) |                             |
|   +---------+    +-----+-----+    +-----------+        +------+------+                             |
|                        |                                      |                                    |
|                        v                                      v                                    |
|             +---------------------+                +---------------------+                         |
|             | soilgrids-client.js |                |   regional-api.js   |                         |
|             | (ISRIC REST v2.0)   |                |   (Biobío Telemetry)|                         |
|             +----------+----------+                +----------+----------+                         |
+------------------------|--------------------------------------|------------------------------------+
                         |                                      |
                         | HTTPS / REST                         | HTTPS / REST
                         v                                      v
+----------------------------------------------------------------------------------------------------+
|                               CAPA DE SERVICIOS (BACKEND RESTFUL API)                               |
|                                                                                                    |
|                              +------------------------------------+                                |
|                              |      Flask 3.0 Core (app.py)       |                                |
|                              |  CORS Middleware | JSON Validation |                                |
|                              +--+--------------+---------------+--+                                |
|                                 |              |               |                                   |
|             +-------------------+              |               +--------------------+              |
|             v                                  v                                    v              |
|   +--------------------+             +-------------------+                +--------------------+   |
|   |   nasa_api.py      |             |rotation_engine.py |                |  soilgrids_api.py  |   |
|   | Agroclimatology &  |             | Algoritmo MCDA y  |                | ISRIC Data Parser  |   |
|   | Trend Evaluator    |             | Matriz de Decisión|                | & USDA Classifier  |   |
|   +---------+----------+             +---------+---------+                +---------+----------+   |
|             |                                  |                                    |              |
|             v                                  v                                    v              |
|   +--------------------+             +-------------------+                +--------------------+   |
|   |  crop_database.py  |             |report_generator.py|                |  regional_api.py   |   |
|   | 25+ Cultivos con   |             | Compilador HTML   |                | Perfil Territorial |   |
|   | Perfiles Hídricos  |             | Autónomo / Print  |                | Comunal Biobío     |   |
|   +--------------------+             +-------------------+                +--------------------+   |
+----------------------------------------------------------------------------------------------------+
                                                 |
                                                 | HTTPS Saliente
                                                 v
+----------------------------------------------------------------------------------------------------+
|                                    FUENTES DE DATOS EXTERNAS                                       |
|                                                                                                    |
|    +----------------------+   +-----------------------+   +------------------------------------+   |
|    |   NASA POWER API     |   | ISRIC SoilGrids v2.0  |   | NASA Earth Data Portals            |   |
|    |   Agroclimatology    |   | 250m Global Soils     |   | SMAP L4, GPM IMERG, Landsat/MODIS  |   |
|    +----------------------+   +-----------------------+   +------------------------------------+   |
+----------------------------------------------------------------------------------------------------+
```

---

## 3. Desglose Modular del Código

### 3.1. Capa de Presentación (Frontend SPA)
*Ubicación:* `frontend/`

- **`index.html`**: Estructura de documento semántico estructurado en 7 vistas mediante contenedores `<section>` desacoplados con visibilidad gobernada por atributos de clase:
  1. `#vista-dashboard`: Mando integral con resumen meteorológico, KPIs de suelo y vitrina de las 3 estrategias.
  2. `#vista-finca`: Sistema de Selección Geográfica, polígonos prediales (Leaflet + ESRI Satellite) e Inspector Dinámico de Suelos SoilGrids.
  3. `#vista-clima`: Monitor agroclimático satelital NASA POWER (temperatura, precipitación, evapotranspiración y alertas de estrés térmico/hídrico).
  4. `#vista-rotaciones`: Simulador interactivo del Motor de Rotaciones con ajuste de ponderaciones MCDA en tiempo real y cronograma fenológico estacional.
  5. `#vista-regional`: Portal B2B de inteligencia territorial para INDAP, PRODESAL y municipios de la Provincia de Biobío (tablas comunales y consola JSON API).
  6. `#vista-reportes`: Generador del Reporte Físico Oficial de 1 Página conforme a los estándares de transferencia técnica de AMAC (Dossier pág. 30-31).
  7. `#vista-nasa`: Fichas metodológicas de trazabilidad de los sensores y misiones espaciales utilizadas.

- **`css/styles.css`**: Sistema de diseño basado en variables nativas CSS (*CSS Custom Properties*), garantizando estricta adhesión a la paleta agro-hídrica oficial:
  - Primarios Verdes: `#2D6A4F` (Forest Green), `#40916C`, `#52B788`.
  - Acentos Azules (Agua/NASA): `#1B4965` (Navy Deep), `#2C7DA0`, `#61A5C2`.
  - Componentes modulares: cards con elevación `box-shadow`, badges de estado, tablas responsivas, grid auto-ajustable y directivas `@media print` para exportación en papel A4 sin desbordamientos.

- **`js/app.js`**: Controlador de ciclo de vida de la aplicación. Gestiona la inicialización de módulos, escucha de eventos globales, actualización dinámica de la fecha actual en español (`Sábado, 14 de Noviembre de 2026`) y control del indicador de sincronización satelital.

- **`js/auth.js`**: Subsistema de Control de Acceso Basado en Roles (RBAC) para el modelo B2B2C. Permite conmutar instantáneamente entre los perfiles:
  - `asesor`: Vista completa agronómica con acceso a variables fisicoquímicas profundas.
  - `agricultor`: Vista operativa simplificada con semáforos de acción y lenguaje llano.
  - `institucion`: Vista de agregación comunal para programas de fomento estatal.

- **`js/map.js`**: Integración cartográfica con Leaflet.js. Implementa capa satelital de alta resolución (ESRI World Imagery), capa base OpenStreetMap, renderizador de radio predial (~65 a 180 ha), sistema de autolocalización GPS y actualización reactiva del Inspector SoilGrids ante clics del usuario.

- **`js/soilgrids-client.js`**: Cliente desacoplado para consultar directamente el endpoint REST v2.0 de ISRIC SoilGrids (`https://rest.isric.org/soilgrids/v2.0/properties/query`). Extrae arcilla, arena, limo, carbono orgánico (SOC), pH y CIC a profundidades de 0-30 cm, calculando automáticamente la clase textural USDA.

- **`js/rotation.js`**: Motor analítico en el navegador que evalúa las 3 estrategias clave (Monocultivo tradicional, Regenerativa con leguminosa de cobertura, y Resiliencia Hídrica estricta) ante variaciones en las preferencias del agricultor.

- **`js/regional-api.js`**: Consola interactiva para el endpoint regional de Biobío, permitiendo a asesores e instituciones inspeccionar métricas de Los Ángeles, Mulchén, Cabrero y Santa Bárbara con vista previa de telemetría JSON.

- **`js/reports.js`**: Renderizador de alta fidelidad del Reporte Oficial de 1 Página para entrega en terreno a Don Manuel Alarcón, estructurado en los 7 bloques obligatorios del equipo AMAC.

---

### 3.2. Capa de Microservicios (Backend RESTful API)
*Ubicación:* `backend/`

- **`app.py`**: Microservicio RESTful en Python (Flask 3.0) con configuración CORS abierta para integración fluida con cualquier origen. Expone los siguientes endpoints estandarizados:
  - `GET /api/health`: Chequeo de salud del servicio y estado de integración satelital.
  - `POST /api/climate-data`: Extracción y agregación de series agroclimáticas NASA POWER para coordenadas específicas.
  - `POST /api/analyze`: Pipeline analítico completo (clima + suelo + cultivos candidatos + balance hídrico).
  - `GET /api/crops`: Catálogo agronómico completo con requerimientos hídricos, térmicos y edáficos.
  - `POST /api/rotation-strategies`: Generación y scoring matemático de alternativas de rotación.
  - `POST /api/report`: Generación del documento imprimible en formato HTML o JSON.
  - `GET /api/v1/regional/biobio`: **Endpoint Territorial B2B** para el monitoreo agrupado de la Provincia de Biobío.
  - `POST /api/v1/soilgrids` y `GET /api/v1/soilgrids`: Proxy de consulta y normalización de propiedades edáficas de ISRIC SoilGrids.

- **`soilgrids_api.py`**: Conector con la API REST de ISRIC World Soil Information. Procesa las respuestas multiespectrales de capas en profundidad (`0-5cm`, `5-15cm`, `15-30cm`), calcula promedios ponderados y maneja fallbacks automáticos ante caídas del servicio internacional con el perfil trumao/volcánico de Biobío.

- **`regional_api.py`**: Repositorio de datos consolidados para la Región del Biobío, integrando datos estadísticos de INDAP, cobertura de PRODESAL (58%) y características microclimáticas de las 4 comunas piloto.

- **`nasa_api.py`**: Módulo de interacción con la API de Agroclimatología de NASA POWER. Descarga parámetros meteorológicos (`T2M`, `T2M_MAX`, `T2M_MIN`, `PRECTOTCORR`, `ALLSKY_SFC_SW_DWN`, `GWETROOT`, `EVPTRNS`) y evalúa riesgos de heladas tardías y ventanas de sequía.

- **`crop_database.py`**: Base de datos agronómica de 25+ especies agrícolas con parámetros biológicos estandarizados: ciclo fenológico, temperatura base, necesidades hídricas en mm/ciclo, tolerancia a salinidad/acidez, aporte de biomasa radicular y potencial de fijación simbiótica de nitrógeno ($kg\ N/ha$).

- **`rotation_engine.py`**: Motor de optimización de rotaciones basado en Análisis Multicriterio (MCDA). Identifica ventanas de barbecho descubierto y formula planes de rotación de 3 años minimizando estrés hídrico y plagas recurrentes.

- **`report_generator.py`**: Generador de reportes agronómicos con plantillas HTML limpias, diseñadas específicamente para impresión técnica y archivo predial.

---

## 4. Matriz de Fusión de Datos Satelitales y Edafológicos

| Misión / Sensor | Proveedor | Resolución Espacial | Cadencia Temporal | Parámetros Extraídos | Función en Terrashift AMAC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **NASA POWER** | NASA LaRC | 0.5° × 0.625° | Diaria / Horaria | `T2M_MIN`, `T2M_MAX`, `PRECTOT`, `ALLSKY_SW`, `EVPTRNS` | Balance hídrico del cultivo, acumulación de Grados Día Desarrollo (GDD) y detección de heladas. |
| **SoilGrids v2.0** | ISRIC | 250 m | Estática (actualizada) | `clay`, `sand`, `silt`, `soc`, `phh2o`, `cec` | Determinación de capacidad de retención de humedad (AWC), textura USDA y fertilidad basal del suelo. |
| **SMAP (L4)** | NASA JPL/GSFC | 9 km | 2–3 días | Humedad superficial y de zona radicular (`GWETROOT`) | Detección precoz de estrés hídrico previo a sintomatología visible en la canopia. |
| **GPM IMERG** | NASA / JAXA | 0.1° (~10 km) | 30 min / Diaria | Precipitación acumulada corregida por satélite | Estimación de riesgo de erosión hídrica durante periodos de suelo descubierto. |
| **Landsat 8-9 / MODIS** | USGS / NASA | 30 m / 250 m | 8–16 días | NDVI, EVI, reflectancia superficial | Monitoreo histórico del vigor vegetativo y validación de cobertura verde en barbechos. |
| **ECOSTRESS** | NASA JPL (ISS) | 70 m | 1–5 días | Temperatura de superficie terrestre (LST) y Evapotranspiración | Mapeo microclimático a nivel de parcela y detección de micro-islas de calor o déficit térmico. |

---

## 5. Formalización Matemática del Motor de Decisión (MCDA)

El motor de recomendación de rotaciones implementa un modelo de **Análisis de Decisión Multicriterio (Multi-Criteria Decision Analysis - MCDA)** basado en una suma lineal ponderada sujeta a penalizaciones no lineales por restricciones agronómicas:

$$S(r) = \left[ \sum_{j=1}^{n} w_j \cdot s_j(r) \right] \cdot \prod_{k=1}^{m} P_k(r)$$

### Definición de Variables y Parámetros:
- **$r$**: Estrategia de rotación evaluada (secuencia de cultivos $C_1 \rightarrow C_2 \rightarrow C_3$).
- **$w_j$**: Vector de pesos ponderados definidos por las prioridades del agricultor o preestablecidos por el asesor técnico, normalizados de forma estricta:
  $$\sum_{j=1}^{n} w_j = 1 \quad \text{donde } w_j \ge 0$$
- **$s_j(r) \in [0, 100]$**: Función de puntaje para el criterio agronómico $j$:
  1. **$s_{\text{suelo}}(r)$ (Salud del Suelo)**: Aporte neto de biomasa, fijación de nitrógeno ($\Delta N$) e incremento estimado de materia orgánica (MOS).
  2. **$s_{\text{agua}}(r)$ (Eficiencia Hídrica)**: Ratio entre requerimiento hídrico acumulado de la rotación ($\sum ET_c$) y la oferta hídrica satelital estimada (Precipitación efectiva NASA POWER + reserva de agua útil SoilGrids).
  3. **$s_{\text{resil}}(r)$ (Resiliencia Climática)**: Capacidad del dosel de tolerar variabilidad térmica (días sobre $30^\circ\text{C}$ y heladas invernales).
  4. **$s_{\text{econ}}(r)$ (Idoneidad Comercial)**: Demanda y estabilidad de precios de los cereales y forrajes en el mercado local chileno (trigo, maíz, forraje para ganado).
  5. **$s_{\text{facil}}(r)$ (Complejidad de Manejo)**: Disponibilidad de maquinaria, semillas certificadas y experiencia del productor local.

### Factores de Penalización ($P_k(r) \in (0, 1]$):
- **$P_{\text{plagas}}$**: Penaliza con un factor $0.40$ la repetición sucesiva de especies de la misma familia botánica (ej: *Triticum aestivum* sobre *Triticum durum* consecutivamente por acumulación de *Fusarium* y *Gaeumannomyces graminis*).
- **$P_{\text{helada}}$**: Si la especie seleccionada es susceptible a heladas en meses con temperatura mínima satelital $< 0^\circ\text{C}$ (NASA POWER `T2M_MIN`), se aplica $P_{\text{helada}} = 0.50$.
- **$P_{\text{suelo\_desnudo}}$**: Si el periodo de barbecho descubierto supera los 60 días en época de altas precipitaciones (GPM IMERG), se penaliza por riesgo de lixiviación y erosión laminar.

---

## 6. Especificación de Contratos de la API RESTful

### 6.1. Endpoint Territorial B2B: `/api/v1/regional/biobio`
- **Método:** `GET`
- **Descripción:** Provee el estado consolidado de la cuenca cerealera de Biobío para INDAP y municipalidades.
- **Respuesta (JSON 200 OK):**
```json
{
  "status": "success",
  "service": "Terrashift Regional API (B2B2C)",
  "model": "NASA Earth Observation + SoilGrids Data Fusion",
  "data": {
    "region_id": "CL-BI",
    "name": "Región del Biobío",
    "target_focus": "Provincia de Biobío (Cuna cerealera: 45.7% de trigo candeal nacional)",
    "comunas_monitoreadas": [
      {
        "comuna": "Los Ángeles",
        "lat": -37.47,
        "lon": -72.35,
        "soilgrids_texture": "Franco arcillo-arenoso (Trumao)",
        "soil_ph": 5.9,
        "soil_organic_matter": "3.8%",
        "nasa_climate": {
          "temp_media": "14.2°C",
          "precip_anual": "1050 mm"
        },
        "estres_hidrico": "Moderado (Déficit en enero-febrero)",
        "rotacion_recomendada": "Trigo Candeal -> Vicia villosa -> Maíz"
      }
    ]
  }
}
```

### 6.2. Endpoint Edafológico: `/api/v1/soilgrids`
- **Método:** `POST` o `GET`
- **Parámetros:** `lat` (float), `lon` (float)
- **Respuesta (JSON 200 OK):**
```json
{
  "status": "success",
  "coordinates": { "lat": -37.47, "lon": -72.35 },
  "clay_percent": 22,
  "sand_percent": 54,
  "silt_percent": 24,
  "organic_matter_percent": 3.8,
  "ph": 5.9,
  "cec": 18.5,
  "source": "SoilGrids v2.0 (ISRIC World Soil Information)"
}
```

---

## 7. Modelo de Seguridad y Control de Acceso (RBAC) B2B2C

```
                      +-----------------------------+
                      |         USUARIOS            |
                      +--------------+--------------+
                                     |
           +-------------------------+-------------------------+
           |                         |                         |
           v                         v                         v
+---------------------+   +---------------------+   +---------------------+
|        ASESOR       |   |      AGRICULTOR     |   |     INSTITUCIÓN     |
| (Ing. R. Valenzuela)|   | (Don Manuel Alarcón)|   |  (INDAP / Municipio)|
+----------+----------+   +----------+----------+   +----------+----------+
           |                         |                         |
           | Permisos:               | Permisos:               | Permisos:
           | - Calibración MCDA      | - Lectura de semáforos  | - API B2B Regional
           | - Análisis SoilGrids    | - Vista de calendario   | - Análisis comunal
           | - Emisión de Reporte    | - Validación en terreno | - Estadísticas de uso
           v                         v                         v
+-------------------------------------------------------------------------+
|                  APLICACIÓN WEB TERRASHIFT (SPA RBAC)                   |
+-------------------------------------------------------------------------+
```

1. **Aislamiento de Telemetría**: El agricultor no requiere credenciales complejas ni compartir datos financieros privados. Las coordenadas prediales son almacenadas en el `localStorage` del cliente y procesadas de forma efímera en la API satelital.
2. **Offline-Resilience**: En caso de pérdida de conectividad a Internet durante la visita a terreno, la aplicación mantiene en caché local la última telemetría satelital consultada y utiliza tablas edafológicas precalculadas de la cuenca del Biobío.

---

## 8. Guía de Ejecución y Pruebas para Desarrolladores

### Requisitos del Sistema
- Python 3.8+ (para el servidor analítico backend)
- Cualquier navegador web con soporte ES6+ (Chrome, Firefox, Safari, Edge)

### Despliegue Local Inmediato
1. **Modo Autónomo (Frontend directo):**  
   Hacer doble clic en `frontend/index.html` o ejecutar `Iniciar_AMAC.bat`. La aplicación se iniciará de inmediato con el motor analítico del cliente y conexión en vivo a ISRIC SoilGrids.
2. **Modo Completo con Backend Python (NASA POWER live):**
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```
   El backend escuchará en `http://localhost:5000`.

---
*Terrashift AMAC — Ingeniería de Software al servicio de la agricultura climáticamente inteligente.*
