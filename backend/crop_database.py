"""
crop_database.py - Base de datos completa de cultivos para AMAC
================================================================
Contiene información detallada de 26+ cultivos con sus características
agronómicas, tolerancias, valor comercial y compatibilidades para
rotación.

Cada cultivo se define como un diccionario con las siguientes claves:
    - name: nombre común en español
    - scientific_name: nombre científico
    - category: cereal | leguminosa | hortaliza | forrajero | cobertura |
                oleaginosa | tubérculo | pseudocereal
    - temp_min / temp_max: rango óptimo de temperatura (°C)
    - water_need: "bajo" (<300 mm), "medio" (300-600 mm), "alto" (>600 mm)
    - water_need_mm: (min, max) del ciclo
    - growing_season_days: duración promedio del ciclo (días)
    - nitrogen_fixer: si fija nitrógeno atmosférico
    - root_depth: "superficial" | "media" | "profunda"
    - organic_matter_contribution: "bajo" | "medio" | "alto"
    - erosion_control: "bajo" | "medio" | "alto"
    - pest_break: si rompe ciclos de plagas en rotación
    - drought_tolerance: "bajo" | "medio" | "alto"
    - frost_tolerance: "bajo" | "medio" | "alto"
    - market_value: "bajo" | "medio" | "alto"
    - forage_value: "bajo" | "medio" | "alto"
    - soil_improvement_score: puntaje de mejora de suelo (1-10)
    - compatible_rotations: lista de cultivos que funcionan en secuencia
    - benefits: beneficios en español
    - risks: riesgos en español
    - planting_months: meses recomendados de siembra (1-12)
"""

from typing import Dict, List, Optional, Any

# --------------------------------------------------------------------------- #
#  Base de datos de cultivos
# --------------------------------------------------------------------------- #

