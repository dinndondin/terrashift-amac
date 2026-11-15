/* ═══════════════════════════════════════════════════
   AMAC — rotation.js  ·  Motor de Estrategias y Plan de Acción
   NASA Space Apps Challenge 2026
   ═══════════════════════════════════════════════════ */

// ─── 3 Estrategias Centrales del Plan de Acción ───
function getMockStrategies() {
    return [
        {
            id: 'strategy_actual',
            name: '1. Rotación Tradicional (Línea Base)',
            tag: '⚠️ Línea Base del Productor',
            tagClass: 'badge-baseline',
            overall_score: 58,
            recommended: false,
            highlightSummary: 'Monocultivo tradicional con suelo descubierto en invierno. Alta vulnerabilidad a erosión y malezas.',
            scores: {
                water_conservation: 52,
                soil_health: 48,
                economic_return: 82,
                pest_management: 45,
                erosion_control: 40,
                nitrogen_fixation: 55
            },
            sequence: [
                { crop: 'Soja', months: 'Oct–Mar', color: '#40916C', desc: 'Cosecha gruesa comercial' },
                { crop: 'Barbecho Químico (Suelo Desnudo)', months: 'Abr–Sep', color: '#6C757D', desc: 'Período vulnerable a erosión' },
                { crop: 'Maíz', months: 'Oct–Mar', color: '#2C7DA0', desc: 'Alta extracción de nutrientes' },
                { crop: 'Barbecho Invernal', months: 'Abr–Sep', color: '#ADB5BD', desc: 'Pérdida de humedad por evaporación' }
            ],
            metrics: {
                waterDemand: '780 mm/año (Alta)',
                nitrogenBalance: '-45 kg N/ha (Déficit)',
                bareSoilDays: '150 días/año sin cobertura',
                erosionRisk: 'Alto (Alerta NASA POWER)'
            },
            benefits: [
                'Manejo agronómico tradicional conocido por el productor',
                'Comercialización rápida e inmediata en mercados de cereales',
                'Menor gasto inicial en semillas de cobertura de invierno'
            ],
            risks: [
                'Pérdida continua de Materia Orgánica por suelo desnudo durante 5 meses al año',
                'Erosión hídrica y eólica severa detectada en observaciones de precipitación NASA GPM',
                'Proliferación de malezas resistentes (Amaranthus, Conyza) que encarecen los herbicidas',
                'Dependencia crítica de fertilizantes nitrogenados químicos con altos costos en dólares'
            ],
            evidence: 'Imágenes multiespectrales Landsat y MODIS revelan que los lotes con barbecho químico continuo presentan una reducción sostenida del 18% en el vigor de la biomasa.',
            info_gaps: 'Se requiere muestreo de suelo georreferenciado para medir profundidad de la capa arable y compactación por maquinaria pesada.'
        },
        {
            id: 'strategy_regenerative',
            name: '2. Regeneración de Suelo y Biomasa',
            tag: '⭐ RECOMENDADA POR AMAC & NASA',
            tagClass: 'badge-recommended',
            overall_score: 88,
            recommended: true,
            highlightSummary: 'Incorpora leguminosa fijadora de Nitrógeno y cobertura continua. Maximiza salud del suelo y reduce insumos.',
            scores: {
                water_conservation: 85,
                soil_health: 94,
                economic_return: 86,
                pest_management: 88,
                erosion_control: 92,
                nitrogen_fixation: 95
            },
            sequence: [
                { crop: 'Soja', months: 'Oct–Mar', color: '#40916C', desc: 'Rendimiento comercial estival' },
                { crop: 'Vicia Villosa (Cobertura Viva)', months: 'Abr–Sep', color: '#52B788', desc: 'Fijación biológica de 100 kg N/ha' },
                { crop: 'Maíz Tardío sobre Rastrojo', months: 'Oct–Mar', color: '#2C7DA0', desc: 'Aprovecha nitrógeno y humedad' },
                { crop: 'Trigo / Cebada Doble Propósito', months: 'Jun–Nov', color: '#F4A261', desc: 'Cosecha de grano y cobertura' }
            ],
            metrics: {
                waterDemand: '590 mm/año (Eficiente)',
                nitrogenBalance: '+85 kg N/ha (Superávit natural)',
                bareSoilDays: '0 días (Cobertura 100% permanente)',
                erosionRisk: 'Mínimo (Protección viva)'
            },
            benefits: [
                'Fijación biológica masiva de Nitrógeno: aporta entre 80 y 130 kg N/ha de forma natural',
                'Ahorro del 25% al 35% en compra de fertilizantes sintéticos (Urea)',
                'Cero días de suelo descubierto: actúa como colchón vivo que frena el viento y la lluvia torrencial',
                'Ruptura natural del ciclo biológico de plagas e interrupción de malezas resistentes',
                'Aumento comprobado de la tasa de infiltración de agua en zona radicular (SMAP)'
            ],
            risks: [
                'Requiere calibrar con precisión la fecha de secado o rolado de la Vicia para no restar agua si la primavera viene seca',
                'Costo inicial de compra de semilla para servicio (ampliamente compensado por ahorro de urea)'
            ],
            evidence: 'Los sensores SMAP y ECOSTRESS confirman que el mulching vegetal vivo retiene hasta un 35% más de humedad en los primeros 100 cm de suelo durante olas de calor extremo.',
            info_gaps: 'Ajustar la fecha de rolado mecánico según el pronóstico trimestral de precipitaciones NASA POWER.'
        },
        {
            id: 'strategy_water',
            name: '3. Resiliencia Hídrica y Ahorro de Agua',
            tag: '💧 MÁXIMA EFICIENCIA HÍDRICA',
            tagClass: 'badge-water',
            overall_score: 82,
            recommended: false,
            highlightSummary: 'Cultivos rústicos de raíz profunda que toleran sequía y aprovechan agua subsuperficial.',
            scores: {
                water_conservation: 94,
                soil_health: 78,
                economic_return: 76,
                pest_management: 82,
                erosion_control: 88,
                nitrogen_fixation: 60
            },
            sequence: [
                { crop: 'Sorgo Granífero / Forrajero', months: 'Nov–Abr', color: '#1B4965', desc: 'Raíces exploratorias de 2 metros' },
                { crop: 'Centeno de Cobertura', months: 'May–Sep', color: '#89C2D9', desc: 'Bajo consumo y alta biomasa' },
                { crop: 'Girasol Tolerante a Sequía', months: 'Oct–Feb', color: '#F4A261', desc: 'Descompacta capas profundas' }
            ],
            metrics: {
                waterDemand: '480 mm/año (Ahorro Máximo)',
                nitrogenBalance: '+15 kg N/ha (Equilibrado)',
                bareSoilDays: '20 días (Alta cobertura)',
                erosionRisk: 'Bajo (Rastrojo leñoso persistente)'
            },
            benefits: [
                'Tolerancia sobresaliente ante sequías prolongadas y olas de calor (NASA POWER)',
                'Raíces profundas de sorgo y girasol que rompen capas compactadas sin laboreo mecánico',
                'Rastrojo leñoso de lenta descomposición que protege el lote durante períodos secos',
                'Ideal para campos sin riego o con reservas hídricas subterráneas bajas (GRACE)'
            ],
            risks: [
                'Menor fijación biológica de nitrógeno respecto a leguminosas como la vicia',
                'Canales de comercialización más restringidos para sorgo frente a la soja'
            ],
            evidence: 'En años con anomalías negativas de precipitación (-30%), el sorgo mantiene índices NDVI 25% superiores al maíz según registros del satélite MODIS.',
            info_gaps: 'Verificar precios y contratos a término con cooperativas y centros de acopio cercanos.'
        }
    ];
}

