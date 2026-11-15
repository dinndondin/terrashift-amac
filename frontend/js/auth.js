/* ═══════════════════════════════════════════════════════════════════
   TERRASHIFT by AMAC  ·  auth.js
   Sistema Integral de Roles (Agricultor vs Asesor Técnico) & B2B2C
   Gestión de Agricultores Asignados, WhatsApp y Clima ENSO
   NASA Space Apps Challenge 2026 · Versión 1 2026
   ═══════════════════════════════════════════════════════════════════ */

const AUTH_STORAGE_KEY = 'terrashift_user_session';
const MANAGED_FARMERS_KEY = 'terrashift_managed_farmers';
const ACTIVE_FARMER_KEY = 'terrashift_active_farmer_id';

// Nómina inicial de agricultores representativos de la Provincia de Biobío
const DEFAULT_MANAGED_FARMERS = [
    {
        id: 'farmer_1',
        name: 'Don Manuel Alarcón',
        phone: '+56 9 8765 4321',
        farmName: 'Predio El Roble',
        comuna: 'Los Ángeles',
        location: { lat: -37.47, lon: -72.35, name: 'Los Ángeles, Provincia de Biobío, Chile' },
        farmSize: 65,
        soilType: 'franco-arcilloso',
        crops: ['trigo', 'avena'],
        priorities: {
            water_conservation: 0.60,
            soil_health: 0.90,
            economic_return: 0.75,
            pest_management: 0.70,
            erosion_control: 0.85,
            nitrogen_fixation: 0.95
        },
        notes: 'Suelo Trumao con pendiente suave hacia el estero Quilque. Prioridad: reducir gasto en urea e incorporar vicia.'
    },
    {
        id: 'farmer_2',
        name: 'Doña Rosa Morales',
        phone: '+56 9 7654 3210',
        farmName: 'Fundo Santa Lucía',
        comuna: 'Mulchén',
        location: { lat: -37.72, lon: -72.24, name: 'Mulchén, Provincia de Biobío, Chile' },
        farmSize: 85,
        soilType: 'franco',
        crops: ['trigo', 'cebada'],
        priorities: {
            water_conservation: 0.70,
            soil_health: 0.80,
            economic_return: 0.85,
            pest_management: 0.65,
            erosion_control: 0.75,
            nitrogen_fixation: 0.70
        },
        notes: 'Predio cerealero tradicional. Preocupación por heladas tardías de primavera y costo de semillas de cobertura.'
    },
    {
        id: 'farmer_3',
        name: 'Don Carlos Henríquez',
        phone: '+56 9 6543 2109',
        farmName: 'Parcela Los Quillayes',
        comuna: 'Cabrero',
        location: { lat: -37.03, lon: -72.40, name: 'Cabrero, Provincia de Biobío, Chile' },
        farmSize: 42,
        soilType: 'arenoso',
        crops: ['maiz', 'avena'],
        priorities: {
            water_conservation: 0.95,
            soil_health: 0.65,
            economic_return: 0.70,
            pest_management: 0.60,
            erosion_control: 0.85,
            nitrogen_fixation: 0.50
        },
        notes: 'Suelos arenosos de baja retención hídrica. Prioridad absoluta: resiliencia hídrica con Sorgo y Centeno.'
    }
];

// Perfiles representativos del Modelo B2B2C
const TERRASHIFT_PROFILES = {
    // 1. Asesor Técnico Agrícola (Copiloto profesional)
    asesor: {
        id: 'user_asesor_biobio',
        name: 'Ing. Rodrigo Valenzuela',
        roleType: 'asesor',
        role: 'Asesor Técnico Agrícola (PRODESAL / INDAP)',
        roleBadge: '🔬 Asesor Agrícola (Copiloto)',
        email: 'r.valenzuela@prodesal-biobio.cl',
        organization: 'PRODESAL Comuna de Los Ángeles (INDAP)',
        territory: 'Provincia de Biobío, Chile',
        avatar: '👨‍🌾',
        assignedPredios: 34,
        valueProp: 'Copiloto profesional: integra clima NASA, cartografía SoilGrids y prepara informes claros para fundamentar cada recomendación.'
    },

    // 2. Agricultor / Productor Familiar (Quien toma la decisión)
    agricultor: {
        id: 'user_agricultor_biobio',
        name: 'Don Manuel Alarcón',
        roleType: 'agricultor',
        role: 'Agricultor Cerealero Familiar',
        roleBadge: '🌾 Agricultor (Toma la Decisión)',
        email: 'manuel.alarcon@campochileno.cl',
        farmName: 'Predio El Roble (Los Ángeles, Biobío)',
        location: { lat: -37.47, lon: -72.35, name: 'Los Ángeles, Provincia de Biobío, Chile' },
        farmSize: 65,
        soilType: 'franco-arcilloso',
        crops: ['trigo', 'avena'],
        avatar: '🚜',
        valueProp: 'Nadie conoce tu tierra mejor que tú. Terrashift te entrega información clara para decidir junto a tu asesor.'
    },

    // 3. Cliente Institucional Pagador (B2B: Municipalidad / INDAP)
    institucion: {
        id: 'user_institucion_biobio',
        name: 'Dirección de Desarrollo Rural',
        roleType: 'institucion',
        role: 'Administrador Institucional (Municipalidad / INDAP)',
        roleBadge: '🏛️ Cliente Institucional (B2B)',
        email: 'fomento.productivo@losangeles.cl',
        organization: 'Municipalidad de Los Ángeles · Plan Regional Biobío',
        territory: 'Provincia de Biobío (11.810 agricultores)',
        avatar: '🏛️',
        valueProp: 'Monitoreo territorial agregado, trazabilidad de impacto ambiental y adaptación climática comunal.'
    }
};

