/* ═══════════════════════════════════════════════════
   AMAC — charts.js  ·  Chart.js Visualizations
   ═══════════════════════════════════════════════════ */

// Track chart instances for cleanup
const chartInstances = {};

function destroyChart(id) {
    if (chartInstances[id]) {
        chartInstances[id].destroy();
        delete chartInstances[id];
    }
}

// ─── Chart Color Palette ───
const CHART_COLORS = {
    green:    { bg: 'rgba(64,145,108,.2)',  border: '#40916C' },
    greenDk:  { bg: 'rgba(45,106,79,.2)',   border: '#2D6A4F' },
    blue:     { bg: 'rgba(44,125,160,.2)',   border: '#2C7DA0' },
    blueLt:   { bg: 'rgba(97,165,194,.2)',   border: '#61A5C2' },
    orange:   { bg: 'rgba(231,111,81,.2)',   border: '#E76F51' },
    yellow:   { bg: 'rgba(244,162,97,.2)',   border: '#F4A261' },
    teal:     { bg: 'rgba(82,183,136,.2)',   border: '#52B788' },
    red:      { bg: 'rgba(230,57,70,.2)',    border: '#E63946' }
};

const MONTHS_ES = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'];

// ─── Shared Defaults ───
function baseChartOptions(yUnit = '', extra = {}) {
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
                    label: ctx => ` ${ctx.dataset.label}: ${ctx.parsed.y}${yUnit ? ' ' + yUnit : ''}`
                }
            },
            ...extra.plugins
        },
        scales: {
            x: {
                grid: { display: false },
                ticks: { font: { family: 'Inter', size: 11 } },
                ...extra.x
            },
            y: {
                grid: { color: 'rgba(0,0,0,.05)' },
                ticks: {
                    font: { family: 'Inter', size: 11 },
                    callback: v => yUnit ? `${v} ${yUnit}` : v
                },
                ...extra.y
            }
        },
        ...extra.root
    };
}

// ═══════════════ TEMPERATURE CHART ═══════════════
function createTemperatureChart(data) {
    const id = 'climate-temp-chart';
    destroyChart(id);
    const ctx = document.getElementById(id);
    if (!ctx) return;

    const d = data || getMockClimateData();

    chartInstances[id] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: d.months,
            datasets: [
                {
                    label: 'Temperatura Máxima',
                    data: d.tempMax,
                    borderColor: CHART_COLORS.orange.border,
                    backgroundColor: CHART_COLORS.orange.bg,
                    borderWidth: 2,
                    tension: .4,
                    fill: false,
                    pointRadius: 4,
                    pointHoverRadius: 6
                },
                {
                    label: 'Temperatura Promedio',
                    data: d.tempAvg,
                    borderColor: CHART_COLORS.green.border,
                    backgroundColor: CHART_COLORS.green.bg,
                    borderWidth: 2.5,
                    tension: .4,
                    fill: '+1',
                    pointRadius: 4,
                    pointHoverRadius: 6
                },
                {
                    label: 'Temperatura Mínima',
                    data: d.tempMin,
                    borderColor: CHART_COLORS.blue.border,
                    backgroundColor: CHART_COLORS.blue.bg,
                    borderWidth: 2,
                    tension: .4,
                    fill: false,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }
            ]
        },
        options: baseChartOptions('°C')
    });
}

// ═══════════════ PRECIPITATION CHART ═══════════════
function createPrecipitationChart(data) {
    const id = 'climate-precip-chart';
    destroyChart(id);
    const ctx = document.getElementById(id);
    if (!ctx) return;

    const d = data || getMockClimateData();

    chartInstances[id] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: d.months,
            datasets: [{
                label: 'Precipitación',
                data: d.precipitation,
                backgroundColor: d.precipitation.map(v =>
                    v > 120 ? 'rgba(27,73,101,.85)' :
                    v > 80  ? 'rgba(44,125,160,.75)' :
                    v > 40  ? 'rgba(70,143,175,.65)' :
                              'rgba(169,214,229,.6)'
                ),
                borderRadius: 6,
                borderSkipped: false
            }]
        },
        options: baseChartOptions('mm')
    });
}

// ═══════════════ SOIL MOISTURE CHART ═══════════════
function createSoilMoistureChart(data) {
    const id = 'climate-moisture-chart';
    destroyChart(id);
    const ctx = document.getElementById(id);
    if (!ctx) return;

    const d = data || getMockClimateData();

    chartInstances[id] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: d.months,
            datasets: [{
                label: 'Humedad del Suelo',
                data: d.soilMoisture,
                borderColor: CHART_COLORS.blue.border,
                backgroundColor: 'rgba(44,125,160,.15)',
                borderWidth: 2.5,
                tension: .4,
                fill: true,
                pointRadius: 4,
                pointHoverRadius: 6,
                pointBackgroundColor: '#fff',
                pointBorderColor: CHART_COLORS.blue.border,
                pointBorderWidth: 2
            },
            {
                label: 'Nivel Óptimo',
                data: d.months.map(() => 50),
                borderColor: 'rgba(64,145,108,.5)',
                borderDash: [6, 4],
                borderWidth: 2,
                pointRadius: 0,
                fill: false
            }]
        },
        options: baseChartOptions('%')
    });
}

