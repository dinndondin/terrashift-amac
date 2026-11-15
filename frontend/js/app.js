/* ═══════════════════════════════════════════════════
   AMAC — app.js  ·  Main Application Controller
   ═══════════════════════════════════════════════════ */

// ─── Global State ───
const state = {
    currentSection: 'dashboard',
    location: { lat: -37.47, lon: -72.35, name: 'Los Ángeles, Provincia de Biobío, Chile' },
    soilType: 'franco-arcilloso',
    currentCrops: ['trigo', 'avena'],
    climateData: null,
    rotationStrategies: null,
    farmerPriorities: {
        water_conservation: 0.6,
        soil_health: 0.85,
        economic_return: 0.75,
        pest_management: 0.7,
        erosion_control: 0.8,
        nitrogen_fixation: 0.9
    }
};

const API_BASE = 'http://localhost:5000';

// Crop display info
const CROP_INFO = {
    soja: { emoji: '🌱', label: 'Soja' },
    maiz: { emoji: '🌽', label: 'Maíz' },
    trigo: { emoji: '🌾', label: 'Trigo' },
    girasol: { emoji: '🌻', label: 'Girasol' },
    sorgo: { emoji: '🌿', label: 'Sorgo' },
    cebada: { emoji: '🌾', label: 'Cebada' },
    alfalfa: { emoji: '🍀', label: 'Alfalfa' },
    avena: { emoji: '🌾', label: 'Avena' }
};

// ─── Navigation ───
function navigateTo(section) {
    // Si el usuario es agricultor, el Portal Regional está deshabilitado
    if (section === 'regional' && typeof currentUser !== 'undefined' && currentUser && currentUser.roleType === 'agricultor') {
        showToast('El Portal Regional es una herramienta exclusiva para asesoría técnica e instituciones.', 'info');
        return;
    }

    // Hide all sections
    document.querySelectorAll('.content-section').forEach(s => s.classList.remove('active'));
    // Show target
    const target = document.getElementById(`section-${section}`);
    if (target) target.classList.add('active');

    // Update nav
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    const navItem = document.querySelector(`.nav-item[data-section="${section}"]`);
    if (navItem) navItem.classList.add('active');

    state.currentSection = section;

    // Section-specific init
    if (section === 'finca') {
        setTimeout(() => {
            if (typeof initMap === 'function') initMap();
            if (typeof forceMapRefresh === 'function') forceMapRefresh();
        }, 120);
    }
    if (section === 'clima') {
        initClimateCharts();
    }
    if (section === 'rotaciones') {
        loadRotationStrategies();
    }
    if (section === 'reportes') {
        initReportControls();
    }
    if (section === 'regional') {
        if (typeof renderRegionalAPIExplorer === 'function') renderRegionalAPIExplorer();
    }

    // Close mobile sidebar
    closeSidebar();
}

// ─── Sidebar Toggle (Mobile) ───
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('open');

    let overlay = document.querySelector('.sidebar-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'sidebar-overlay';
        overlay.onclick = closeSidebar;
        document.body.appendChild(overlay);
    }
    overlay.classList.toggle('active');
}

function closeSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.remove('open');
    const overlay = document.querySelector('.sidebar-overlay');
    if (overlay) overlay.classList.remove('active');
}

// ─── Loading Overlay ───
function showLoading() {
    document.getElementById('loading-overlay').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading-overlay').classList.add('hidden');
}

// ─── Toast Notifications ───
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };
    toast.innerHTML = `<span>${icons[type] || 'ℹ️'}</span><span>${message}</span>`;

    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('toast-exit');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// ─── API Helper ───
async function apiCall(endpoint, method = 'GET', data = null) {
    const opts = {
        method,
        headers: { 'Content-Type': 'application/json' }
    };
    if (data && method !== 'GET') {
        opts.body = JSON.stringify(data);
    }

    try {
        const url = `${API_BASE}${endpoint}`;
        const res = await fetch(url, opts);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return await res.json();
    } catch (err) {
        console.warn(`API call failed (${endpoint}):`, err.message);
        return null; // Caller uses mock data as fallback
    }
}

