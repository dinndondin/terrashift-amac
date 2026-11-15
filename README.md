<div align="center">

# 🌱 TERRASHIFT (AMAC)
### Climate-Smart Crop Rotation & Agricultural Decision Support Platform

**NASA Space Apps Challenge 2026** · *Challenge: Field Shift — Adapting Farms with NASA Data*

[![English](https://img.shields.io/badge/Language-English-1B4965?style=for-the-badge)](README.md)
[![Español](https://img.shields.io/badge/Idioma-Español-2D6A4F?style=for-the-badge)](README.es.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-40916C?style=for-the-badge)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](backend/requirements.txt)
[![Flask 3.0](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](backend/app.py)

*Transforming NASA satellite Earth Observations and global soil telemetry into clear, actionable crop rotation decisions for farmers, agronomists, and rural institutions.*

[Link to GITLAB](https://terrashift-amac-148591.gitlab.io)
[📖 How It Works (Brief Visual Guide)](docs/HOW_IT_WORKS_EN.md) · [🏛️ System Architecture (ES)](ARCHITECTURE.md) · [🚀 Quick Start](#-quick-start)

</div>

---

## 🎯 The Problem

Farmers worldwide face shifting temperatures, erratic rainfall, prolonged droughts, late frosts, and soil degradation. Choosing which crop to plant next—and when to keep living roots in the soil—often relies on guesswork or generic advice that ignores micro-climate trends and local soil properties.

## 💡 What TERRASHIFT (AMAC) Does

**TERRASHIFT** (*Asistente de Monitoreo Agrícola Climático* — AMAC) is a **B2B2C Agronomic Decision Support System (DSS)** piloted in the **Biobío Province, Chile** (Los Ángeles, Mulchén, Cabrero, and Santa Bárbara).

It fuses **NASA satellite climate data** with **ISRIC SoilGrids (250 m)** soil telemetry and a **Multi-Criteria Decision Analysis (MCDA)** engine to:

1. **Locate any farm** on an interactive satellite map and inspect its soil texture, pH, organic matter, and water retention.
2. **Analyze agroclimatic risks** (frost windows, heat waves, water deficit, and bare-soil erosion periods).
3. **Compare 3 tailored crop rotation strategies** head-to-head across a 26-crop agronomic catalog.
4. **Adapt the experience to each user role** (Farmer, Technical Advisor, or Government Institution).
5. **Generate a 1-page printable field report** for immediate on-farm execution.

---

## 👥 Who Is It For? (B2B2C Role System)

Upon opening TERRASHIFT, users choose the view that fits their daily workflow:

| Role | Target User | What They See & Do |
| :--- | :--- | :--- |
| 🚜 **Farmer / Producer** | Family & commercial farmers | Simplified, jargon-free dashboard with traffic-light risk alerts, clear planting recommendations, and a 1-page printable field guide. |
| 🔬 **Technical Advisor** | Agronomists (PRODESAL / INDAP) | Multi-farm portfolio management, full SoilGrids physicochemical metrics, real-time MCDA weight sliders, and report generation. |
| 🏛️ **Institution (B2B)** | Municipalities & agricultural agencies | Regional Biobío territorial intelligence dashboard, commune-level vulnerability comparison, and live JSON API telemetry (`/api/v1/regional/biobio`). |

---

## 🔄 The 3 Core Crop Rotation Strategies

TERRASHIFT evaluates and scores multi-season sequences based on **6 farmer-weighted criteria**: *water conservation, soil health, economic return, pest cycle breaking, erosion control,* and *biological nitrogen fixation*.

| Strategy | Sequence Example | Key Impact |
| :--- | :--- | :--- |
| **1. Traditional Monoculture (Baseline)** | Summer Crop → ~150 days Bare Fallow → Summer Maize | High erosion risk, organic matter loss, heavy synthetic fertilizer dependency. |
| **2. Soil & Biomass Regeneration ⭐ (Recommended)** | Cereal/Summer Crop → Winter Cover Crop (*Vicia villosa*) → Late Maize over mulch | **0 days of bare soil**, natural nitrogen fixation, lower synthetic urea cost, improved moisture retention. |
| **3. Water Resilience & Drought Defense 💧** | Deep-rooted Forage Sorghum → Winter Rye (*Secale cereale*) → Sunflower | Maximizes water-use efficiency in sandy or drought-stressed soils by tapping deeper moisture layers. |

---

## 🖥️ Inside the App (7 Interactive Modules)

1. **🏠 General Dashboard** — Instant overview of weather KPIs, soil health status, and top-ranked rotation strategy.
2. **🌾 My Farm (`Mi Predio`)** — Interactive Leaflet map (OpenStreetMap + ESRI Satellite) with farm boundary visualization and live ISRIC SoilGrids v2.0 lookup.
3. **🌤️ NASA Climate (`Clima NASA`)** — Temperature, rainfall, solar radiation, and evapotranspiration charts powered by NASA POWER, with frost and drought alerts.
4. **🔄 3 Strategies (`3 Estrategias`)** — Interactive MCDA simulator where sliders recalculate rotation scores and phenological timelines in real time.
5. **🏛️ Regional Portal** — Provincial Biobío monitoring across Los Ángeles, Mulchén, Cabrero, and Santa Bárbara with a live API telemetry viewer.
6. **📊 Official Report** — Clean, print-ready (`@media print` A4) 1-page technical sheet ready to hand directly to farmers in the field.
7. **🛰️ NASA & Soil Data** — Scientific traceability cards explaining every satellite sensor and dataset behind the calculations.

---

## 📡 NASA & Global Datasets Integrated

| Dataset / Mission | Source | Parameters Used | Purpose in TERRASHIFT |
| :--- | :--- | :--- | :--- |
| **NASA POWER** | NASA LaRC | `T2M`, `T2M_MAX`, `T2M_MIN`, `PRECTOTCORR`, `ALLSKY_SFC_SW_DWN` | Agroclimatic series, Growing Degree Days (GDD), frost risk windows |
| **ISRIC SoilGrids v2.0** | ISRIC World Soil | Clay, Sand, Silt, SOC, pH, CEC (0–30 cm) | USDA soil texture classification & water-holding capacity |
| **SMAP (L4)** | NASA JPL / GSFC | `GWETROOT` (Root-zone soil moisture) | Sowing windows & early drought stress detection |
| **GPM IMERG** | NASA / JAXA | Precipitation anomalies & intensity | Bare-fallow water erosion risk assessment |
| **Landsat 8-9 & MODIS** | NASA / USGS | `NDVI`, `EVI` vegetation indices | Vegetative vigor & cover-crop verification |
| **ECOSTRESS** | NASA JPL (ISS) | `EVPTRNS` & canopy temperature | Evapotranspiration & crop water stress monitoring |
| **GRACE / GRACE-FO** | NASA / GFZ | Terrestrial water storage anomalies | Long-term regional aquifer & basin water trends |

---

## 🏗️ Architecture

TERRASHIFT uses a **Zero-Failure Hybrid Architecture**:
- **Autonomous Frontend Mode:** Runs directly in any modern browser using client-side MCDA models, offline-resilient fallbacks, and live REST calls to ISRIC SoilGrids.
- **Full-Stack Mode (with Python Backend):** Connects to the Flask 3.0 REST API for live NASA POWER data queries, full 26-crop database filtering, and HTML/JSON report generation.

```text
┌───────────────────────────┐       HTTPS / REST       ┌───────────────────────────┐
│   Frontend SPA (Browser)  │ ───────────────────────▶ │   Backend API (Flask 3.0) │
│   HTML5 · CSS3 · ES6 JS   │ ◀─────────────────────── │   Python 3.8+             │
│   Leaflet · Chart.js      │                          │   MCDA Engine · 26 Crops  │
└─────────────┬─────────────┘                          └─────────────┬─────────────┘
              │                                                      │
              ▼                                                      ▼
   ISRIC SoilGrids v2.0                                       NASA POWER API
   (Live Soil Telemetry)                                  (Live Agroclimatology)
```

---

## 🚀 Quick Start

### Option 1: Instant Launch (No Backend Required)
1. Open `frontend/index.html` directly in your browser (or double-click `Iniciar_AMAC.bat` on Windows).
2. Choose **Farmer**, **Technical Advisor**, or **Institution** and start exploring.

### Option 2: Full Mode with Live NASA POWER Backend
**Prerequisites:** Python 3.8+

```bash
# 1. Navigate to the backend folder
cd backend

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the Flask API server (runs on http://localhost:5000)
python app.py
```

Then open `frontend/index.html` (or serve `frontend/` with `python -m http.server 8080` and visit `http://localhost:8080`).

### Main Backend API Endpoints
* `GET /api/health` — Service & satellite integration health check
* `POST /api/climate-data` — Historical NASA POWER agroclimatic time series
* `POST /api/analyze` — Full 360° farm analysis (climate + risks + rotations + fallow windows)
* `GET /api/crops` — Complete 26-crop agronomic catalog
* `POST /api/rotation-strategies` — Custom MCDA rotation scoring
* `POST /api/report` — Generate printable HTML/JSON periodic reports
* `GET /api/v1/regional/biobio` — B2B provincial Biobío monitoring endpoint
* `GET / POST /api/v1/soilgrids` — ISRIC SoilGrids v2.0 soil profile query

---

## 📁 Project Structure

```text
├── frontend/
│   ├── index.html              # 7-view SPA interface + B2B2C Role Gate
│   ├── css/styles.css          # Agro-hydric design system & A4 print rules
│   └── js/                     # Modular controllers (app, auth, map, rotation, charts, reports, regional-api, soilgrids-client, nasa-data)
├── backend/
│   ├── app.py                  # Flask 3.0 REST API server
│   ├── nasa_api.py             # NASA POWER client & risk evaluators
│   ├── soilgrids_api.py        # ISRIC SoilGrids v2.0 parser & USDA classifier
│   ├── crop_database.py        # 26-crop agronomic knowledge base
│   ├── rotation_engine.py      # MCDA rotation optimization engine
│   ├── regional_api.py         # Biobío B2B regional data provider
│   ├── report_generator.py     # Printable report generator
│   └── requirements.txt        # Python dependencies
├── docs/
│   ├── HOW_IT_WORKS_EN.md      # Brief visual guide (English)
│   └── COMO_FUNCIONA_ES.md     # Brief visual guide (Spanish)
├── ARCHITECTURE.md             # Detailed technical architecture spec (ES)
├── Iniciar_AMAC.bat            # Windows 1-click launcher
├── README.md                   # English documentation (default)
├── README.es.md                # Spanish documentation
└── LICENSE                     # MIT License
```

---

## 👥 Team AMAC & License

Developed by **Team AMAC** for the **NASA Space Apps Challenge 2026**.  
Licensed under the [MIT License](LICENSE) — open for educational, agricultural, and research use.
