<div align="center">

# 🌱 How TERRASHIFT (AMAC) Works
### A 2-Minute Visual Walkthrough

[![English](https://img.shields.io/badge/Language-English-1B4965?style=for-the-badge)](HOW_IT_WORKS_EN.md)
[![Español](https://img.shields.io/badge/Idioma-Español-2D6A4F?style=for-the-badge)](COMO_FUNCIONA_ES.md)
[![Back to README](https://img.shields.io/badge/⬅_Back_to-README-40916C?style=for-the-badge)](../README.md)

</div>

---

## 🧭 What Problem Does It Solve?

In one sentence: **TERRASHIFT turns complex NASA satellite data and soil maps into a clear, personalized 3-year crop rotation plan that protects soil, saves water, and cuts fertilizer costs.**

---

## 🔄 How the App Works in 4 Simple Steps

```text
  [1. Choose Role]  ──▶  [2. Pick Your Farm]  ──▶  [3. Adjust Priorities]  ──▶  [4. Get Action Plan]
   Farmer / Advisor       Satellite Map +           Water, Soil, Profit,         Best Rotation +
   / Institution          ISRIC SoilGrids           Frost & Pest Sliders         1-Page Field Report
```

### Step 1 — Choose Who You Are
When you open the app, you pick your perspective:
- **🚜 Farmer:** Clean, friendly interface with traffic-light alerts (🟢 Safe / 🟡 Caution / 🔴 Risk) and zero technical jargon.
- **🔬 Technical Advisor:** Full agronomic workbench to manage multiple farms, inspect soil chemistry, and fine-tune decision weights.
- **🏛️ Institution (INDAP / Municipality):** Big-picture regional view across Biobío communes (Los Ángeles, Mulchén, Cabrero, Santa Bárbara).

### Step 2 — Click Your Farm on the Map
In **My Farm (`Mi Predio`)**, you click anywhere on the interactive satellite map (or pick a pilot farm).  
Behind the scenes, TERRASHIFT automatically fetches:
- **Soil profile** from **ISRIC SoilGrids v2.0** (clay, sand, silt, pH, organic carbon, CEC) and classifies it (e.g., volcanic *Trumao* loam or sandy soil).
- **Climate history & risks** from **NASA POWER** (temperatures, rain, solar radiation, frost risk, and drought trends).

### Step 3 — Compare 3 Strategies Tailored to Your Priorities
In **3 Strategies (`3 Estrategias`)**, you move simple priority sliders (*Save Water*, *Improve Soil*, *Economic Return*, *Pest Control*).  
Our **MCDA Decision Engine** instantly scores **3 strategies** side by side:
1. **Traditional Monoculture** *(Baseline — warns about bare-soil erosion and high urea cost)*
2. **Soil & Biomass Regeneration ⭐** *(Adds winter cover crops like Vicia villosa to fix natural nitrogen and keep 0 days of bare soil)*
3. **Water Resilience 💧** *(Pairs deep-rooted sorghum, rye, and sunflower for drought-prone fields)*

### Step 4 — Print or Share the 1-Page Field Report
In **Official Report (`Informe Oficial`)**, TERRASHIFT builds a clean, 1-page printable A4 summary with:
- Farm coordinates & soil health snapshot
- Frost & drought traffic lights
- Step-by-step seasonal calendar of what to plant and when

---

## ✨ Why Judges & Farmers Love It

- **Works even offline / without setup:** Open `frontend/index.html` in any browser and every core view works immediately.
- **Real science, simple UI:** Powered by NASA Earth Observations (POWER, SMAP, GPM, Landsat/MODIS, ECOSTRESS, GRACE) and ISRIC SoilGrids v2.0, yet readable in plain language by a family farmer.
- **Built for real extension workflows:** Bridges the gap between space agencies, agricultural advisors, and farmers in the field.