let currentUser = null;
let currentEnsoPhase = 'nino'; // 'nino' | 'nina'

const ROLE_GATE_SESSION_KEY = 'terrashift_role_chosen';

// ─── Inicialización de Sesión ───
function initAuth() {
    try {
        const saved = localStorage.getItem(AUTH_STORAGE_KEY);
        if (saved) {
            currentUser = JSON.parse(saved);
        } else {
            // Por defecto arranca en Modo Asesor Técnico Agrícola hasta elegir en la pantalla inicial
            currentUser = { ...TERRASHIFT_PROFILES.asesor };
            localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(currentUser));
        }
    } catch (e) {
        currentUser = { ...TERRASHIFT_PROFILES.asesor };
    }

    // Asegurar que la nómina de agricultores exista en localStorage
    ensureManagedFarmers();

    applyUserProfile(currentUser);
    renderUserWidget();
    applyRoleView(currentUser.roleType || 'asesor');

    // Mostrar pantalla grande de decisión inicial entre Agricultor y Asesor al abrir la web
    initRoleGate();
}

function initRoleGate() {
    const gate = document.getElementById('role-gate-overlay');
    if (!gate) return;
    try {
        const chosenInSession = sessionStorage.getItem(ROLE_GATE_SESSION_KEY);
        if (!chosenInSession) {
            openRoleGate();
        }
    } catch (e) {
        openRoleGate();
    }
}