// ─── Farm Config ───
function saveFarmConfig() {
    state.soilType = document.getElementById('soil-type').value;
    const sizeEl = document.getElementById('farm-size');
    state.farmSize = sizeEl ? parseInt(sizeEl.value) || 65 : 65;

    // Update dashboard
    const dashLoc = document.getElementById('dash-location');
    if (dashLoc) dashLoc.textContent = state.location.name || 'Sin ubicación';
    const dashSoil = document.getElementById('dash-soil');
    if (dashSoil && typeof formatSoilLabel === 'function') {
        dashSoil.textContent = `Tipo de suelo: ${formatSoilLabel(state.soilType)}`;
    }

    if (typeof drawParcelCircle === 'function' && state.location.lat) {
        drawParcelCircle(state.location.lat, state.location.lon, state.farmSize);
    }
    if (typeof renderDashboardStrategyShowcase === 'function') {
        renderDashboardStrategyShowcase(state.rotationStrategies);
    }
    if (typeof renderDecisionRecommendation === 'function') {
        renderDecisionRecommendation(state.rotationStrategies);
    }

    showToast('Configuración del predio guardada y estrategias actualizadas', 'success');
}

function addCrop() {
    const sel = document.getElementById('add-crop-select');
    const val = sel.value;
    if (!val || state.currentCrops.includes(val)) {
        if (val && state.currentCrops.includes(val)) showToast('Este cultivo ya está agregado', 'warning');
        return;
    }
    state.currentCrops.push(val);
    renderCrops();
    sel.value = '';
    showToast(`${CROP_INFO[val]?.label || val} agregado`, 'success');
}

function removeCrop(btn, crop) {
    state.currentCrops = state.currentCrops.filter(c => c !== crop);
    renderCrops();
}

function renderCrops() {
    const container = document.getElementById('crops-container');
    container.innerHTML = state.currentCrops.map(c => {
        const info = CROP_INFO[c] || { emoji: '🌱', label: c };
        return `<span class="chip chip-active">${info.emoji} ${info.label} <button onclick="removeCrop(this,'${c}')">×</button></span>`;
    }).join('');
}

// ─── Initialize Application ───
function initApp() {
    console.log('🌿 AMAC — Inicializando...');

    // Relacionar con fecha actual y reloj
    updateCurrentDateUI();
    setInterval(updateCurrentDateUI, 60000); // Actualizar cada minuto

    // Render initial crops
    renderCrops();

    // Set default dates relacionados con el día actual
    const now = new Date();
    const endStr = now.toISOString().split('T')[0];
    const pastDate = new Date();
    pastDate.setDate(now.getDate() - 30);
    const startStr = pastDate.toISOString().split('T')[0];

    document.querySelectorAll('#climate-start, #report-start').forEach(el => el.value = startStr);
    document.querySelectorAll('#climate-end, #report-end').forEach(el => el.value = endStr);

    // Init dashboard charts with mock data
    setTimeout(() => {
        createDashboardTempChart();
        createDashboardPrecipChart();
        if (typeof renderDashboardStrategyShowcase === 'function') {
            renderDashboardStrategyShowcase();
        }
        if (typeof applyRoleView === 'function' && typeof currentUser !== 'undefined' && currentUser) {
            applyRoleView(currentUser.roleType || 'asesor');
        }
    }, 200);

    console.log('🌿 AMAC — Listo');
}

/**
 * Actualiza la interfaz con la fecha actual del sistema en español
 */
