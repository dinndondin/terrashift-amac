/* ═══════════════════════════════════════════════════
   AMAC — nasa-data.js  ·  NASA Data Client & Mock
   ═══════════════════════════════════════════════════ */

// ─── Mock Climate Data (Región del Biobío, Chile — Régimen Mediterráneo) ───
function getMockClimateData() {
    return {
        months: ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'],
        tempMax:  [28.4, 27.9, 24.8, 19.8, 15.2, 12.4, 12.1, 13.8, 16.6, 19.9, 23.5, 26.8],
        tempAvg:  [20.6, 20.1, 17.5, 13.8, 10.6,  8.4,  7.9,  9.0, 11.0, 13.6, 16.4, 19.1],
        tempMin:  [12.8, 12.3, 10.2,  7.8,  6.0,  4.4,  3.7,  4.2,  5.4,  7.3,  9.3, 11.4],
        precipitation: [18, 22, 38, 72, 175, 215, 195, 155, 75, 42, 24, 20],
        soilMoisture: [33, 31, 35, 46, 65, 76, 78, 74, 62, 50, 41, 36],
        humidity:  [56, 58, 64, 74, 83, 86, 85, 82, 76, 69, 62, 58],
        solarRadiation: [25.8, 22.4, 17.6, 12.2, 7.9, 6.2, 6.9, 9.8, 14.5, 19.3, 23.4, 25.9],
        windSpeed: [3.6, 3.4, 3.1, 2.8, 3.3, 3.9, 3.7, 3.5, 3.2, 3.3, 3.5, 3.7],
        summary: {
            avgTemp: 14.0,
            totalPrecip: 1051,
            maxTemp: 28.4,
            minTemp: 3.7,
            avgMoisture: 52.1,
            avgHumidity: 71.1
        }
    };
}

// ─── Fetch Climate Data from Backend ───
async function fetchClimateData(lat, lon, startDate, endDate) {
    const params = new URLSearchParams({
        lat: lat || state.location.lat,
        lon: lon || state.location.lon,
        start_date: startDate,
        end_date: endDate
    });

    const data = await apiCall(`/api/climate?${params}`);
    return data;
}

// ─── Fetch Climate Analysis ───
async function fetchClimateAnalysis(lat, lon) {
    const params = new URLSearchParams({
        lat: lat || state.location.lat,
        lon: lon || state.location.lon
    });

    const data = await apiCall(`/api/climate/analysis?${params}`);
    return data;
}

// ─── Process Raw Climate Data for Charts ───
function processClimateData(rawData) {
    if (!rawData || !rawData.parameters) return getMockClimateData();

    const params = rawData.parameters;
    const months = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'];

    // Group daily data by month
    const monthlyData = {};
    for (let m = 0; m < 12; m++) {
        monthlyData[m] = { tempMax: [], tempMin: [], tempAvg: [], precip: [], moisture: [] };
    }

    // Process T2M (temperature), PRECTOTCORR (precipitation), etc.
    if (params.T2M) {
        Object.entries(params.T2M).forEach(([dateStr, val]) => {
            if (val === -999) return;
            const month = parseInt(dateStr.substring(4, 6)) - 1;
            if (monthlyData[month]) monthlyData[month].tempAvg.push(val);
        });
    }
    if (params.T2M_MAX) {
        Object.entries(params.T2M_MAX).forEach(([dateStr, val]) => {
            if (val === -999) return;
            const month = parseInt(dateStr.substring(4, 6)) - 1;
            if (monthlyData[month]) monthlyData[month].tempMax.push(val);
        });
    }
    if (params.T2M_MIN) {
        Object.entries(params.T2M_MIN).forEach(([dateStr, val]) => {
            if (val === -999) return;
            const month = parseInt(dateStr.substring(4, 6)) - 1;
            if (monthlyData[month]) monthlyData[month].tempMin.push(val);
        });
    }
    if (params.PRECTOTCORR) {
        Object.entries(params.PRECTOTCORR).forEach(([dateStr, val]) => {
            if (val === -999) return;
            const month = parseInt(dateStr.substring(4, 6)) - 1;
            if (monthlyData[month]) monthlyData[month].precip.push(val);
        });
    }

    // Average monthly values
    const avg = arr => arr.length ? Math.round((arr.reduce((a, b) => a + b, 0) / arr.length) * 10) / 10 : 0;
    const sum = arr => arr.length ? Math.round(arr.reduce((a, b) => a + b, 0) * 10) / 10 : 0;

    const tempMax = months.map((_, i) => avg(monthlyData[i].tempMax));
    const tempMin = months.map((_, i) => avg(monthlyData[i].tempMin));
    const tempAvg = months.map((_, i) => avg(monthlyData[i].tempAvg));
    const precipitation = months.map((_, i) => Math.round(sum(monthlyData[i].precip)));

    // Estimate soil moisture from precipitation (simplified)
    const soilMoisture = precipitation.map(p => Math.min(80, Math.max(20, Math.round(25 + p * 0.25))));

    return {
        months,
        tempMax,
        tempMin,
        tempAvg,
        precipitation,
        soilMoisture,
        summary: calculateClimateSummary({ tempMax, tempMin, tempAvg, precipitation, soilMoisture })
    };
}

// ─── Calculate Summary Statistics ───
function calculateClimateSummary(data) {
    const avg = arr => arr.length ? Math.round((arr.reduce((a, b) => a + b, 0) / arr.length) * 10) / 10 : 0;

    return {
        avgTemp: avg(data.tempAvg),
        totalPrecip: Math.round(data.precipitation.reduce((a, b) => a + b, 0)),
        maxTemp: Math.max(...data.tempMax),
        minTemp: Math.min(...data.tempMin),
        avgMoisture: avg(data.soilMoisture)
    };
}

// ─── Format for Spanish Display ───
function formatClimateForDisplay(data) {
    const d = data || getMockClimateData();
    const s = d.summary || calculateClimateSummary(d);

    return {
        avgTemp: `${s.avgTemp}°C`,
        totalPrecip: `${s.totalPrecip.toLocaleString('es-AR')} mm`,
        maxTemp: `${s.maxTemp}°C`,
        minTemp: `${s.minTemp}°C`,
        avgMoisture: `${s.avgMoisture}%`
    };
}

// ─── Load Climate Data (called from UI) ───
async function loadClimateData() {
    const startDate = document.getElementById('climate-start').value;
    const endDate = document.getElementById('climate-end').value;

    showLoading();

    try {
        const rawData = await fetchClimateData(state.location.lat, state.location.lon, startDate, endDate);

        if (rawData) {
            state.climateData = processClimateData(rawData);
            showToast('Datos climáticos actualizados desde NASA POWER', 'success');
        } else {
            state.climateData = getMockClimateData();
            showToast('Usando datos de muestra (el servidor no está disponible)', 'warning');
        }

        // Update summary cards
        const display = formatClimateForDisplay(state.climateData);
        document.getElementById('climate-avg-temp').textContent = display.avgTemp;
        document.getElementById('climate-total-precip').textContent = display.totalPrecip;
        document.getElementById('climate-max-temp').textContent = display.maxTemp;
        document.getElementById('climate-min-temp').textContent = display.minTemp;

        // Refresh charts
        initClimateCharts();

    } catch (err) {
        console.error('Error loading climate data:', err);
        state.climateData = getMockClimateData();
        initClimateCharts();
        showToast('Error cargando datos. Usando datos de muestra.', 'error');
    } finally {
        hideLoading();
    }
}