// ─── Sincronizar Sliders con state.farmerPriorities ───
function syncPrioritySlidersFromState() {
    if (!state || !state.farmerPriorities) return;
    const sliders = document.querySelectorAll('.priority-slider input[type="range"]');
    sliders.forEach(slider => {
        const key = slider.dataset.priority;
        if (state.farmerPriorities[key] !== undefined) {
            const pct = Math.round(state.farmerPriorities[key] * 100);
            slider.value = pct;
            const valueSpan = slider.nextElementSibling;
            if (valueSpan) valueSpan.textContent = `${pct}%`;
        }
    });
}

// ─── Recalcular Puntajes Ponderados según Prioridades ───
function recalculateStrategyScores(strategies) {
    if (!strategies || !strategies.length) return strategies;

    const totalWeight = Object.values(state.farmerPriorities || {}).reduce((a, b) => a + b, 0);

    const updated = strategies.map(s => {
        if (!s.scores) return s;
        const keys = Object.keys(s.scores);
        const weighted = keys.reduce((acc, key) => {
            const weight = totalWeight > 0
                ? (state.farmerPriorities[key] !== undefined ? state.farmerPriorities[key] : 0.5)
                : 1;
            return acc + (s.scores[key] * weight);
        }, 0);
        const denom = totalWeight > 0 ? totalWeight : (keys.length || 1);
        s.overall_score = Math.min(100, Math.max(0, Math.round(weighted / denom)));
        return s;
    });

    const maxScore = Math.max(...updated.map(s => s.overall_score));
    let optimalAssigned = false;
    updated.forEach(s => {
        if (s.overall_score === maxScore && !optimalAssigned) {
            s.recommended = true;
            optimalAssigned = true;
        } else {
            s.recommended = false;
        }
    });

    return updated;
}