// ═══════════════ CLIMATE OVERVIEW CHART ═══════════════
function createClimateOverviewChart(data) {
    const id = 'climate-overview-chart';
    destroyChart(id);
    const ctx = document.getElementById(id);
    if (!ctx) return;

    const d = data || getMockClimateData();

    chartInstances[id] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: d.months,
            datasets: [
                {
                    type: 'line',
                    label: 'Temperatura (°C)',
                    data: d.tempAvg,
                    borderColor: CHART_COLORS.orange.border,
                    backgroundColor: 'transparent',
                    borderWidth: 2.5,
                    tension: .4,
                    pointRadius: 3,
                    yAxisID: 'yTemp',
                    order: 0
                },
                {
                    type: 'bar',
                    label: 'Precipitación (mm)',
                    data: d.precipitation,
                    backgroundColor: 'rgba(44,125,160,.55)',
                    borderRadius: 5,
                    borderSkipped: false,
                    yAxisID: 'yPrecip',
                    order: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { font: { family: 'Inter', size: 11 }, padding: 14, usePointStyle: true }
                },
                tooltip: {
                    backgroundColor: '#212529',
                    titleFont: { family: 'Inter', size: 12 },
                    bodyFont: { family: 'Inter', size: 11 },
                    padding: 10,
                    cornerRadius: 8
                }
            },
            scales: {
                x: { grid: { display: false }, ticks: { font: { family: 'Inter', size: 11 } } },
                yTemp: {
                    type: 'linear',
                    position: 'left',
                    title: { display: true, text: 'Temperatura (°C)', font: { family: 'Inter', size: 11 } },
                    grid: { color: 'rgba(0,0,0,.05)' },
                    ticks: { font: { family: 'Inter', size: 10 }, callback: v => `${v}°C` }
                },
                yPrecip: {
                    type: 'linear',
                    position: 'right',
                    title: { display: true, text: 'Precipitación (mm)', font: { family: 'Inter', size: 11 } },
                    grid: { display: false },
                    ticks: { font: { family: 'Inter', size: 10 }, callback: v => `${v} mm` }
                }
            }
        }
    });
}

// ═══════════════ STRATEGY RADAR CHART ═══════════════
function createStrategyRadarChart(strategies) {
    const id = 'strategy-radar-chart';
    destroyChart(id);
    const ctx = document.getElementById(id);
    if (!ctx) return;

    const strats = strategies || getMockStrategies();
    const radarColors = [
        { bg: 'rgba(64,145,108,.2)',  border: '#40916C' },
        { bg: 'rgba(44,125,160,.2)',  border: '#2C7DA0' },
        { bg: 'rgba(231,111,81,.2)',  border: '#E76F51' }
    ];

    const labels = [
        'Conservación de Agua',
        'Salud del Suelo',
        'Retorno Económico',
        'Manejo de Plagas',
        'Control de Erosión',
        'Fijación de Nitrógeno'
    ];

    const datasets = strats.map((s, i) => ({
        label: s.name,
        data: [
            s.scores.water_conservation,
            s.scores.soil_health,
            s.scores.economic_return,
            s.scores.pest_management,
            s.scores.erosion_control,
            s.scores.nitrogen_fixation
        ],
        borderColor: radarColors[i % radarColors.length].border,
        backgroundColor: radarColors[i % radarColors.length].bg,
        borderWidth: 2.5,
        pointRadius: 4,
        pointHoverRadius: 6,
        pointBackgroundColor: '#fff',
        pointBorderWidth: 2,
        pointBorderColor: radarColors[i % radarColors.length].border
    }));

    chartInstances[id] = new Chart(ctx, {
        type: 'radar',
        data: { labels, datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { font: { family: 'Inter', size: 12 }, padding: 16, usePointStyle: true }
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        stepSize: 20,
                        font: { family: 'Inter', size: 10 },
                        backdropColor: 'transparent'
                    },
                    grid: { color: 'rgba(0,0,0,.06)' },
                    angleLines: { color: 'rgba(0,0,0,.06)' },
                    pointLabels: {
                        font: { family: 'Inter', size: 11, weight: '500' },
                        color: '#495057'
                    }
                }
            }
        }
    });
}

// ═══════════════ INIT CLIMATE CHARTS ═══════════════
function initClimateCharts() {
    const data = state.climateData || getMockClimateData();
    createTemperatureChart(data);
    createPrecipitationChart(data);
    createSoilMoistureChart(data);
    createClimateOverviewChart(data);
}