CROPS_DB: List[Dict[str, Any]] = [
    {
        "name": "Maíz",
        "scientific_name": "Zea mays",
        "category": "cereal",
        "temp_min": 10,
        "temp_max": 35,
        "water_need": "alto",
        "water_need_mm": (500, 800),
        "growing_season_days": 120,
        "nitrogen_fixer": False,
        "root_depth": "media",
        "organic_matter_contribution": "medio",
        "erosion_control": "medio",
        "pest_break": False,
        "drought_tolerance": "medio",
        "frost_tolerance": "bajo",
        "market_value": "alto",
        "forage_value": "alto",
        "soil_improvement_score": 4,
        "compatible_rotations": ["Soja", "Trigo", "Avena", "Vicia", "Trébol"],
        "benefits": [
            "Alto rendimiento por hectárea",
            "Gran versatilidad de uso (grano, silo, forraje)",
            "Buen aporte de rastrojo al suelo",
        ],
        "risks": [
            "Alta demanda de nitrógeno",
            "Susceptible a sequía en floración",
            "Favorece plagas como gusano cogollero",
        ],
        "planting_months": [9, 10, 11, 12],
    },
    {
        "name": "Trigo",
        "scientific_name": "Triticum aestivum",
        "category": "cereal",
        "temp_min": 3,
        "temp_max": 25,
        "water_need": "medio",
        "water_need_mm": (350, 550),
        "growing_season_days": 150,
        "nitrogen_fixer": False,
        "root_depth": "media",
        "organic_matter_contribution": "medio",
        "erosion_control": "alto",
        "pest_break": True,
        "drought_tolerance": "medio",
        "frost_tolerance": "alto",
        "market_value": "alto",
        "forage_value": "medio",
        "soil_improvement_score": 5,
        "compatible_rotations": ["Soja", "Maíz", "Girasol", "Garbanzo", "Lenteja"],
        "benefits": [
            "Excelente cobertura invernal del suelo",
            "Rompe ciclos de plagas de cultivos estivales",
            "Alto valor comercial y demanda estable",
        ],
        "risks": [
            "Sensible a exceso de humedad (fusarium)",
            "Requiere fertilización nitrogenada",
            "Puede agotar reservas de agua para el cultivo siguiente",
        ],
        "planting_months": [5, 6, 7],
    },
    {
        "name": "Soja",
        "scientific_name": "Glycine max",
        "category": "leguminosa",
        "temp_min": 15,
        "temp_max": 35,
        "water_need": "medio",
        "water_need_mm": (400, 600),
        "growing_season_days": 130,
        "nitrogen_fixer": True,
        "root_depth": "media",
        "organic_matter_contribution": "bajo",
        "erosion_control": "bajo",
        "pest_break": True,
        "drought_tolerance": "medio",
        "frost_tolerance": "bajo",
        "market_value": "alto",
        "forage_value": "bajo",
        "soil_improvement_score": 6,
        "compatible_rotations": ["Maíz", "Trigo", "Sorgo", "Avena", "Cebada"],
        "benefits": [
            "Fija nitrógeno atmosférico (60-100 kg N/ha)",
            "Alto valor comercial internacional",
            "Buen cultivo para rotación con gramíneas",
        ],
        "risks": [
            "Bajo aporte de rastrojo (rápida descomposición)",
            "Susceptible a nematodos si se repite",
            "Sensible a heladas tempranas",
        ],
        "planting_months": [10, 11, 12],
    },
    {
        "name": "Arroz",
        "scientific_name": "Oryza sativa",
        "category": "cereal",
        "temp_min": 20,
        "temp_max": 38,
        "water_need": "alto",
        "water_need_mm": (900, 1200),
        "growing_season_days": 140,
        "nitrogen_fixer": False,
        "root_depth": "superficial",
        "organic_matter_contribution": "medio",
        "erosion_control": "bajo",
        "pest_break": False,
        "drought_tolerance": "bajo",
        "frost_tolerance": "bajo",
        "market_value": "alto",
        "forage_value": "bajo",
        "soil_improvement_score": 3,
        "compatible_rotations": ["Soja", "Trébol", "Alfalfa"],
        "benefits": [
            "Alto rendimiento en zonas húmedas",
            "Alimento básico con demanda constante",
            "Adaptado a suelos inundables",
        ],
        "risks": [
            "Requiere grandes cantidades de agua",
            "Emisión de metano en cultivo inundado",
            "Limitado a suelos con capacidad de retención hídrica",
        ],
        "planting_months": [10, 11],
    },
    {
        "name": "Papa",
        "scientific_name": "Solanum tuberosum",
        "category": "tubérculo",
        "temp_min": 7,
        "temp_max": 24,
        "water_need": "medio",
        "water_need_mm": (400, 600),
        "growing_season_days": 120,
        "nitrogen_fixer": False,
        "root_depth": "superficial",
        "organic_matter_contribution": "bajo",
        "erosion_control": "bajo",
        "pest_break": True,
        "drought_tolerance": "bajo",
        "frost_tolerance": "medio",
        "market_value": "alto",
        "forage_value": "bajo",
        "soil_improvement_score": 3,
        "compatible_rotations": ["Trigo", "Avena", "Vicia", "Trébol", "Centeno"],
        "benefits": [
            "Alto valor nutricional y comercial",
            "Adaptado a climas templados y fríos",
            "Rompe ciclos de plagas de gramíneas",
        ],
        "risks": [
            "Susceptible a tizón tardío",
            "Sensible a heladas fuertes",
            "Requiere suelos bien drenados",
        ],
        "planting_months": [7, 8, 9, 10],
    },
    {
        "name": "Frijol",
        "scientific_name": "Phaseolus vulgaris",
        "category": "leguminosa",
        "temp_min": 15,
        "temp_max": 30,
        "water_need": "medio",
        "water_need_mm": (300, 500),
        "growing_season_days": 90,
        "nitrogen_fixer": True,
        "root_depth": "superficial",
        "organic_matter_contribution": "medio",
        "erosion_control": "bajo",
        "pest_break": True,
        "drought_tolerance": "bajo",
        "frost_tolerance": "bajo",
        "market_value": "medio",
        "forage_value": "bajo",
        "soil_improvement_score": 6,
        "compatible_rotations": ["Maíz", "Sorgo", "Trigo", "Arroz"],
        "benefits": [
            "Fija nitrógeno atmosférico",
            "Ciclo corto permite doble cultivo",
            "Alto valor proteico y nutricional",
        ],
        "risks": [
            "Sensible a exceso de humedad",
            "Susceptible a plagas como mosca blanca",
            "Bajo aporte de cobertura al suelo",
        ],
        "planting_months": [2, 3, 8, 9],
    },
    {
        "name": "Sorgo",
        "scientific_name": "Sorghum bicolor",
        "category": "cereal",
        "temp_min": 15,
        "temp_max": 40,
        "water_need": "bajo",
        "water_need_mm": (250, 400),
        "growing_season_days": 110,
        "nitrogen_fixer": False,
        "root_depth": "profunda",
        "organic_matter_contribution": "medio",
        "erosion_control": "alto",
        "pest_break": False,
        "drought_tolerance": "alto",
        "frost_tolerance": "bajo",
        "market_value": "medio",
        "forage_value": "alto",
        "soil_improvement_score": 5,
        "compatible_rotations": ["Soja", "Maíz", "Girasol", "Vicia"],
        "benefits": [
            "Excelente tolerancia a la sequía",
            "Sistema radicular profundo que mejora estructura del suelo",
            "Versatilidad: grano, silo, pastoreo",
        ],
        "risks": [
            "Puede producir ácido cianhídrico (toxicidad en rebrote)",
            "Menor valor comercial que maíz",
            "Hospedante de pulgón verde",
        ],
        "planting_months": [10, 11, 12],
    },
    {
        "name": "Girasol",
        "scientific_name": "Helianthus annuus",
        "category": "oleaginosa",
        "temp_min": 10,
        "temp_max": 34,
        "water_need": "medio",
        "water_need_mm": (350, 550),
        "growing_season_days": 120,
        "nitrogen_fixer": False,
        "root_depth": "profunda",
        "organic_matter_contribution": "medio",
        "erosion_control": "medio",
        "pest_break": True,
        "drought_tolerance": "alto",
        "frost_tolerance": "bajo",
        "market_value": "alto",
        "forage_value": "bajo",
        "soil_improvement_score": 5,
        "compatible_rotations": ["Trigo", "Soja", "Maíz", "Avena"],
        "benefits": [
            "Raíz pivotante profunda que descompacta suelos",
            "Buena tolerancia a sequía",
            "Alto valor del aceite extraído",
        ],
        "risks": [
            "Susceptible a enfermedades fúngicas (Sclerotinia)",
            "No debe repetirse en la misma parcela por 4+ años",
            "Agota nutrientes del subsuelo",
        ],
        "planting_months": [8, 9, 10, 11],
    },
    {
        "name": "Avena",
        "scientific_name": "Avena sativa",
        "category": "cereal",
        "temp_min": 3,
        "temp_max": 25,
        "water_need": "medio",
        "water_need_mm": (300, 500),
        "growing_season_days": 130,
        "nitrogen_fixer": False,
        "root_depth": "media",
        "organic_matter_contribution": "alto",
        "erosion_control": "alto",
        "pest_break": True,
        "drought_tolerance": "medio",
        "frost_tolerance": "alto",
        "market_value": "medio",
        "forage_value": "alto",
        "soil_improvement_score": 7,
        "compatible_rotations": ["Soja", "Maíz", "Girasol", "Papa"],
        "benefits": [
            "Excelente cultivo de cobertura invernal",
            "Alto aporte de materia orgánica",
            "Suprime malezas eficientemente",
        ],
        "risks": [
            "Susceptible a roya de la hoja",
            "Menor valor de grano que trigo",
            "Puede competir por agua con cultivo siguiente",
        ],
        "planting_months": [3, 4, 5, 6],
    },
    {
        "name": "Cebada",
        "scientific_name": "Hordeum vulgare",
        "category": "cereal",
        "temp_min": 4,
        "temp_max": 28,
        "water_need": "bajo",
        "water_need_mm": (250, 400),
        "growing_season_days": 120,
        "nitrogen_fixer": False,
        "root_depth": "media",
        "organic_matter_contribution": "medio",
        "erosion_control": "alto",
        "pest_break": True,
        "drought_tolerance": "alto",
        "frost_tolerance": "alto",
        "market_value": "medio",
        "forage_value": "alto",
        "soil_improvement_score": 5,
        "compatible_rotations": ["Soja", "Maíz", "Girasol", "Lenteja"],
        "benefits": [
            "Ciclo corto que libera el lote temprano",
            "Buena tolerancia a frío y sequía",
            "Demanda cervecera estable",
        ],
        "risks": [
            "Calidad cervecera exige manejo preciso de N",
            "Susceptible a pulgones y carbón",
            "Menor rendimiento que trigo",
        ],
        "planting_months": [5, 6, 7],
    },
    {
        "name": "Centeno",
        "scientific_name": "Secale cereale",
        "category": "cereal",
        "temp_min": -5,
        "temp_max": 25,
        "water_need": "bajo",
        "water_need_mm": (200, 350),
        "growing_season_days": 140,
        "nitrogen_fixer": False,
        "root_depth": "profunda",
        "organic_matter_contribution": "alto",
        "erosion_control": "alto",
        "pest_break": True,
        "drought_tolerance": "alto",
        "frost_tolerance": "alto",
        "market_value": "bajo",
        "forage_value": "medio",
        "soil_improvement_score": 8,
        "compatible_rotations": ["Soja", "Maíz", "Girasol", "Papa"],
        "benefits": [
            "Máxima tolerancia al frío entre cereales",
            "Excelente cultivo de cobertura y anti-erosión",
            "Crece en suelos pobres y arenosos",
        ],
        "risks": [
            "Bajo valor comercial del grano",
            "Alelopatía puede afectar cultivos siguientes si no se maneja bien",
            "Puede convertirse en maleza si se deja granar",
        ],
        "planting_months": [3, 4, 5],
    },
    {
        "name": "Alfalfa",
        "scientific_name": "Medicago sativa",
        "category": "forrajero",
        "temp_min": 5,
        "temp_max": 30,
        "water_need": "medio",
        "water_need_mm": (400, 700),
        "growing_season_days": 365,  # Perenne, múltiples cortes al año
        "nitrogen_fixer": True,
        "root_depth": "profunda",
        "organic_matter_contribution": "alto",
        "erosion_control": "alto",
        "pest_break": True,
        "drought_tolerance": "alto",
        "frost_tolerance": "alto",
        "market_value": "medio",
        "forage_value": "alto",
        "soil_improvement_score": 10,
        "compatible_rotations": ["Maíz", "Trigo", "Sorgo", "Girasol"],
        "benefits": [
            "Fija hasta 300 kg N/ha/año",
            "Raíz pivotante profunda que descompacta suelos",
            "Produce forraje de altísima calidad durante 3-5 años",
        ],
        "risks": [
            "Ocupa el lote durante varios años",
            "Susceptible a pulgón y trips",
            "Requiere suelos bien drenados (no tolera encharcamiento)",
        ],
        "planting_months": [3, 4, 9, 10],
    },
    {
        "name": "Trébol",
        "scientific_name": "Trifolium spp.",
        "category": "forrajero",
        "temp_min": 5,
        "temp_max": 28,
        "water_need": "medio",
        "water_need_mm": (350, 550),
        "growing_season_days": 365,
        "nitrogen_fixer": True,
        "root_depth": "media",
        "organic_matter_contribution": "alto",
        "erosion_control": "alto",
        "pest_break": True,
        "drought_tolerance": "medio",
        "frost_tolerance": "alto",
        "market_value": "bajo",
        "forage_value": "alto",
        "soil_improvement_score": 9,
        "compatible_rotations": ["Maíz", "Trigo", "Arroz", "Sorgo"],
        "benefits": [
            "Excelente fijador de nitrógeno",
            "Ideal como cultivo de cobertura y abono verde",
            "Protege el suelo de erosión y mejora estructura",
        ],
        "risks": [
            "Bajo valor comercial como grano",
            "Puede ser invadido por gramíneas agresivas",
            "Sensible a sequía prolongada",
        ],
        "planting_months": [3, 4, 5, 9, 10],
    },
    {
        "name": "Vicia",
        "scientific_name": "Vicia sativa",
        "category": "cobertura",
        "temp_min": 2,
        "temp_max": 25,
        "water_need": "bajo",
        "water_need_mm": (200, 400),
        "growing_season_days": 120,
        "nitrogen_fixer": True,
        "root_depth": "media",
        "organic_matter_contribution": "alto",
        "erosion_control": "alto",
        "pest_break": True,
        "drought_tolerance": "medio",
        "frost_tolerance": "alto",
        "market_value": "bajo",
        "forage_value": "medio",
        "soil_improvement_score": 9,
        "compatible_rotations": ["Maíz", "Sorgo", "Girasol", "Trigo"],
        "benefits": [
            "Fija 80-150 kg N/ha como abono verde",
            "Excelente cultivo de cobertura invernal",
            "Se puede asociar con gramíneas (vicia + avena)",
        ],
        "risks": [
            "Sin valor comercial como grano (uso solo forrajero/cobertura)",
            "Puede ser hospedante de pulgón negro",
            "Requiere inoculación con Rhizobium específico",
        ],
        "planting_months": [3, 4, 5],
    },
    {
        "name": "Lenteja",
        "scientific_name": "Lens culinaris",
        "category": "leguminosa",
        "temp_min": 5,
        "temp_max": 25,
        "water_need": "bajo",
        "water_need_mm": (200, 350),
        "growing_season_days": 110,
        "nitrogen_fixer": True,
        "root_depth": "superficial",
        "organic_matter_contribution": "medio",
        "erosion_control": "bajo",
        "pest_break": True,
        "drought_tolerance": "medio",
        "frost_tolerance": "medio",
        "market_value": "alto",
        "forage_value": "bajo",
        "soil_improvement_score": 6,
        "compatible_rotations": ["Trigo", "Cebada", "Avena", "Centeno"],
        "benefits": [
            "Alto valor comercial y nutricional",
            "Fija nitrógeno atmosférico",
            "Ciclo corto que permite doble cultivo",
        ],
        "risks": [
            "Sensible a exceso de lluvias en cosecha",
            "Susceptible a Ascochyta (tizón)",
            "Bajo porte dificulta cosecha mecánica",
        ],
        "planting_months": [5, 6, 7],
    },
    {
        "name": "Garbanzo",
        "scientific_name": "Cicer arietinum",
        "category": "leguminosa",
        "temp_min": 8,
        "temp_max": 30,
        "water_need": "bajo",
        "water_need_mm": (250, 400),
        "growing_season_days": 130,
        "nitrogen_fixer": True,
        "root_depth": "profunda",
        "organic_matter_contribution": "medio",
        "erosion_control": "medio",
        "pest_break": True,
        "drought_tolerance": "alto",
        "frost_tolerance": "medio",
        "market_value": "alto",
        "forage_value": "bajo",
        "soil_improvement_score": 7,
        "compatible_rotations": ["Trigo", "Maíz", "Cebada", "Sorgo"],
        "benefits": [
            "Alto valor comercial (exportación)",
            "Buena tolerancia a sequía",
            "Fija nitrógeno y mejora estructura del suelo",
        ],
        "risks": [
            "Sensible a exceso de humedad (fusarium, rabia)",
            "Requiere control de malezas cuidadoso",
            "No tolera heladas severas en floración",
        ],
        "planting_months": [5, 6, 7],
    },
    {
        "name": "Canola",
        "scientific_name": "Brassica napus",
        "category": "oleaginosa",
        "temp_min": 3,
        "temp_max": 25,
        "water_need": "medio",
        "water_need_mm": (350, 500),
        "growing_season_days": 150,
        "nitrogen_fixer": False,
        "root_depth": "profunda",
        "organic_matter_contribution": "medio",
        "erosion_control": "medio",
        "pest_break": True,
        "drought_tolerance": "medio",
        "frost_tolerance": "alto",
        "market_value": "alto",
        "forage_value": "bajo",
        "soil_improvement_score": 6,
        "compatible_rotations": ["Trigo", "Soja", "Maíz", "Cebada"],
        "benefits": [
            "Alto valor del aceite (premium)",
            "Raíz pivotante descompacta suelos",
            "Excelente para romper ciclo de enfermedades en gramíneas",
        ],
        "risks": [
            "Susceptible a plagas (pulgones, polilla)",
            "No repetir en la misma parcela por 3+ años",
            "Requiere buen control de malezas en implantación",
        ],
        "planting_months": [4, 5, 6],
    },
    {
        "name": "Algodón",
        "scientific_name": "Gossypium hirsutum",
        "category": "oleaginosa",
        "temp_min": 18,
        "temp_max": 38,
        "water_need": "alto",
        "water_need_mm": (500, 800),
        "growing_season_days": 160,
        "nitrogen_fixer": False,
        "root_depth": "profunda",
        "organic_matter_contribution": "bajo",
        "erosion_control": "bajo",
        "pest_break": True,
        "drought_tolerance": "medio",
        "frost_tolerance": "bajo",
        "market_value": "alto",
        "forage_value": "bajo",
        "soil_improvement_score": 2,
        "compatible_rotations": ["Maíz", "Sorgo", "Soja", "Vicia"],
        "benefits": [
            "Alto valor comercial de la fibra",
            "Adaptado a climas cálidos y semiáridos con riego",
            "Subproductos (semilla) con valor forrajero",
        ],
        "risks": [
            "Alto costo de insumos (plaguicidas)",
            "Agota nutrientes del suelo si no se rota",
            "Altamente susceptible a picudo del algodón",
        ],
        "planting_months": [10, 11],
    },
    {
        "name": "Caña de azúcar",
        "scientific_name": "Saccharum officinarum",
        "category": "cereal",
        "temp_min": 20,
        "temp_max": 40,
        "water_need": "alto",
        "water_need_mm": (1000, 1500),
        "growing_season_days": 365,
        "nitrogen_fixer": False,
        "root_depth": "profunda",
        "organic_matter_contribution": "medio",
        "erosion_control": "medio",
        "pest_break": False,
        "drought_tolerance": "medio",
        "frost_tolerance": "bajo",
        "market_value": "alto",
        "forage_value": "medio",
        "soil_improvement_score": 3,
        "compatible_rotations": ["Soja", "Frijol", "Maní"],
        "benefits": [
            "Alto rendimiento energético (azúcar, etanol)",
            "Cultivo perenne que reduce costos de implantación",
            "Genera gran volumen de biomasa",
        ],
        "risks": [
            "Requiere mucha agua",
            "Monocultivo prolongado degrada suelos",
            "Sensible a heladas",
        ],
        "planting_months": [2, 3, 4, 9, 10],
    },
    {
        "name": "Mijo",
        "scientific_name": "Panicum miliaceum",
        "category": "cereal",
        "temp_min": 15,
        "temp_max": 38,
        "water_need": "bajo",
        "water_need_mm": (200, 350),
        "growing_season_days": 75,
        "nitrogen_fixer": False,
        "root_depth": "media",
        "organic_matter_contribution": "medio",
        "erosion_control": "medio",
        "pest_break": True,
        "drought_tolerance": "alto",
        "frost_tolerance": "bajo",
        "market_value": "bajo",
        "forage_value": "medio",
        "soil_improvement_score": 5,
        "compatible_rotations": ["Soja", "Trigo", "Avena", "Lenteja"],
        "benefits": [
            "Ciclo muy corto (ideal para siembras tardías)",
            "Excelente tolerancia a sequía",
            "Bajo costo de producción",
        ],
        "risks": [
            "Mercado limitado",
            "Bajo rendimiento comparado con maíz o sorgo",
            "Susceptible a pájaros en maduración",
        ],
        "planting_months": [11, 12, 1],
    },
    {
        "name": "Quinoa",
        "scientific_name": "Chenopodium quinoa",
        "category": "pseudocereal",
        "temp_min": 3,
        "temp_max": 30,
        "water_need": "bajo",
        "water_need_mm": (200, 400),
        "growing_season_days": 120,
        "nitrogen_fixer": False,
        "root_depth": "media",
        "organic_matter_contribution": "medio",
        "erosion_control": "medio",
        "pest_break": True,
        "drought_tolerance": "alto",
        "frost_tolerance": "medio",
        "market_value": "alto",
        "forage_value": "bajo",
        "soil_improvement_score": 5,
        "compatible_rotations": ["Papa", "Trigo", "Avena", "Frijol"],
        "benefits": [
            "Alto valor nutricional y comercial (superalimento)",
            "Tolerante a salinidad y sequía",
            "Adaptable a altitudes elevadas",
        ],
        "risks": [
            "Susceptible a mildiu (Peronospora)",
            "Requiere manejo postcosecha cuidadoso",
            "Rendimientos variables según condiciones",
        ],
        "planting_months": [9, 10, 11],
    },
    {
        "name": "Amaranto",
        "scientific_name": "Amaranthus spp.",
        "category": "pseudocereal",
        "temp_min": 15,
        "temp_max": 35,
        "water_need": "bajo",
        "water_need_mm": (200, 400),
        "growing_season_days": 100,
        "nitrogen_fixer": False,
        "root_depth": "media",
        "organic_matter_contribution": "medio",
        "erosion_control": "medio",
        "pest_break": True,
        "drought_tolerance": "alto",
        "frost_tolerance": "bajo",
        "market_value": "alto",
        "forage_value": "medio",
        "soil_improvement_score": 5,
        "compatible_rotations": ["Maíz", "Frijol", "Trigo", "Papa"],
        "benefits": [
            "Alto contenido proteico del grano",
            "Muy tolerante a sequía y suelos pobres",
            "Hojas comestibles (doble propósito)",
        ],
        "risks": [
            "Mercado de nicho (volumen limitado)",
            "Cosecha complicada (grano muy pequeño)",
            "Algunas especies son malezas invasoras",
        ],
        "planting_months": [9, 10, 11],
    },
    {
        "name": "Mostaza",
        "scientific_name": "Sinapis alba",
        "category": "cobertura",
        "temp_min": 5,
        "temp_max": 25,
        "water_need": "bajo",
        "water_need_mm": (200, 350),
        "growing_season_days": 90,
        "nitrogen_fixer": False,
        "root_depth": "profunda",
        "organic_matter_contribution": "medio",
        "erosion_control": "alto",
        "pest_break": True,
        "drought_tolerance": "medio",
        "frost_tolerance": "alto",
        "market_value": "bajo",
        "forage_value": "bajo",
        "soil_improvement_score": 7,
        "compatible_rotations": ["Maíz", "Soja", "Trigo", "Sorgo"],
        "benefits": [
            "Biofumigante natural (suprime nematodos y patógenos)",
            "Raíz pivotante descompacta suelos",
            "Rápido crecimiento como cobertura",
        ],
        "risks": [
            "Puede ser hospedante de plagas de crucíferas",
            "No repetir con canola u otras brassicáceas",
            "Semilla puede persistir como maleza",
        ],
        "planting_months": [3, 4, 5],
    },
    {
        "name": "Rábano forrajero",
        "scientific_name": "Raphanus sativus var. oleiferus",
        "category": "cobertura",
        "temp_min": 5,
        "temp_max": 25,
        "water_need": "bajo",
        "water_need_mm": (150, 300),
        "growing_season_days": 60,
        "nitrogen_fixer": False,
        "root_depth": "profunda",
        "organic_matter_contribution": "medio",
        "erosion_control": "alto",
        "pest_break": True,
        "drought_tolerance": "medio",
        "frost_tolerance": "medio",
        "market_value": "bajo",
        "forage_value": "medio",
        "soil_improvement_score": 8,
        "compatible_rotations": ["Maíz", "Soja", "Sorgo", "Trigo"],
        "benefits": [
            "Raíz gruesa que rompe capas compactadas (biodrilling)",
            "Ciclo muy corto ideal como cultivo puente",
            "Recicla nutrientes de capas profundas",
        ],
        "risks": [
            "Sin valor comercial de grano",
            "Olor desagradable al descomponerse",
            "Puede ser afectado por heladas severas antes de completar su efecto",
        ],
        "planting_months": [3, 4, 5],
    },
    {
        "name": "Nabo forrajero",
        "scientific_name": "Brassica rapa",
        "category": "cobertura",
        "temp_min": 5,
        "temp_max": 25,
        "water_need": "bajo",
        "water_need_mm": (150, 300),
        "growing_season_days": 70,
        "nitrogen_fixer": False,
        "root_depth": "profunda",
        "organic_matter_contribution": "medio",
        "erosion_control": "alto",
        "pest_break": True,
        "drought_tolerance": "medio",
        "frost_tolerance": "alto",
        "market_value": "bajo",
        "forage_value": "medio",
        "soil_improvement_score": 7,
        "compatible_rotations": ["Maíz", "Soja", "Trigo", "Sorgo"],
        "benefits": [
            "Descompacta suelos con raíz pivotante",
            "Buen valor forrajero (hojas y raíz)",
            "Rápida cobertura del suelo",
        ],
        "risks": [
            "No repetir con otras crucíferas (hernia de las crucíferas)",
            "Puede atraer pulgones",
            "Bajo valor comercial",
        ],
        "planting_months": [3, 4, 5],
    },
    {
        "name": "Lupino",
        "scientific_name": "Lupinus spp.",
        "category": "leguminosa",
        "temp_min": 5,
        "temp_max": 25,
        "water_need": "bajo",
        "water_need_mm": (250, 400),
        "growing_season_days": 140,
        "nitrogen_fixer": True,
        "root_depth": "profunda",
        "organic_matter_contribution": "alto",
        "erosion_control": "alto",
        "pest_break": True,
        "drought_tolerance": "medio",
        "frost_tolerance": "medio",
        "market_value": "medio",
        "forage_value": "medio",
        "soil_improvement_score": 9,
        "compatible_rotations": ["Trigo", "Cebada", "Avena", "Centeno"],
        "benefits": [
            "Fija grandes cantidades de nitrógeno (100-200 kg N/ha)",
            "Adapta suelos ácidos y arenosos",
            "Grano con alto contenido proteico",
        ],
        "risks": [
            "Algunas variedades contienen alcaloides tóxicos",
            "Mercado limitado en algunas regiones",
            "Crecimiento inicial lento (competencia con malezas)",
        ],
        "planting_months": [4, 5, 6],
    },
]


