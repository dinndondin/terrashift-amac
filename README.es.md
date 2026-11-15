<div align="center">

# 🌱 TERRASHIFT (AMAC)
### Asistente de Monitoreo Agrícola Climático y Rotación Inteligente de Cultivos

**NASA Space Apps Challenge 2026** · *Desafío: Field Shift — Adapting Farms with NASA Data*

[![English](https://img.shields.io/badge/Language-English-1B4965?style=for-the-badge)](README.md)
[![Español](https://img.shields.io/badge/Idioma-Español-2D6A4F?style=for-the-badge)](README.es.md)
[![Licencia: MIT](https://img.shields.io/badge/Licencia-MIT-40916C?style=for-the-badge)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](backend/requirements.txt)
[![Flask 3.0](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](backend/app.py)

*Transformamos datos satelitales de la NASA y telemetría global de suelos en decisiones claras y accionables de rotación de cultivos para agricultores, asesores técnicos e instituciones rurales.*

[📖 Cómo Funciona (Guía Breve)](docs/COMO_FUNCIONA_ES.md) · [🏛️ Arquitectura Técnica](ARCHITECTURE.md) · [🚀 Inicio Rápido](#-inicio-rápido)

</div>

---

## 🎯 El Problema

Los agricultores enfrentan cambios de temperatura, lluvias erráticas, sequías prolongadas, heladas tardías y degradación progresiva del suelo. Elegir qué cultivo sembrar después —y evitar dejar la tierra desnuda durante meses— suele hacerse por intuición o con recomendaciones genéricas que no consideran el microclima ni las propiedades reales del suelo de cada predio.

## 💡 ¿Qué hace TERRASHIFT (AMAC)?

**TERRASHIFT** (*Asistente de Monitoreo Agrícola Climático* — AMAC) es un **Sistema de Soporte a la Toma de Decisiones Agronómicas (DSS)** bajo modelo **B2B2C**, piloteado en la **Provincia de Biobío, Chile** (Los Ángeles, Mulchén, Cabrero y Santa Bárbara).

Combina **observaciones satelitales de la NASA** con datos edáficos de **ISRIC SoilGrids (250 m)** y un motor matemático de **Análisis Multicriterio (MCDA)** para:

1. **Ubicar cualquier predio** en un mapa satelital interactivo e inspeccionar su textura, pH, materia orgánica y retención de humedad.
2. **Evaluar riesgos agroclimáticos** (ventanas de heladas, estrés hídrico, olas de calor y riesgo de erosión en barbechos).
3. **Comparar 3 estrategias de rotación de cultivos** adaptadas a un catálogo agronómico de 26 especies.
4. **Adaptar la interfaz según el perfil del usuario** (Agricultor, Asesor Técnico o Institución).
5. **Generar un informe imprimible de 1 página** listo para entregar y ejecutar en terreno.

---

## 👥 ¿Para quién está diseñado? (Modelo de Roles B2B2C)

Al abrir TERRASHIFT, cada usuario elige el perfil que mejor se adapta a su trabajo:

| Perfil | Usuario Objetivo | Qué ve y qué puede hacer |
| :--- | :--- | :--- |
| 🚜 **Agricultor / Productor** | Agricultores familiares y medianos | Panel simple y sin tecnicismos, alertas tipo semáforo, recomendación directa de qué sembrar y guía práctica imprimible de 1 página. |
| 🔬 **Asesor Técnico** | Agrónomos / Extensionistas (PRODESAL / INDAP) | Cartera de múltiples agricultores, variables fisicoquímicas de SoilGrids, calibración en vivo de pesos MCDA y emisión de reportes. |
| 🏛️ **Institución (B2B)** | Municipalidades, INDAP y cooperativas | Portal territorial de la Provincia de Biobío, comparativa de vulnerabilidad comunal y consola de telemetría JSON (`/api/v1/regional/biobio`). |

---

## 🔄 Las 3 Estrategias de Rotación Comparadas

TERRASHIFT evalúa y puntúa secuencias multianuales según **6 criterios ponderables**: *conservación de agua, salud del suelo, retorno económico, corte de ciclo de plagas, control de erosión* y *fijación biológica de nitrógeno*.

| Estrategia | Ejemplo de Secuencia | Impacto Principal |
| :--- | :--- | :--- |
| **1. Monocultivo Tradicional (Línea Base)** | Cultivo de verano → ~150 días de barbecho desnudo → Maíz | Alto riesgo de erosión, pérdida de materia orgánica y alta dependencia de fertilizantes sintéticos. |
| **2. Regeneración de Suelo y Biomasa ⭐ (Recomendada)** | Cereal/Cultivo → Cultivo de cobertura invernal (*Vicia villosa*) → Maíz sobre rastrojo | **0 días de suelo desnudo**, fijación natural de nitrógeno, menor gasto en urea y mayor retención de humedad. |
| **3. Resiliencia Hídrica y Defensa ante Sequía 💧** | Sorgo forrajero de raíz profunda → Centeno invernal (*Secale cereale*) → Girasol | Maximiza la eficiencia del uso del agua en suelos arenosos o con déficit hídrico severo. |

---

## 🖥️ Módulos de la Aplicación (7 Vistas Interactivas)

1. **🏠 General** — Resumen instantáneo de clima, indicadores del suelo y la estrategia ganadora.
2. **🌾 Mi Predio** — Mapa interactivo Leaflet (OpenStreetMap + Satélite ESRI) con polígonos prediales y consulta en vivo a ISRIC SoilGrids v2.0.
3. **🌤️ Clima NASA** — Gráficos de temperatura, precipitación, radiación solar y evapotranspiración desde NASA POWER, con alertas de heladas y sequía.
4. **🔄 3 Estrategias** — Simulador MCDA interactivo donde los deslizadores recalculan puntajes y calendarios fenológicos en tiempo real.
5. **🏛️ Portal Regional** — Monitoreo territorial de Los Ángeles, Mulchén, Cabrero y Santa Bárbara con vista previa de API JSON.
6. **📊 Informe Oficial** — Ficha técnica de 1 página lista para imprimir (`@media print` en A4) y entregar en terreno.
7. **🛰️ Bases NASA / Suelos** — Fichas científicas con trazabilidad de cada satélite y fuente de datos utilizada.

---

## 📡 Datos de la NASA y Fuentes Globales Utilizadas

| Misión / Dataset | Fuente | Parámetros Clave | Uso en TERRASHIFT |
| :--- | :--- | :--- | :--- |
| **NASA POWER** | NASA LaRC | `T2M`, `T2M_MAX`, `T2M_MIN`, `PRECTOTCORR`, `ALLSKY_SFC_SW_DWN` | Series agroclimáticas, Grados Día (GDD) y riesgo de heladas |
| **ISRIC SoilGrids v2.0** | ISRIC World Soil | Arcilla, Arena, Limo, SOC, pH, CIC (0–30 cm) | Clasificación textural USDA y retención hídrica del suelo |
| **SMAP (L4)** | NASA JPL / GSFC | `GWETROOT` (Humedad radicular) | Ventanas óptimas de siembra y detección temprana de sequía |
| **GPM IMERG** | NASA / JAXA | Anomalías e intensidad de lluvia | Riesgo de erosión hídrica durante periodos sin cobertura |
| **Landsat 8-9 y MODIS** | NASA / USGS | Índices `NDVI` y `EVI` | Vigor vegetativo y validación de cultivos de cobertura |
| **ECOSTRESS** | NASA JPL (ISS) | `EVPTRNS` y temperatura del dosel | Evapotranspiración y monitoreo de estrés hídrico |
| **GRACE / GRACE-FO** | NASA / GFZ | Anomalías de almacenamiento hídrico | Tendencias regionales de agua subterránea a largo plazo |

---

## 🏗️ Arquitectura del Sistema

TERRASHIFT utiliza una **Arquitectura Híbrida Resiliente ("Zero-Failure")**:
- **Modo Autónomo (Solo Navegador):** Funciona directamente abriendo el frontend, con cálculo MCDA en el cliente, respaldos locales y consulta directa a ISRIC SoilGrids.
- **Modo Completo (con Backend Python):** Se conecta a la API REST en Flask 3.0 para consultar NASA POWER en vivo, filtrar la base de 26 cultivos y generar reportes HTML/JSON.

```text
┌───────────────────────────┐       HTTPS / REST       ┌───────────────────────────┐
│   Frontend SPA (Browser)  │ ───────────────────────▶ │   Backend API (Flask 3.0) │
│   HTML5 · CSS3 · ES6 JS   │ ◀─────────────────────── │   Python 3.8+             │
│   Leaflet · Chart.js      │                          │   Motor MCDA · 26 Cultivos│
└─────────────┬─────────────┘                          └─────────────┬─────────────┘
              │                                                      │
              ▼                                                      ▼
   ISRIC SoilGrids v2.0                                       NASA POWER API
  (Telemetría de Suelos)                                 (Agroclimatología en Vivo)
```

---

## 🚀 Inicio Rápido

### Opción 1: Uso Inmediato (Sin instalar nada)
1. Haz doble clic en `Iniciar_AMAC.bat` (en Windows) o abre `frontend/index.html` directamente en tu navegador.
2. Elige tu perfil (**Agricultor**, **Asesor Técnico** o **Institución**) y comienza a explorar.

### Opción 2: Modo Completo con Backend Python (NASA POWER en vivo)
**Requisito previo:** Python 3.8+

```bash
# 1. Ir a la carpeta del backend
cd backend

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Iniciar el servidor Flask (puerto http://localhost:5000)
python app.py
```

Luego abre `frontend/index.html` (o sirve `frontend/` con `python -m http.server 8080` y entra a `http://localhost:8080`).

### Endpoints Principales de la API
* `GET /api/health` — Estado del servicio e integración satelital
* `POST /api/climate-data` — Series agroclimáticas históricas desde NASA POWER
* `POST /api/analyze` — Análisis integral 360° del predio (clima + riesgos + rotaciones)
* `GET /api/crops` — Catálogo completo de 26 cultivos
* `POST /api/rotation-strategies` — Cálculo personalizado de estrategias MCDA
* `POST /api/report` — Generación de reportes periódicos en HTML o JSON
* `GET /api/v1/regional/biobio` — Endpoint territorial B2B para la Provincia de Biobío
* `GET / POST /api/v1/soilgrids` — Consulta normalizada de suelos ISRIC SoilGrids v2.0

---

## 📁 Estructura del Proyecto

```text
├── frontend/
│   ├── index.html              # Interfaz SPA de 7 vistas + Selector de Rol B2B2C
│   ├── css/styles.css          # Sistema de diseño agro-hídrico y estilos de impresión A4
│   └── js/                     # Módulos JS (app, auth, map, rotation, charts, reports, regional-api, soilgrids-client, nasa-data)
├── backend/
│   ├── app.py                  # Servidor API REST Flask 3.0
│   ├── nasa_api.py             # Cliente NASA POWER y evaluadores de riesgo
│   ├── soilgrids_api.py        # Procesador de ISRIC SoilGrids v2.0 y clasificación USDA
│   ├── crop_database.py        # Base de conocimiento de 26 cultivos
│   ├── rotation_engine.py      # Motor de optimización de rotaciones MCDA
│   ├── regional_api.py         # Datos territoriales B2B de Biobío
│   ├── report_generator.py     # Generador de reportes imprimibles
│   └── requirements.txt        # Dependencias Python
├── docs/
│   ├── HOW_IT_WORKS_EN.md      # Guía visual breve (Inglés)
│   └── COMO_FUNCIONA_ES.md     # Guía visual breve (Español)
├── ARCHITECTURE.md             # Especificación técnica detallada de arquitectura
├── Iniciar_AMAC.bat            # Lanzador rápido en 1 clic (Windows)
├── README.md                   # Documentación principal (Inglés)
├── README.es.md                # Documentación en Español
└── LICENSE                     # Licencia MIT
```

---

## 👥 Equipo AMAC y Licencia

Desarrollado por el **Equipo AMAC** para el **NASA Space Apps Challenge 2026**.  
Publicado bajo [Licencia MIT](LICENSE) — libre uso educativo, agrícola y de investigación.