// ─── Cargar y Renderizar Estrategias ───
async function loadRotationStrategies() {
    let strategies = null;
    let usedBackend = false;

    try {
        const payload = {
            lat: state.location.lat,
            lon: state.location.lon,
            soil_type: state.soilType,
            current_crops: state.currentCrops,
            priorities: state.farmerPriorities
        };

        const result = await apiCall('/api/rotation/strategies', 'POST', payload);
        if (result && result.strategies) {
            strategies = result.strategies;
            usedBackend = true;
        }
    } catch (err) {
        console.warn('Usando estrategias locales:', err);
    }

    if (!strategies) {
        strategies = getMockStrategies();
    }

    syncPrioritySlidersFromState();
    if (!usedBackend) {
        strategies = recalculateStrategyScores(strategies);
    }

    state.rotationStrategies = strategies;
    renderHeadToHeadMatrix(strategies);
    if (!isAgricultorView()) {
        createStrategyRadarChart(strategies);
    }
    renderDashboardStrategyShowcase(strategies);
    renderDecisionRecommendation(strategies);
}

function isAgricultorView() {
    return (typeof currentUser !== 'undefined' && currentUser && currentUser.roleType === 'agricultor');
}

// ─── Actualizar Calificaciones en la Matriz Comparativa Frente a Frente (Head-to-Head) ───
function renderHeadToHeadMatrix(strategies) {
    const list = (strategies && strategies.length) ? strategies : getMockStrategies();
    const baseTitles = {
        strategy_actual: '1. Rotación Actual (Línea Base)',
        strategy_regenerative: '2. Regenerativa',
        strategy_water: '3. Resiliencia Hídrica 💧'
    };

    let optimalScore = 88;

    list.forEach(s => {
        const clamped = Math.min(100, Math.max(0, Math.round(s.overall_score)));
        if (s.recommended) optimalScore = clamped;

        // Actualizar encabezado de columna según cuál estrategia sea óptima
        const thEl = document.getElementById(`h2h-col-${s.id}`);
        if (thEl) {
            const baseLabel = baseTitles[s.id] || s.name;
            thEl.textContent = s.recommended ? `${baseLabel} (Recomendada AMAC) ⭐` : baseLabel;
            thEl.classList.remove('h2h-th-base', 'h2h-th-rec', 'h2h-th-water');
            if (s.recommended) {
                thEl.classList.add('h2h-th-rec');
            } else if (s.id === 'strategy_water') {
                thEl.classList.add('h2h-th-water');
            } else {
                thEl.classList.add('h2h-th-base');
            }
        }

        // Actualizar calificación en la fila Puntuación Ponderada AMAC
        const scoreEl = document.getElementById(`h2h-score-${s.id}`);
        if (scoreEl) {
            const newText = `${clamped} / 100${s.recommended ? ' (Óptima)' : ''}`;
            const changed = scoreEl.textContent.trim() !== newText;
            scoreEl.textContent = newText;
            scoreEl.className = `score-pill ${s.recommended ? 'score-pill-rec' : (s.id === 'strategy_water' ? 'score-pill-water' : 'score-pill-low')}`;
            if (changed) {
                scoreEl.classList.add('score-pill-pulse');
                setTimeout(() => scoreEl.classList.remove('score-pill-pulse'), 350);
            }
        }
    });

    // Sincronizar puntaje óptimo en Resumen Ejecutivo del Agricultor
    const execScoreEl = document.getElementById('exec-optimal-score');
    if (execScoreEl) {
        execScoreEl.textContent = `${optimalScore} / 100`;
    }
}