function openRoleGate() {
    const gate = document.getElementById('role-gate-overlay');
    if (!gate) return;
    gate.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeRoleGate() {
    const gate = document.getElementById('role-gate-overlay');
    if (!gate) return;
    gate.classList.remove('active');
    document.body.style.overflow = '';
}

function selectInitialRole(roleKey) {
    try {
        sessionStorage.setItem(ROLE_GATE_SESSION_KEY, roleKey);
    } catch (e) {
        // Ignorar si sessionStorage no está disponible
    }
    closeRoleGate();
    switchUserRole(roleKey);
    if (typeof navigateTo === 'function') {
        navigateTo('dashboard');
    }
}

// ─── Gestión de Nómina de Agricultores (Exclusivo Asesor) ───
function ensureManagedFarmers() {
    try {
        const stored = localStorage.getItem(MANAGED_FARMERS_KEY);
        if (!stored) {
            localStorage.setItem(MANAGED_FARMERS_KEY, JSON.stringify(DEFAULT_MANAGED_FARMERS));
        }
        const activeId = localStorage.getItem(ACTIVE_FARMER_KEY);
        if (!activeId) {
            localStorage.setItem(ACTIVE_FARMER_KEY, 'farmer_1');
        }
    } catch (e) {
        console.warn('Error accediendo a localStorage de agricultores:', e);
    }
}

function getManagedFarmers() {
    try {
        const stored = localStorage.getItem(MANAGED_FARMERS_KEY);
        return stored ? JSON.parse(stored) : [...DEFAULT_MANAGED_FARMERS];
    } catch (e) {
        return [...DEFAULT_MANAGED_FARMERS];
    }
}

function saveManagedFarmers(farmers) {
    try {
        localStorage.setItem(MANAGED_FARMERS_KEY, JSON.stringify(farmers));
    } catch (e) {
        console.error('Error guardando agricultores:', e);
    }
}

function getActiveFarmer() {
    const farmers = getManagedFarmers();
    const activeId = localStorage.getItem(ACTIVE_FARMER_KEY) || 'farmer_1';
    return farmers.find(f => f.id === activeId) || farmers[0];
}

function setActiveFarmer(farmerId, notify = true) {
    localStorage.setItem(ACTIVE_FARMER_KEY, farmerId);
    const farmer = getActiveFarmer();
    if (!farmer) return;

    // Sincronizar estado global con el agricultor seleccionado
    state.location = { ...farmer.location };
    state.soilType = farmer.soilType;
    state.farmSize = farmer.farmSize;
    state.currentCrops = [...farmer.crops];
    if (farmer.priorities) {
        state.farmerPriorities = { ...farmer.priorities };
    }

    // Actualizar campos de configuración de la finca
    const soilSelect = document.getElementById('soil-type');
    if (soilSelect) soilSelect.value = farmer.soilType;
    const sizeInput = document.getElementById('farm-size');
    if (sizeInput) sizeInput.value = farmer.farmSize;
    if (typeof renderCrops === 'function') renderCrops();

    // Actualizar textos de ubicación y suelo
    const dashLoc = document.getElementById('dash-location');
    if (dashLoc) dashLoc.textContent = farmer.location.name;
    const dashSoil = document.getElementById('dash-soil');
    if (dashSoil) dashSoil.textContent = `Tipo de suelo: ${formatSoilLabel(farmer.soilType)}`;
    const selLoc = document.getElementById('selected-location');
    if (selLoc) selLoc.textContent = farmer.location.name;
    const selLat = document.getElementById('sel-lat');
    if (selLat) selLat.textContent = farmer.location.lat.toFixed(4);
    const selLon = document.getElementById('sel-lon');
    if (selLon) selLon.textContent = farmer.location.lon.toFixed(4);

    // Actualizar mapa satelital
    if (typeof updateMapMarker === 'function') {
        updateMapMarker(farmer.location.lat, farmer.location.lon);
    }
    if (typeof drawParcelCircle === 'function') {
        drawParcelCircle(farmer.location.lat, farmer.location.lon, farmer.farmSize);
    }
    if (window.map) {
        window.map.setView([farmer.location.lat, farmer.location.lon], 12);
    }

    // Renderizar componentes dependientes
    renderAdvisorFarmersList();
    renderAdvisorActiveFarmerBanner();
    syncAdvisorCalibDropdown();

    // Recalcular rotaciones para este agricultor
    if (typeof loadRotationStrategies === 'function') {
        loadRotationStrategies();
    }

    if (notify) {
        showToast(`Lote cargado: ${farmer.name} — ${farmer.farmName} (${farmer.comuna})`, 'success');
    }
}

// ─── Renderizado de la Lista de Agricultores del Asesor ───
function renderAdvisorFarmersList() {
    const container = document.getElementById('advisor-farmers-list');
    if (!container) return;

    const farmers = getManagedFarmers();
    const activeFarmer = getActiveFarmer();

    container.innerHTML = farmers.map(f => {
        const isActive = activeFarmer && activeFarmer.id === f.id;
        const phoneClean = (f.phone || '').replace(/[^0-9]/g, '');
        const waMsg = encodeURIComponent(
            `Hola ${f.name}, le escribe su asesor técnico Ing. Rodrigo Valenzuela (PRODESAL / INDAP Biobío). Le comparto el reporte de AMAC Terrashift para su predio '${f.farmName}': Recomendamos adoptar la rotación regenerativa con Vicia villosa para fijar nitrógeno, ahorrar 30% en fertilizante químico y proteger la humedad del suelo. ¡Quedo atento a sus dudas para coordinar la visita a terreno!`
        );

        return `
            <div class="advisor-farmer-card-item ${isActive ? 'active-farmer' : ''}" onclick="setActiveFarmer('${f.id}')">
                <div class="farmer-card-top">
                    <div class="farmer-avatar-circle">🚜</div>
                    <div class="farmer-meta-title">
                        <strong class="farmer-name-text">${f.name}</strong>
                        <span class="farmer-sub-text">📍 ${f.farmName} · ${f.comuna}</span>
                    </div>
                    ${isActive ? '<span class="farmer-active-pill">Predio en Mapa</span>' : ''}
                </div>
                
                <div class="farmer-card-details">
                    <span class="farmer-spec-chip">📐 ${f.farmSize} ha</span>
                    <span class="farmer-spec-chip">🌱 ${f.soilType}</span>
                    <span class="farmer-spec-chip">🌾 ${f.crops.join(', ')}</span>
                </div>

                <div class="farmer-card-actions" onclick="event.stopPropagation()">
                    <a href="https://wa.me/${phoneClean}?text=${waMsg}" target="_blank" class="btn-wa-action" title="Abrir WhatsApp directo con ${f.name}">
                        <span class="wa-icon">💬</span> WhatsApp: ${f.phone}
                    </a>
                    <button class="btn btn-secondary btn-sm" onclick="setActiveFarmer('${f.id}'); navigateTo('finca');" style="padding: 4px 10px; font-size: 0.8rem;">
                        🗺️ Ver Lote
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

function renderAdvisorActiveFarmerBanner() {
    const banner = document.getElementById('advisor-active-farmer-banner');
    if (!banner) return;

    const farmer = getActiveFarmer();
    if (!farmer) {
        banner.innerHTML = '';
        return;
    }

    const phoneClean = (farmer.phone || '').replace(/[^0-9]/g, '');
    const waMsg = encodeURIComponent(
        `Hola ${farmer.name}, le escribe su asesor técnico Ing. Rodrigo Valenzuela. Le adjunto el resumen técnico del predio '${farmer.farmName}': Puntuación de adaptación climática: 88/100 con rotación Vicia-Maíz-Trigo. Reducción estimada de urea: 30%. Saludos cordiales.`
    );

    banner.innerHTML = `
        <div class="active-farmer-banner-content">
            <div class="active-farmer-info-left">
                <span class="active-badge">⭐ AGRICULTOR ACTIVO EN ANÁLISIS:</span>
                <strong class="active-name">${farmer.name}</strong>
                <span class="active-farm-sub">🌾 ${farmer.farmName} (${farmer.location.name}) · ${farmer.farmSize} ha</span>
            </div>
            <div class="active-farmer-actions-right">
                <a href="https://wa.me/${phoneClean}?text=${waMsg}" target="_blank" class="btn-whatsapp-large" title="Enviar informe breve por WhatsApp">
                    <span class="wa-icon">🟢</span> Enviar Resumen Técnico por WhatsApp
                </a>
                <button class="btn btn-secondary btn-sm" onclick="navigateTo('reportes')" title="Generar reporte completo">
                    📄 Ver Informe Oficial
                </button>
            </div>
        </div>
    `;
}

// ─── Modal para Agregar Nuevo Agricultor ───
function toggleAddFarmerModal() {
    const modal = document.getElementById('add-farmer-modal');
    if (!modal) return;
    const isHidden = modal.style.display === 'none' || !modal.style.display;
    modal.style.display = isHidden ? 'flex' : 'none';
}

function handleAddNewFarmer(e) {
    if (e) e.preventDefault();

    const name = document.getElementById('new-farmer-name')?.value.trim();
    const phone = document.getElementById('new-farmer-phone')?.value.trim();
    const farm = document.getElementById('new-farmer-farm')?.value.trim();
    const comunaKey = document.getElementById('new-farmer-comuna')?.value || 'losangeles';
    const size = parseInt(document.getElementById('new-farmer-size')?.value) || 50;
    const soil = document.getElementById('new-farmer-soil')?.value || 'franco-arcilloso';
    const mainCrop = document.getElementById('new-farmer-crop')?.value || 'trigo';

    if (!name || !phone || !farm) {
        showToast('Por favor completa todos los campos requeridos.', 'warning');
        return;
    }

    const comunaCoords = {
        losangeles: { lat: -37.47, lon: -72.35, name: 'Los Ángeles, Provincia de Biobío, Chile', label: 'Los Ángeles' },
        mulchen: { lat: -37.72, lon: -72.24, name: 'Mulchén, Provincia de Biobío, Chile', label: 'Mulchén' },
        cabrero: { lat: -37.03, lon: -72.40, name: 'Cabrero, Provincia de Biobío, Chile', label: 'Cabrero' },
        santabarbara: { lat: -37.67, lon: -72.02, name: 'Santa Bárbara, Provincia de Biobío, Chile', label: 'Santa Bárbara' }
    };

    const targetLoc = comunaCoords[comunaKey] || comunaCoords.losangeles;

    const newFarmer = {
        id: 'farmer_' + Date.now(),
        name: name,
        phone: phone,
        farmName: farm,
        comuna: targetLoc.label,
        location: { lat: targetLoc.lat, lon: targetLoc.lon, name: targetLoc.name },
        farmSize: size,
        soilType: soil,
        crops: [mainCrop, 'avena'],
        priorities: {
            water_conservation: 0.65,
            soil_health: 0.85,
            economic_return: 0.75,
            pest_management: 0.70,
            erosion_control: 0.80,
            nitrogen_fixation: 0.90
        },
        notes: `Agricultor incorporado por asesor técnico. Comuna: ${targetLoc.label}.`
    };

    const farmers = getManagedFarmers();
    farmers.push(newFarmer);
    saveManagedFarmers(farmers);

    toggleAddFarmerModal();
    setActiveFarmer(newFarmer.id);
    showToast(`✅ Agricultor "${name}" agregado exitosamente a tu nómina de Biobío.`, 'success');
}

// ─── Sincronización del Selector de Agricultores en Calibración de Prioridades ───
function syncAdvisorCalibDropdown() {
    const select = document.getElementById('advisor-calib-select');
    if (!select) return;

    const farmers = getManagedFarmers();
    const activeFarmer = getActiveFarmer();

    select.innerHTML = farmers.map(f => {
        const isSel = activeFarmer && activeFarmer.id === f.id ? 'selected' : '';
        return `<option value="${f.id}" ${isSel}>${f.name} — ${f.farmName} (${f.comuna})</option>`;
    }).join('');

    const badge = document.getElementById('calib-farmer-badge');
    if (badge && activeFarmer) {
        badge.textContent = `📍 ${activeFarmer.comuna}`;
    }
}

function onAdvisorCalibFarmerChange(farmerId) {
    setActiveFarmer(farmerId, false);
    // Aplicar deslizadores según las prioridades de ese agricultor
    const farmer = getActiveFarmer();
    if (farmer && farmer.priorities) {
        Object.entries(farmer.priorities).forEach(([k, val]) => {
            const slider = document.querySelector(`.priority-slider input[data-priority="${k}"]`);
            if (slider) {
                const pct = Math.round(val * 100);
                slider.value = pct;
                const valueSpan = slider.nextElementSibling;
                if (valueSpan) valueSpan.textContent = `${pct}%`;
            }
        });
        if (typeof updatePriorities === 'function') {
            updatePriorities();
        }
        showToast(`Prioridades y lote calibrados para ${farmer.name}`, 'info');
    }
}

// ─── Módulo Interactivo ENSO: El Niño vs La Niña ───
function switchEnsoTab(phase) {
    currentEnsoPhase = phase;
    const tabNino = document.getElementById('tab-enso-nino');
    const tabNina = document.getElementById('tab-enso-nina');

    if (tabNino && tabNina) {
        tabNino.classList.toggle('active', phase === 'nino');
        tabNina.classList.toggle('active', phase === 'nina');
    }

    renderEnsoContent(phase, currentUser ? currentUser.roleType : 'asesor');
}

function renderEnsoContent(phase, roleType) {
    const container = document.getElementById('enso-content-body');
    const tagline = document.getElementById('enso-audience-tagline');
    if (!container) return;

    const isAgricultor = roleType === 'agricultor';

    if (tagline) {
        tagline.textContent = isAgricultor
            ? '🚜 Cómo afecta a tu terreno y recomendaciones directas para cuidar tu siembra'
            : '🔬 Diagnóstico Agrometeorológico para tus agricultores asesorados (NASA POWER & MERRA-2)';
    }

    if (phase === 'nino') {
        // El Niño (Fase Cálida / Aumento de precipitaciones en Biobío)
        if (isAgricultor) {
            container.innerHTML = `
                <div class="enso-view-agricultor">
                    <div class="enso-status-pill enso-status-nino">
                        🌊 <strong>El Niño en tu Zona (Biobío):</strong> Mayor cantidad de lluvias en invierno y primavera
                    </div>
                    <div class="enso-grid-farmer">
                        <div class="enso-f-card">
                            <span class="enso-f-icon">🌧️</span>
                            <h4>¿Qué pasará en tu terreno?</h4>
                            <p>Habrá más agua disponible, pero con <strong>riesgo de encharcamiento</strong> en partes bajas del lote y mayor aparición de hongos (roya) en trigo. Las lluvias intensas pueden lavar la tierra fértil si el suelo queda pelado.</p>
                        </div>
                        <div class="enso-f-card">
                            <span class="enso-f-icon">🚜</span>
                            <h4>¿Qué debes hacer en tu campo?</h4>
                            <ul>
                                <li>● <strong>Siembra el abono verde (Vicia):</strong> Las raíces retendrán la tierra fértil para que la lluvia no se la lleve.</li>
                                <li>● <strong>Limpia y repasa zanjas:</strong> Evita que el agua se empoce y pudra las raíces del cultivo.</li>
                                <li>● <strong>Revisa con tu asesor:</strong> Aplica fungicida preventivo a tiempo si el ambiente se mantiene tibio y húmedo.</li>
                            </ul>
                        </div>
                        <div class="enso-f-card">
                            <span class="enso-f-icon">💡</span>
                            <h4>Recomendación Clave:</h4>
                            <p style="color: #2D6A4F; font-weight: 700;">"Aprovecha el agua de El Niño con cultivos de cobertura; no dejes el suelo descubierto en invierno para evitar que la lluvia arrastre tus nutrientes."</p>
                        </div>
                    </div>
                </div>
            `;
        } else {
            // Asesor Técnico
            container.innerHTML = `
                <div class="enso-view-asesor">
                    <div class="enso-tech-banner">
                        <div class="enso-tech-meta">
                            <strong>Anomalía TSM Región El Niño 3.4 (+1.4°C) · Proyección Satelital NASA POWER / GEOS:</strong>
                            <span>Probabilidad de superávit pluviométrico (+25% a +40%) en latitud -37.5°S (Provincia de Biobío).</span>
                        </div>
                    </div>
                    <div class="enso-grid-advisor">
                        <div class="enso-a-card">
                            <div class="enso-a-title">⚠️ Diagnóstico Edafológico y Fitosanitario</div>
                            <p>Saturación del horizonte arable en suelos Trumao volcánicos. Rápida lixiviación de nitratos (NO3-) hacia napas profundas. Presión extrema de patógenos fúngicos (<em>Puccinia striiformis</em> y <em>Septoria tritici</em>) en cereales de invierno.</p>
                        </div>
                        <div class="enso-a-card">
                            <div class="enso-a-title">🎯 Acciones de Extensión con tus Agricultores</div>
                            <ul>
                                <li>1. <strong>Calibrar rolado de Vicia villosa:</strong> Ejecutar en floración para incorporar biomasa y evitar asfixia radicular en siembras posteriores.</li>
                                <li>2. <strong>Fraccionar la fertilización:</strong> No aplicar toda la urea de golpe; dividir las dosis para amortiguar pérdidas por lavado hídrico.</li>
                                <li>3. <strong>Monitorear SMAP (GWETROOT > 0.75):</strong> Alertar al agricultor de suspender tránsito de maquinaria pesada para prevenir compactación.</li>
                            </ul>
                        </div>
                    </div>
                </div>
            `;
        }
    } else {
        // La Niña (Fase Fría / Sequía y Heladas en Biobío)
        if (isAgricultor) {
            container.innerHTML = `
                <div class="enso-view-agricultor">
                    <div class="enso-status-pill enso-status-nina">
                        ❄️ <strong>La Niña en tu Zona (Biobío):</strong> Menos lluvias, períodos secos y riesgo de heladas tardías
                    </div>
                    <div class="enso-grid-farmer">
                        <div class="enso-f-card">
                            <span class="enso-f-icon">☀️</span>
                            <h4>¿Qué pasará en tu terreno?</h4>
                            <p>El sol y el viento secarán rápido el suelo. Menos lluvias en primavera y <strong>mayor peligro de heladas en las madrugadas</strong> de septiembre y octubre que pueden quemar las flores del trigo o la emergencia del maíz.</p>
                        </div>
                        <div class="enso-f-card">
                            <span class="enso-f-icon">🌾</span>
                            <h4>¿Qué debes hacer en tu campo?</h4>
                            <ul>
                                <li>● <strong>Cuida cada gota con colchón de paja:</strong> Deja el rastrojo sobre la tierra; actúa como un techo protector contra el sol.</li>
                                <li>● <strong>Elige variedades aguantadoras:</strong> Consulta con tu asesor por la Estrategia 3 (Sorgo o Centeno) que tienen raíces profundas.</li>
                                <li>● <strong>Riega antes de la helada:</strong> El suelo húmedo retiene más calor y protege a la planta del frío nocturno.</li>
                            </ul>
                        </div>
                        <div class="enso-f-card">
                            <span class="enso-f-icon">💧</span>
                            <h4>Recomendación Clave:</h4>
                            <p style="color: #1B4965; font-weight: 700;">"En años de La Niña, el rastrojo sobre el suelo es tu mejor seguro contra la sequía. No quemes ni entierres los residuos de cosecha."</p>
                        </div>
                    </div>
                </div>
            `;
        } else {
            // Asesor Técnico
            container.innerHTML = `
                <div class="enso-view-asesor">
                    <div class="enso-tech-banner enso-banner-nina">
                        <div class="enso-tech-meta">
                            <strong>Anomalía Negativa TSM (-1.2°C) · Bloqueo Anticiclónico del Pacífico Sur:</strong>
                            <span>Déficit histórico proyectado de -30% a -50% en precipitaciones y aumento del 40% en heladas radiativas (T2M_MIN < 0°C).</span>
                        </div>
                    </div>
                    <div class="enso-grid-advisor">
                        <div class="enso-a-card">
                            <div class="enso-a-title">⚠️ Diagnóstico de Estrés Térmico e Hídrico</div>
                            <p>Estrés hídrico anticipado en encañado y espigazón de trigo. Sensores ECOSTRESS evidencian elevación anormal de la temperatura foliar por cierre estomático prematuro. Agotamiento de la recarga en perfiles profundos (GRACE-FO).</p>
                        </div>
                        <div class="enso-a-card">
                            <div class="enso-a-title">🎯 Acciones de Extensión con tus Agricultores</div>
                            <ul>
                                <li>1. <strong>Recomendar la Estrategia 3 (Resiliencia Hídrica):</strong> Priorizar especies C4 de alta eficiencia en uso del agua (Sorgo granífero / Centeno de ciclo corto).</li>
                                <li>2. <strong>Reducir densidad de siembra (-15%):</strong> Ajustar índice de área foliar (LAI) a la menor disponibilidad de agua detectada en SMAP.</li>
                                <li>3. <strong>Retención absoluta de cobertura (Mulching):</strong> Prohibir barbecho químico descubierto; el colchón reduce hasta 40% la evaporación directa.</li>
                            </ul>
                        </div>
                    </div>
                </div>
            `;
        }
    }
}

// ─── Aplicación Exhaustiva de Vistas por Rol (Mentorías AMAC) ───
function applyRoleView(roleKey) {
    const isAgri = roleKey === 'agricultor';
    const isAsesor = roleKey === 'asesor';

    // Clases en body para control global de estilos y tamaño de tipografía
    document.body.classList.toggle('role-agricultor-view', isAgri);
    document.body.classList.toggle('role-asesor-view', isAsesor);

    // 1. Selector Rápido de la Barra Lateral
    const btnAgri = document.getElementById('btn-role-agri');
    const btnAsesor = document.getElementById('btn-role-asesor');
    if (btnAgri && btnAsesor) {
        btnAgri.classList.toggle('active', isAgri);
        btnAsesor.classList.toggle('active', isAsesor);
    }

    // 2. Títulos de Navegación en Barra Lateral
    const navFinca = document.getElementById('nav-label-finca');
    if (navFinca) {
        navFinca.textContent = isAgri ? 'Mi predio' : 'Predio de mi agricultor';
    }

    const navRotaciones = document.getElementById('nav-label-rotaciones');
    if (navRotaciones) {
        navRotaciones.textContent = isAgri ? 'Resumen' : 'Estrategias';
    }

    const navReportes = document.getElementById('nav-label-reportes');
    if (navReportes) {
        navReportes.textContent = isAgri ? 'Guía del Agricultor' : 'Informe Oficial';
    }

    // Portal Regional: Borrado / Oculto para el agricultor (Requisito Explícito)
    const navRegional = document.getElementById('nav-item-regional');
    if (navRegional) {
        navRegional.style.display = isAgri ? 'none' : 'flex';
    }

    // Si el usuario agricultor estaba en la sección regional, redirigir a dashboard
    if (isAgri && state.currentSection === 'regional') {
        navigateTo('dashboard');
    }

    // 3. Encabezados de Secciones
    const fincaTitle = document.getElementById('finca-section-title');
    const fincaDesc = document.getElementById('finca-section-desc');
    if (fincaTitle) fincaTitle.textContent = isAgri ? '🌾 Mi terreno' : '🌾 Predio de mi agricultor';
    if (fincaDesc) fincaDesc.textContent = isAgri
        ? 'Visualiza tu lote satelital y confirma los cultivos y suelo de tu predio'
        : 'Administra los predios de tus agricultores asignados, revisa su mapa satelital y envíales reportes por WhatsApp';

    const rotTitle = document.getElementById('rotaciones-section-title');
    const rotDesc = document.getElementById('rotaciones-section-desc');
    if (rotTitle) rotTitle.textContent = isAgri ? '📋 Resumen de Estrategias para tu Terreno' : '🔄 Plan de Acción: 3 Estrategias de Rotación';
    if (rotDesc) rotDesc.textContent = isAgri
        ? 'Plan claro y práctico para mejorar tus cosechas y ahorrar dinero en insumos'
        : 'Comparativa agronómica y financiera para adaptar la explotación al cambio climático con telemetría NASA';

    const repTitle = document.getElementById('reportes-section-title');
    const repDesc = document.getElementById('reportes-section-desc');
    if (repTitle) repTitle.textContent = isAgri ? '📋 Guía Práctica para el Agricultor' : '🔬 Dossier Técnico Oficial de Extensión Agrícola';
    if (repDesc) repDesc.textContent = isAgri
        ? 'Resumen simple con acciones directas para tu campo y ahorro económico estimado'
        : 'Reporte multidimensional con respaldo científico de la NASA para fundamentar cada recomendación';

    // 4. Dashboard: Gráficos (Ocultos para agricultor, Visibles en grilla 2 col para asesor)
    const dashCharts = document.getElementById('dashboard-charts-row');
    if (dashCharts) {
        dashCharts.style.display = isAgri ? 'none' : 'grid';
    }

    // Botón "Ver Análisis Completo" en el Plan de Acción del Dashboard (Oculto para agricultor, Visible para asesor)
    const btnShowcase = document.getElementById('btn-showcase-complete');
    if (btnShowcase) {
        btnShowcase.style.display = isAgri ? 'none' : 'inline-block';
    }

    // Re-renderizar el showcase de estrategias en Dashboard (asegurando que siempre esté visible y con datos)
    if (typeof renderDashboardStrategyShowcase === 'function') {
        renderDashboardStrategyShowcase(state.rotationStrategies);
    }

    // 5. Mi Predio: Panel de Gestión de Agricultores del Asesor
    const advisorPanel = document.getElementById('advisor-farmer-panel');
    if (advisorPanel) {
        advisorPanel.style.display = isAsesor ? 'block' : 'none';
        if (isAsesor) {
            renderAdvisorFarmersList();
            renderAdvisorActiveFarmerBanner();
        }
    }

    // 6. Clima NASA: Gráficos (Ocultos para agricultor, Visibles para asesor)
    const climateCharts = document.getElementById('climate-charts-wrapper');
    if (climateCharts) {
        climateCharts.style.display = isAgri ? 'none' : 'block';
    }

    // Módulo ENSO (El Niño & La Niña)
    renderEnsoContent(currentEnsoPhase, roleKey);

    // 7. Sección 3 Estrategias: Resumen Ejecutivo vs Desplegable Asesor
    const execSummary = document.getElementById('farmer-executive-summary');
    if (execSummary) {
        execSummary.style.display = isAgri ? 'block' : 'none';
        const execFarmName = document.getElementById('exec-farm-name');
        const activeF = getActiveFarmer();
        if (execFarmName && activeF) {
            execFarmName.textContent = `${activeF.farmName} (${activeF.comuna})`;
        }
    }

    const advisorHero = document.getElementById('advisor-hero-banner');
    if (advisorHero) {
        advisorHero.style.display = isAsesor ? 'block' : 'none';
    }

    const advisorCalib = document.getElementById('advisor-farmer-calib-wrap');
    if (advisorCalib) {
        advisorCalib.style.display = isAsesor ? 'block' : 'none';
        if (isAsesor) syncAdvisorCalibDropdown();
    }

    // Gráfico Radar Multidimensional (Eliminado de la visión del agricultor; visible para asesor)
    const radarCard = document.getElementById('strategy-radar-card');
    if (radarCard) {
        radarCard.style.display = isAgri ? 'none' : 'block';
    }

    // 8. Re-renderizar matriz comparativa, radar (solo asesor) y recomendación simplificada
    if (typeof renderHeadToHeadMatrix === 'function' && state.rotationStrategies) {
        renderHeadToHeadMatrix(state.rotationStrategies);
    }
    if (!isAgri && typeof createStrategyRadarChart === 'function' && state.rotationStrategies) {
        createStrategyRadarChart(state.rotationStrategies);
    }
    if (typeof renderDecisionRecommendation === 'function') {
        renderDecisionRecommendation(state.rotationStrategies);
    }

    // 9. Si el reporte oficial está abierto, re-generarlo para el rol activo
    const reportCard = document.getElementById('report-preview-card');
    if (reportCard && reportCard.style.display !== 'none' && typeof generateReport === 'function') {
        generateReport();
    }
}

function formatSoilLabel(soilKey) {
    const labels = {
        'franco': 'Franco Equilibrado',
        'franco-arcilloso': 'Franco-Arcilloso (Trumao)',
        'franco-arenoso': 'Franco-Arenoso',
        'arenoso': 'Arenoso',
        'arcilloso': 'Arcilloso',
        'limoso': 'Limoso'
    };
    return labels[soilKey] || soilKey || 'Franco Trumao';
}

// ─── Aplicación de Datos de Perfil ───
function applyUserProfile(user) {
    if (!user) return;

    if (user.location) {
        state.location = { ...user.location };
    } else {
        state.location = { lat: -37.47, lon: -72.35, name: 'Los Ángeles, Provincia de Biobío, Chile' };
    }

    if (user.soilType) {
        state.soilType = user.soilType;
        const soilEl = document.getElementById('soil-type');
        if (soilEl) soilEl.value = user.soilType;
    }

    if (user.crops && Array.isArray(user.crops)) {
        state.currentCrops = [...user.crops];
        if (typeof renderCrops === 'function') renderCrops();
    }

    if (user.farmSize) {
        state.farmSize = user.farmSize;
        const sizeEl = document.getElementById('farm-size');
        if (sizeEl) sizeEl.value = user.farmSize;
    }

    // Actualizar marcadores de texto en dashboard
    const dashLoc = document.getElementById('dash-location');
    if (dashLoc) dashLoc.textContent = state.location.name;

    const dashSoil = document.getElementById('dash-soil');
    if (dashSoil) dashSoil.textContent = `Tipo de suelo: ${formatSoilLabel(state.soilType)}`;

    const selLoc = document.getElementById('selected-location');
    if (selLoc) selLoc.textContent = state.location.name;

    // Actualizar mapa si está activo
    if (typeof updateMapMarker === 'function' && state.location.lat) {
        updateMapMarker(state.location.lat, state.location.lon);
        if (window.map) {
            window.map.setView([state.location.lat, state.location.lon], 11);
        }
    }
}

// ─── Widget de Usuario en la Barra Lateral ───
function renderUserWidget() {
    const container = document.getElementById('user-profile-widget');
    if (!container) return;

    if (!currentUser) {
        container.innerHTML = `
            <div class="user-widget-anonymous" onclick="openLoginModal()">
                <div class="user-avatar-placeholder">👤</div>
                <div class="user-info-text">
                    <span class="user-name-label">Seleccionar Perfil</span>
                    <span class="user-role-label">Asesor o Agricultor</span>
                </div>
                <span class="user-login-arrow">➔</span>
            </div>
        `;
        return;
    }

    const orgOrFarm = currentUser.farmName || currentUser.organization || 'Biobío, Chile';

    container.innerHTML = `
        <div class="user-widget-card" onclick="openLoginModal()">
            <div class="user-avatar-circle">${currentUser.avatar || '👨‍🌾'}</div>
            <div class="user-info-text">
                <div class="user-name-line">
                    <span class="user-name-label">${currentUser.name}</span>
                </div>
                <span class="user-farm-label">📍 ${orgOrFarm}</span>
                <span class="user-role-badge ${currentUser.roleType === 'asesor' ? 'badge-role-asesor' : currentUser.roleType === 'agricultor' ? 'badge-role-agri' : 'badge-role-inst'}">
                    ${currentUser.roleBadge}
                </span>
            </div>
            <button class="user-menu-btn" title="Cambiar rol o predio" onclick="event.stopPropagation(); openLoginModal();">🔄</button>
        </div>
    `;
}

function openLoginModal() {
    const modal = document.getElementById('auth-modal');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeLoginModal() {
    const modal = document.getElementById('auth-modal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// ─── Cambio Rápido de Rol (1 Clic) ───
function switchUserRole(roleKey) {
    const profile = TERRASHIFT_PROFILES[roleKey];
    if (!profile) return;

    try {
        sessionStorage.setItem(ROLE_GATE_SESSION_KEY, roleKey);
    } catch (e) {}

    currentUser = { ...profile };
    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(currentUser));

    applyUserProfile(currentUser);
    renderUserWidget();
    applyRoleView(roleKey);
    closeLoginModal();

    showToast(`Modo cambiado a: ${currentUser.roleBadge}`, 'success');

    // Refrescar mapa o gráficos si la sección activa los contiene
    if (state.currentSection === 'finca' && typeof forceMapRefresh === 'function') {
        forceMapRefresh();
    }
    if (state.currentSection === 'rotaciones' && typeof loadRotationStrategies === 'function') {
        loadRotationStrategies();
    }
    if (state.currentSection === 'clima' && typeof initClimateCharts === 'function') {
        initClimateCharts();
    }
}

function handleCustomLogin(e) {
    if (e) e.preventDefault();

    const name = document.getElementById('login-name')?.value.trim();
    const farm = document.getElementById('login-farm')?.value.trim();
    const roleType = document.getElementById('login-role')?.value || 'agricultor';
    const locationName = document.getElementById('login-location')?.value.trim() || 'Los Ángeles, Biobío, Chile';

    if (!name) {
        showToast('Por favor ingrese su nombre.', 'warning');
        return;
    }

    const isAsesor = roleType === 'asesor';
    currentUser = {
        id: 'user_' + Date.now(),
        name: name,
        roleType: roleType,
        role: isAsesor ? 'Asesor Técnico Agropecuario' : 'Productor Agrícola',
        roleBadge: isAsesor ? '🔬 Asesor Agrícola (Copiloto)' : '🌾 Agricultor (Toma la Decisión)',
        email: `${name.toLowerCase().replace(/\s+/g, '')}@biobio-agro.cl`,
        farmName: farm || 'Predio Agrícola',
        organization: isAsesor ? (farm || 'PRODESAL Biobío') : undefined,
        location: { lat: -37.47, lon: -72.35, name: locationName },
        farmSize: parseInt(document.getElementById('farm-size')?.value) || 65,
        soilType: state.soilType || 'franco-arcilloso',
        crops: state.currentCrops || ['trigo', 'avena'],
        avatar: isAsesor ? '👨‍🌾' : '🚜'
    };

    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(currentUser));
    applyUserProfile(currentUser);
    renderUserWidget();
    applyRoleView(roleType);
    closeLoginModal();

    showToast(`Sesión iniciada con éxito como ${currentUser.name}.`, 'success');
}

document.addEventListener('DOMContentLoaded', () => {
    initAuth();
});