# --------------------------------------------------------------------------- #
#  Funciones de consulta
# --------------------------------------------------------------------------- #

def get_all_crops() -> List[Dict[str, Any]]:
    """
    Retorna la lista completa de cultivos disponibles en la base de datos.

    Returns:
        Lista de diccionarios con la información de cada cultivo.
    """
    return CROPS_DB


def get_crop(name: str) -> Optional[Dict[str, Any]]:
    """
    Busca un cultivo por su nombre (case-insensitive).

    Args:
        name: Nombre del cultivo en español.

    Returns:
        Diccionario con la información del cultivo, o None si no se encuentra.
    """
    name_lower = name.lower().strip()
    for crop in CROPS_DB:
        if crop["name"].lower() == name_lower:
            return crop
    return None


def get_crops_by_category(category: str) -> List[Dict[str, Any]]:
    """
    Filtra cultivos por categoría.

    Args:
        category: Una de: cereal, leguminosa, hortaliza, forrajero, cobertura,
                  oleaginosa, tubérculo, pseudocereal.

    Returns:
        Lista de cultivos que pertenecen a la categoría indicada.
    """
    cat_lower = category.lower().strip()
    return [c for c in CROPS_DB if c["category"].lower() == cat_lower]


def get_compatible_crops(
    current_crop: str,
    soil_type: str,
    climate_data: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Filtra cultivos compatibles con el cultivo actual, tipo de suelo y clima.

    Criterios de filtrado:
        1. El cultivo aparece en la lista compatible_rotations del cultivo actual.
        2. Si hay datos climáticos, la temperatura promedio cae dentro del rango
           del cultivo candidato.
        3. Se ajusta según el tipo de suelo (ej. suelos arenosos favorecen
           cultivos tolerantes a sequía).

    Args:
        current_crop: Nombre del cultivo actual.
        soil_type: Tipo de suelo (arcilloso, arenoso, limoso, franco, etc.).
        climate_data: Datos climáticos (resultado de fetch_climate_data), opcional.

    Returns:
        Lista de cultivos compatibles ordenados por soil_improvement_score.
    """
    crop = get_crop(current_crop)
    if crop is None:
        # Si no encontramos el cultivo actual, devolvemos todos
        return CROPS_DB

    # Paso 1: filtrar por compatibilidad de rotación declarada
    compatible_names = {n.lower() for n in crop["compatible_rotations"]}
    candidates = [
        c for c in CROPS_DB
        if c["name"].lower() in compatible_names and c["name"] != crop["name"]
    ]

    # Paso 2: filtrar por temperatura si hay datos climáticos
    if climate_data:
        summary = climate_data.get("summary", {})
        t2m = summary.get("T2M", {})
        avg_temp = t2m.get("promedio")
        if avg_temp is not None:
            candidates = [
                c for c in candidates
                if c["temp_min"] <= avg_temp <= c["temp_max"]
            ]

    # Paso 3: ajuste por tipo de suelo
    soil_lower = soil_type.lower().strip()
    if soil_lower == "arenoso":
        # Priorizar cultivos tolerantes a sequía
        candidates = [
            c for c in candidates
            if c["drought_tolerance"] in ("medio", "alto")
        ]
    elif soil_lower == "arcilloso":
        # Priorizar cultivos con raíces que descompacten
        candidates.sort(
            key=lambda c: (
                0 if c["root_depth"] == "profunda"
                else 1 if c["root_depth"] == "media"
                else 2
            )
        )

    # Ordenar por puntaje de mejora de suelo (descendente)
    candidates.sort(key=lambda c: c["soil_improvement_score"], reverse=True)

    return candidates