// ─── Recalcular con Deslizadores de Prioridades ───
function updatePriorities() {
    const sliders = document.querySelectorAll('.priority-slider input[type="range"]');
    sliders.forEach(slider => {
        const key = slider.dataset.priority;
        const val = parseInt(slider.value);
        state.farmerPriorities[key] = val / 100;

        const valueSpan = slider.nextElementSibling;
        if (valueSpan) valueSpan.textContent = `${val}%`;
    });

    if (!state.rotationStrategies || !state.rotationStrategies.length) {
        state.rotationStrategies = getMockStrategies();
    }

    const strategies = recalculateStrategyScores(state.rotationStrategies);
    state.rotationStrategies = strategies;

    renderHeadToHeadMatrix(strategies);
    if (!isAgricultorView()) {
        createStrategyRadarChart(strategies);
    }
    renderDashboardStrategyShowcase(strategies);
    renderDecisionRecommendation(strategies);
}

/**
 * Ajusta los deslizadores a perfiles agronómicos típicos
 */
function setPredefinedPriorities(preset) {
    const presets = {
        soil: {
            soil_health: 95,
            nitrogen_fixation: 90,
            erosion_control: 85,
            water_conservation: 65,
            pest_management: 80,
            economic_return: 60
        },
        water: {
            water_conservation: 95,
            erosion_control: 80,
            soil_health: 70,
            economic_return: 70,
            pest_management: 65,
            nitrogen_fixation: 45
        }
    };

    const target = presets[preset];
    if (!target) return;

    Object.entries(target).forEach(([k, val]) => {
        const slider = document.querySelector(`.priority-slider input[data-priority="${k}"]`);
        if (slider) {
            slider.value = val;
            const valueSpan = slider.nextElementSibling;
            if (valueSpan) valueSpan.textContent = `${val}%`;
            state.farmerPriorities[k] = val / 100;
        }
    });

    updatePriorities();
    showToast(`Prioridades ajustadas a perfil: ${preset === 'soil' ? 'Salud del Suelo' : 'Ahorro Hídrico'}`, 'info');
}