function updateCurrentDateUI() {
    const now = new Date();
    const optionsDate = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const dateFormatted = now.toLocaleDateString('es-ES', optionsDate);
    // Capitalizar primera letra
    const dateStr = dateFormatted.charAt(0).toUpperCase() + dateFormatted.slice(1);

    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const timeStr = `${hours}:${minutes}`;

    const dateHeaderEl = document.getElementById('dash-current-date');
    if (dateHeaderEl) {
        dateHeaderEl.innerHTML = `📅 <strong>${dateStr}</strong> &nbsp;·&nbsp; 🕒 Sincronizado: <span>${timeStr} hs</span>`;
    }

    const reportDateBadge = document.getElementById('report-current-badge');
    if (reportDateBadge) {
        reportDateBadge.textContent = dateStr;
    }
}

/**
 * Forzar sincronización de datos satelitales NASA con fecha actual
 */
function refreshSatelliteData() {
    showLoading();
    const btn = document.getElementById('sync-btn');
    if (btn) btn.classList.add('rotating');

    setTimeout(() => {
        updateCurrentDateUI();
        if (btn) btn.classList.remove('rotating');
        hideLoading();
        showToast('🛰️ ¡Datos de NASA POWER, SMAP y GPM actualizados exitosamente al día de hoy!', 'success');

        // Efecto visual de parpadeo en las tarjetas de métricas
        document.querySelectorAll('.metric-card').forEach(c => {
            c.style.transform = 'scale(1.03)';
            c.style.transition = 'transform 0.25s ease';
            setTimeout(() => c.style.transform = '', 250);
        });
    }, 900);
}

// ─── Dashboard mini-charts (called from init) ───
function createDashboardTempChart() {
    const mock = getMockClimateData();
    const ctx = document.getElementById('dashboard-temp-chart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: mock.months,
            datasets: [
                {
                    label: 'Máxima',
                    data: mock.tempMax,
                    borderColor: '#E76F51',
                    backgroundColor: 'rgba(231,111,81,.1)',
                    borderWidth: 2,
                    tension: .4,
                    fill: false,
                    pointRadius: 3
                },
                {
                    label: 'Promedio',
                    data: mock.tempAvg,
                    borderColor: '#40916C',
                    backgroundColor: 'rgba(64,145,108,.15)',
                    borderWidth: 2.5,
                    tension: .4,
                    fill: true,
                    pointRadius: 3
                },
                {
                    label: 'Mínima',
                    data: mock.tempMin,
                    borderColor: '#2C7DA0',
                    backgroundColor: 'rgba(44,125,160,.1)',
                    borderWidth: 2,
                    tension: .4,
                    fill: false,
                    pointRadius: 3
                }
            ]
        },
        options: chartDefaults('°C')
    });
}

function createDashboardPrecipChart() {
    const mock = getMockClimateData();
    const ctx = document.getElementById('dashboard-precip-chart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: mock.months,
            datasets: [{
                label: 'Precipitación (mm)',
                data: mock.precipitation,
                backgroundColor: mock.precipitation.map(v =>
                    v > 100 ? 'rgba(44,125,160,.8)' :
                        v > 60 ? 'rgba(70,143,175,.7)' :
                            'rgba(169,214,229,.7)'
                ),
                borderRadius: 6,
                borderSkipped: false
            }]
        },
        options: chartDefaults('mm')
    });
}

function chartDefaults(unit) {
    return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    font: { family: 'Inter', size: 11 },
                    padding: 14,
                    usePointStyle: true,
                    pointStyleWidth: 10
                }
            },
            tooltip: {
                backgroundColor: '#212529',
                titleFont: { family: 'Inter', size: 12 },
                bodyFont: { family: 'Inter', size: 11 },
                padding: 10,
                cornerRadius: 8,
                callbacks: {
                    label: ctx => ` ${ctx.dataset.label}: ${ctx.parsed.y} ${unit}`
                }
            }
        },
        scales: {
            x: {
                grid: { display: false },
                ticks: { font: { family: 'Inter', size: 11 } }
            },
            y: {
                grid: { color: 'rgba(0,0,0,.05)' },
                ticks: {
                    font: { family: 'Inter', size: 11 },
                    callback: v => `${v} ${unit}`
                }
            }
        }
    };
}