// ─── Renderizar Escaparate Protagonista de las 3 Estrategias en el Dashboard ───
function renderDashboardStrategyShowcase(strategies) {
    const showcaseContainer = document.getElementById('dashboard-strategies-showcase');
    if (!showcaseContainer) return;

    if (!strategies || !strategies.length) {
        strategies = getMockStrategies();
    }

    const isAgricultor = (typeof currentUser !== 'undefined' && currentUser && currentUser.roleType === 'agricultor');

    // Para el agricultor, el botón de "Ver Análisis completo" no aparece para no confundirlo (Requisito Mentorías AMAC)
    const actionButtonHtml = isAgricultor ? '' : `
        <button id="btn-showcase-complete" class="btn btn-secondary btn-sm" onclick="navigateTo('rotaciones')">
            Ver Análisis Completo ➔
        </button>
    `;

    // Sincronizar tarjeta de estrategia recomendada en el Dashboard principal
    const recStrat = strategies.find(s => s.recommended) || strategies[1] || strategies[0];
    if (recStrat) {
        const recScoreClamped = Math.min(100, Math.max(0, Math.round(recStrat.overall_score)));
        const dashBar = document.getElementById('dash-score-bar');
        const dashText = document.getElementById('dash-score-text');
        const dashCrops = document.getElementById('dash-rec-crops');
        if (dashBar) {
            dashBar.style.width = recScoreClamped + '%';
            dashBar.setAttribute('data-score', recScoreClamped);
        }
        if (dashText) {
            dashText.textContent = `Puntuación general: ${recScoreClamped}/100`;
        }
        if (dashCrops && recStrat.sequence) {
            dashCrops.textContent = recStrat.sequence.map(step => step.crop.split(' ')[0]).join(' → ');
        }
    }

    const soilLabels = {
        'franco': 'Franco Equilibrado',
        'franco-arcilloso': 'Franco-Arcilloso (Trumao)',
        'franco-arenoso': 'Franco-Arenoso',
        'arenoso': 'Arenoso',
        'arcilloso': 'Arcilloso',
        'limoso': 'Limoso'
    };
    const soilDisplay = soilLabels[state.soilType] || (state.soilType || 'Franco').toUpperCase();

    showcaseContainer.innerHTML = `
        <div class="showcase-header">
            <div>
                <span class="showcase-badge">🎯 ¿QUÉ DECISIÓN TOMAR? · FIELD SHIFT NASA</span>
                <h3 class="showcase-title">Comparativa de las 3 Estrategias de Rotación</h3>
                <p class="showcase-subtitle">Evaluadas con telemetría satelital NASA POWER, SMAP y GPM para tu suelo (${soilDisplay})</p>
            </div>
            ${actionButtonHtml}
        </div>

        <div class="showcase-cards-grid">
            ${strategies.map((s, idx) => {
    const clampedScore = Math.min(100, Math.max(0, Math.round(s.overall_score)));
    const clampedWater = Math.min(100, Math.max(0, Math.round(s.scores.water_conservation)));
    const clampedSoil = Math.min(100, Math.max(0, Math.round(s.scores.soil_health)));

    return `
                <div class="showcase-card ${s.recommended ? 'showcase-card-rec' : ''}" onclick="navigateTo('rotaciones')">
                    <div class="showcase-card-top">
                        <span class="showcase-card-badge ${s.tagClass || ''}">${s.tag || 'Opción ' + (idx + 1)}</span>
                        <div class="showcase-card-score">${clampedScore}<span>/100</span></div>
                    </div>
                    <h4 class="showcase-card-name">${s.name}</h4>
                    <p class="showcase-card-summary">${s.highlightSummary || ''}</p>
                    
                    <div class="showcase-timeline-mini">
                        ${s.sequence.map(step => `<span class="mini-crop-pill" style="background:${step.color}20; color:${step.color}; border:1px solid ${step.color}40;">${step.crop.split(' ')[0]}</span>`).join(' ➔ ')}
                    </div>

                    <div class="showcase-card-footer">
                        <span>💧 Agua: <strong>${clampedWater}/100</strong></span>
                        <span>🌱 Suelo: <strong>${clampedSoil}/100</strong></span>
                        <span class="showcase-link">${isAgricultor ? 'Ver Recomendación →' : 'Detalles →'}</span>
                    </div>
                </div>
                `;
}).join('')}
        </div>
    `;
}

// ─── Bloque Simplificado: "¿Qué decisión tomar? — Recomendación AMAC" ───
function renderDecisionRecommendation(strategies, selectedId = null) {
    const container = document.getElementById('action-plan-timeline');
    if (!container) return;

    const list = (strategies && strategies.length) ? strategies : getMockStrategies();
    const chosen = (selectedId ? list.find(s => s.id === selectedId) : null)
        || list.find(s => s.recommended)
        || list[1]
        || list[0];

    const isAgricultor = (typeof currentUser !== 'undefined' && currentUser && currentUser.roleType === 'agricultor');
    const clampedScore = Math.min(100, Math.max(0, Math.round(chosen.overall_score)));
    const locName = state.location?.name || 'Los Ángeles, Biobío';

    let headline = 'Incorpora cobertura viva de Vicia villosa y rota con Maíz tardío / Trigo';
    let whyText = 'Evitas los 150 días de suelo desnudo en invierno, retienes hasta 35% más humedad radicular y fijas nitrógeno biológico gratis.';
    let savingsChip = '25% – 35% menos Urea';
    let steps = [
        {
            when: '1. Ahora (Post-cosecha)',
            title: 'Sembrar cobertura en otoño',
            desc: isAgricultor
                ? 'No dejes el potrero pelado después de cosechar. Siembra Vicia villosa inoculada con las primeras lluvias.'
                : 'Implantar Vicia villosa inoculada inmediatamente post-cosecha para anular el barbecho químico invernal.',
            nasa: 'SMAP GWETROOT ≥ 45% para siembra óptima'
        },
        {
            when: '2. Invierno (Crecimiento)',
            title: 'Proteger suelo y fijar nitrógeno',
            desc: isAgricultor
                ? 'La cobertura frena la erosión de las lluvias fuertes y junta entre 85 y 130 kg/ha de abono natural.'
                : 'Cobertura viva del 100% reduce escorrentía por eventos GPM y acumula 85–130 kg N/ha simbiótico.',
            nasa: 'MODIS NDVI > 0.55 valida vigor invernal'
        },
        {
            when: '3. Primavera – Verano',
            title: 'Sembrar sobre el colchón protector',
            desc: isAgricultor
                ? 'Pasa el rolo antes de sembrar maíz o trigo. El rastrojo guarda la humedad del verano y ahorra fertilizante.'
                : 'Rolado mecánico en floración y siembra directa sobre rastrojo; ajustar dosis de N sintético (-30%).',
            nasa: 'ECOSTRESS monitorea estrés térmico foliar'
        }
    ];

    if (chosen.id === 'strategy_water') {
        headline = 'Prioriza Sorgo de raíz profunda y Centeno de cobertura para resistir sequía';
        whyText = 'Tus prioridades priorizan el ahorro de agua. Este esquema consume solo 480 mm/año y explora humedad profunda.';
        savingsChip = '38% menos consumo hídrico';
        steps = [
            {
                when: '1. Ahora (Preparación)',
                title: 'Conservar el rastrojo en superficie',
                desc: isAgricultor
                    ? 'No quemes ni des vuelta la tierra. Deja la paja encima para que el sol no evapore la humedad.'
                    : 'Mantener cobertura residual completa para disminuir evaporación directa antes de la siembra.',
                nasa: 'SMAP verifica reserva hídrica subsuperficial'
            },
            {
                when: '2. Otoño – Invierno',
                title: 'Establecer Centeno rústico',
                desc: isAgricultor
                    ? 'Siembra Centeno para cubrir el campo gastando muy poca agua y soltar la tierra apretada.'
                    : 'Centeno de bajo requerimiento hídrico genera biomasa fibrosa y mejora infiltración.',
                nasa: 'NASA POWER PRECTOTCORR sigue recarga invernal'
            },
            {
                when: '3. Primavera – Verano',
                title: 'Sembrar Sorgo o Girasol resistente',
                desc: isAgricultor
                    ? 'Usa variedades de raíz profunda que aguantan los veranos secos sin perder rendimiento.'
                    : 'Sorgo C4 / Girasol exploran hasta 2 m de profundidad frente a déficits hídricos.',
                nasa: 'GRACE-FO y MODIS confirman resiliencia en sequía'
            }
        ];
    } else if (chosen.id === 'strategy_actual') {
        headline = 'Atención: Mantener la rotación tradicional tiene alto riesgo climático y de costos';
        whyText = 'Aunque es el manejo conocido, dejar el suelo desnudo en invierno pierde humedad, acelera la erosión y encarece los fertilizantes.';
        savingsChip = '0% ahorro · Déficit -45 kg N/ha';
        steps = [
            {
                when: '1. Diagnóstico inmediato',
                title: 'Reducir ventanas de suelo desnudo',
                desc: isAgricultor
                    ? 'Si sigues con este plan, intenta al menos dejar el rastrojo picado sin quemar ni rastrear.'
                    : 'Evaluar transición parcial hacia un cultivo puente para mitigar 150 días de barbecho descubierto.',
                nasa: 'Landsat muestra caída de -18% en biomasa'
            },
            {
                when: '2. Control de erosión',
                title: 'Vigilar lluvias intensas y malezas',
                desc: isAgricultor
                    ? 'Revisa drenajes y malezas resistentes antes de aplicar herbicidas costosos.'
                    : 'Alta presión de Amaranthus/Conyza y pérdida de suelo superficial ante lluvias GPM.',
                nasa: 'GPM IMERG alerta riesgo de lavado superficial'
            },
            {
                when: '3. Siguiente campaña',
                title: 'Probar franja piloto regenerativa',
                desc: isAgricultor
                    ? 'Compara un potrero pequeño con Vicia o Centeno junto a tu asesor para ver el ahorro en tu bolsillo.'
                    : 'Implementar parcela demostrativa con Estrategia 2 o 3 para validar ahorro en Urea y humedad.',
                nasa: 'Comparativa multiespectral NDVI en finca'
            }
        ];
    }

    container.innerHTML = `
        <div class="decision-header">
            <div>
                <span class="action-plan-badge">🧭 DECISIÓN CLARA BASADA EN NASA + SUELO LOCAL</span>
                <h3 class="decision-main-title">¿Qué decisión tomar? — Recomendación AMAC</h3>
                <p class="card-hint">
                    ${isAgricultor
                        ? `Recomendación directa para <strong>${locName}</strong> combinando satélites de la NASA con tu terreno:`
                        : `Síntesis ejecutiva para extensión en <strong>${locName}</strong> (Fusión NASA POWER/SMAP + ISRIC SoilGrids + MCDA):`}
                </p>
            </div>
            <div class="decision-score-pill">
                <span class="decision-score-label">Puntaje</span>
                <strong class="decision-score-num">${clampedScore}<span>/100</span></strong>
            </div>
        </div>

        <div class="decision-hero-box">
            <div class="decision-hero-tag">⭐ RECOMENDACIÓN PRINCIPAL: ${chosen.name}</div>
            <h4 class="decision-hero-headline">${headline}</h4>
            <p class="decision-hero-why">${whyText}</p>
            <div class="decision-impact-chips">
                <span class="decision-chip chip-water">💧 Agua: ${chosen.metrics?.waterDemand || 'Eficiente'}</span>
                <span class="decision-chip chip-soil">🌱 Nitrógeno: ${chosen.metrics?.nitrogenBalance || 'Positivo'}</span>
                <span class="decision-chip chip-save">💰 Impacto: ${savingsChip}</span>
            </div>
        </div>

        <div class="decision-steps-grid">
            ${steps.map(st => `
                <div class="decision-step-card">
                    <span class="decision-step-when">${st.when}</span>
                    <h5 class="decision-step-title">${st.title}</h5>
                    <p class="decision-step-desc">${st.desc}</p>
                    ${!isAgricultor ? `<div class="decision-step-nasa">🛰️ <strong>Validación NASA:</strong> ${st.nasa}</div>` : ''}
                </div>
            `).join('')}
        </div>
    `;
}

// ─── Acción al Seleccionar una Estrategia ───
function selectStrategyForActionPlan(stratId) {
    renderDecisionRecommendation(state.rotationStrategies, stratId);
    showToast('Recomendación actualizada según la estrategia seleccionada', 'success');
    const actionPlanSection = document.getElementById('action-plan-timeline');
    if (actionPlanSection) {
        actionPlanSection.scrollIntoView({ behavior: 'smooth' });
    }
}
