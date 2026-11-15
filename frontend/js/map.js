/* ═══════════════════════════════════════════════════
   AMAC — map.js  ·  Módulo Geoespacial Leaflet Mejorado
   NASA Space Apps Challenge 2026
   ═══════════════════════════════════════════════════ */

let map = null;
let marker = null;
let parcelCircle = null;
let baseLayers = {};
let amacPinIcon = null;
let _mapResizeObserver = null;
window._mapInitialized = false;

function buildAmacPinIcon() {
    if (typeof L === 'undefined') return null;
    if (amacPinIcon) return amacPinIcon;
    amacPinIcon = L.divIcon({
        html: `
            <div style="
                position: relative;
                width: 38px;
                height: 38px;
                background: linear-gradient(135deg, #2D6A4F 0%, #52B788 100%);
                border: 3px solid #ffffff;
                border-radius: 50% 50% 50% 0;
                transform: rotate(-45deg);
                box-shadow: 0 4px 14px rgba(0,0,0,0.4);
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
            ">
                <span style="transform: rotate(45deg); font-size: 18px;">🌾</span>
            </div>
        `,
        className: 'amac-custom-marker',
        iconSize: [38, 38],
        iconAnchor: [19, 38],
        popupAnchor: [0, -40]
    });
    return amacPinIcon;
}

/**
 * Inicializa el mapa interactivo de forma segura y resistente
 */
function initMap() {
    const mapEl = document.getElementById('farm-map');
    if (!mapEl) return;

    if (typeof L === 'undefined') {
        mapEl.innerHTML = `
            <div style="height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:24px;text-align:center;background:#eef7f2;color:#2D6A4F;border-radius:12px;">
                <span style="font-size:2.2rem;margin-bottom:8px;">🛰️</span>
                <strong>Mapa satelital en modo sin conexión</strong>
                <p style="font-size:0.85rem;margin-top:6px;max-width:360px;">Verifica tu conexión a internet para cargar las imágenes satelitales de ESRI / OpenStreetMap. Los cálculos locales de suelo y clima siguen activos.</p>
            </div>
        `;
        return;
    }

    // Si el mapa ya fue creado previamente, sólo forzamos re-dimensionado y centrado
    if (map && window._mapInitialized) {
        forceMapRefresh();
        return;
    }

    // Asegurar que el contenedor tenga altura explícita en el DOM
    mapEl.style.height = '440px';
    mapEl.style.minHeight = '420px';
    mapEl.style.width = '100%';
    mapEl.style.display = 'block';

    const defaultLat = state.location.lat || -37.47;
    const defaultLon = state.location.lon || -72.35;

    try {
        // Si había una instancia residual de Leaflet en el contenedor, limpiarla
        if (mapEl._leaflet_id) {
            mapEl._leaflet_id = null;
        }

        map = L.map('farm-map', {
            center: [defaultLat, defaultLon],
            zoom: 12,
            zoomControl: true,
            scrollWheelZoom: true
        });
        window.map = map;

        // 1. Capa Satelital de Alta Resolución (ESRI World Imagery - Excelente para campos agrícolas)
        const satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
            maxZoom: 18
        });

        // 2. Capa Mapa Terrestre / OpenStreetMap
        const osmLayer = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 19
        });

        // 3. Capa Topográfica CartoDB
        const lightLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; CartoDB',
            maxZoom: 19
        });

        // Capa activa por defecto: Satelital para ver los lotes de cultivo
        satelliteLayer.addTo(map);

        // Control de capas para alternar con 1 clic
        baseLayers = {
            "🛰️ Satelital (Alta Resolución)": satelliteLayer,
            "🗺️ Terrestre / Caminos (OSM)": osmLayer,
            "🌱 Topográfico Claro": lightLayer
        };
        L.control.layers(baseLayers, null, { position: 'topright' }).addTo(map);

        // Marcador inicial
        const icon = buildAmacPinIcon();
        marker = L.marker([defaultLat, defaultLon], icon ? { icon, draggable: true } : { draggable: true }).addTo(map);

        // Parcela visual aproximada (círculo representativo de hectáreas)
        drawParcelCircle(defaultLat, defaultLon, state.farmSize || 65);

        // Actualizar popup
        updatePopupText(state.location.name || 'Mi Lote Agrícola');

        // Evento de clic en cualquier lugar del mapa
        map.on('click', async (e) => {
            const { lat, lng } = e.latlng;
            updateMapMarker(lat, lng);
            await reverseGeocode(lat, lng);
        });

        // Evento al arrastrar el pin
        marker.on('dragend', async (e) => {
            const pos = e.target.getLatLng();
            updateMapMarker(pos.lat, pos.lng);
            await reverseGeocode(pos.lat, pos.lng);
        });

        // Revalidar tamaño automáticamente cuando el contenedor cambia de visibilidad o ancho
        if (typeof ResizeObserver !== 'undefined' && !_mapResizeObserver) {
            _mapResizeObserver = new ResizeObserver(() => {
                if (map) map.invalidateSize();
            });
            _mapResizeObserver.observe(mapEl);
        }

        window._mapInitialized = true;

        // Múltiples revalidaciones para asegurar que los tiles no se corten
        forceMapRefresh();

        console.log('🗺️ Mapa AMAC inicializado con éxito');
    } catch (err) {
        console.error('Error al inicializar mapa:', err);
    }
}

/**
 * Dibuja un área circular visual estimada de la superficie de la finca en hectáreas
 */
function drawParcelCircle(lat, lon, hectares) {
    if (!map) return;

    if (parcelCircle) {
        map.removeLayer(parcelCircle);
    }

    // Radio aproximado: 1 ha = 10.000 m2 -> radio aprox sqrt(hectareas * 10000 / PI)
    const radiusMeters = Math.max(250, Math.round(Math.sqrt((hectares * 10000) / Math.PI)));

    parcelCircle = L.circle([lat, lon], {
        color: '#52B788',
        fillColor: '#40916C',
        fillOpacity: 0.25,
        weight: 2,
        dashArray: '4, 6',
        radius: radiusMeters
    }).addTo(map);

    parcelCircle.bindTooltip(`Área estimada del lote: ~${hectares} ha`, { permanent: false, direction: 'top' });
}

/**
 * Revalida el tamaño del mapa en varios momentos para evitar el problema de pantalla gris
 */
function forceMapRefresh() {
    if (!map) return;
    const delays = [50, 150, 300, 600, 1000];
    delays.forEach(d => {
        setTimeout(() => {
            if (map) {
                map.invalidateSize();
            }
        }, d);
    });
}

/**
 * Actualiza la posición del pin y el círculo en el mapa
 */
function updateMapMarker(lat, lon) {
    state.location.lat = Math.round(lat * 10000) / 10000;
    state.location.lon = Math.round(lon * 10000) / 10000;

    if (marker && map) {
        marker.setLatLng([lat, lon]);
    }

    drawParcelCircle(lat, lon, state.farmSize || 180);

    // Actualizar etiquetas en la interfaz
    const latEl = document.getElementById('sel-lat');
    const lonEl = document.getElementById('sel-lon');
    if (latEl) latEl.textContent = state.location.lat.toFixed(4);
    if (lonEl) lonEl.textContent = state.location.lon.toFixed(4);

    const coordsDisplay = document.getElementById('soilgrids-coords-display');
    if (coordsDisplay) coordsDisplay.textContent = `Lat: ${state.location.lat.toFixed(4)}, Lon: ${state.location.lon.toFixed(4)}`;

    // Consultar SoilGrids para el nuevo punto
    if (typeof fetchSoilGridsData === 'function') {
        fetchSoilGridsData(lat, lon).then(data => {
            if (!data) return;
            const texEl = document.getElementById('sg-texture');
            const omEl = document.getElementById('sg-om');
            const phEl = document.getElementById('sg-ph');
            const cecEl = document.getElementById('sg-cec');
            if (texEl) texEl.textContent = data.textureClass;
            if (omEl) omEl.textContent = `${data.organicMatterPercent}% (${data.organicMatterPercent > 3 ? 'Alta' : 'Media'})`;
            if (phEl) phEl.textContent = `${data.ph} (${data.ph < 6 ? 'Ácido/Trumao' : 'Neutro'})`;
            if (cecEl) cecEl.textContent = `${data.cec} mmol/kg`;
        });
    }

    updatePopupText(state.location.name || 'Lote seleccionado');

    // Notificar al agricultor
    showToast(`Ubicación actualizada: [${state.location.lat.toFixed(3)}, ${state.location.lon.toFixed(3)}]`, 'info');
}

/**
 * Actualiza el texto del popup sobre el marcador
 */
function updatePopupText(title) {
    if (!marker) return;
    marker.bindPopup(`
        <div style="font-family: 'Inter', sans-serif; padding: 4px; min-width: 170px;">
            <strong style="color: #2D6A4F; font-size: 14px; display: block; margin-bottom: 4px;">📍 ${title}</strong>
            <div style="font-size: 12px; color: #495057;">Lat: <strong>${state.location.lat.toFixed(4)}</strong></div>
            <div style="font-size: 12px; color: #495057;">Lon: <strong>${state.location.lon.toFixed(4)}</strong></div>
            <div style="margin-top: 6px; padding-top: 6px; border-top: 1px solid #e9ecef; font-size: 11px; color: #6c757d;">
                🌱 Superficie: ~${state.farmSize || 180} ha
            </div>
        </div>
    `).openPopup();
}

/**
 * Geocodificación inversa con OpenStreetMap Nominatim y respaldo instantáneo
 */
async function reverseGeocode(lat, lon) {
    const locText = document.getElementById('selected-location');
    const dashLoc = document.getElementById('dash-location');

    try {
        const url = `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json&accept-language=es`;
        const res = await fetch(url, { headers: { 'Accept': 'application/json' } });
        if (!res.ok) throw new Error('Geocoding error');
        const data = await res.json();

        let cleanName = '';
        if (data && data.address) {
            const a = data.address;
            const parts = [a.county || a.city || a.town || a.village, a.state, a.country].filter(Boolean);
            cleanName = parts.slice(0, 2).join(', ') || data.display_name.split(',').slice(0, 3).join(',');
        } else {
            cleanName = `Coordenadas: ${lat.toFixed(2)}, ${lon.toFixed(2)}`;
        }

        state.location.name = cleanName;
        if (locText) locText.textContent = cleanName;
        if (dashLoc) dashLoc.textContent = cleanName;
        updatePopupText(cleanName);
    } catch (err) {
        const fallbackName = `Lat: ${lat.toFixed(2)}, Lon: ${lon.toFixed(2)}`;
        state.location.name = fallbackName;
        if (locText) locText.textContent = fallbackName;
        if (dashLoc) dashLoc.textContent = fallbackName;
    }
}

/**
 * Buscar ubicación por texto
 */
async function searchLocation(query) {
    if (!query || !query.trim()) {
        showToast('Ingrese una ciudad o región para buscar', 'warning');
        return;
    }

    showLoading();
    try {
        const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query)}&format=json&limit=1&accept-language=es`;
        const res = await fetch(url);
        const data = await res.json();

        if (data && data.length > 0) {
            const lat = parseFloat(data[0].lat);
            const lon = parseFloat(data[0].lon);
            const name = data[0].display_name.split(',').slice(0, 3).join(',');

            state.location.name = name;
            updateMapMarker(lat, lon);
            if (map) {
                map.setView([lat, lon], 12);
            }
            showToast(`Ubicación encontrada: ${name}`, 'success');
        } else {
            showToast('No se encontró esa ubicación. Intente con otra ciudad.', 'warning');
        }
    } catch (err) {
        showToast('Error al conectar con el servicio de búsqueda.', 'error');
    } finally {
        hideLoading();
    }
}

/**
 * Centrar mapa en la ubicación GPS real del dispositivo del usuario
 */
function useCurrentGPSLocation() {
    if (!navigator.geolocation) {
        showToast('Tu navegador no soporta geolocalización GPS.', 'warning');
        return;
    }

    showLoading();
    navigator.geolocation.getCurrentPosition(
        async (position) => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            updateMapMarker(lat, lon);
            if (map) {
                map.setView([lat, lon], 13);
            }
            await reverseGeocode(lat, lon);
            hideLoading();
            showToast('📍 ¡Ubicación GPS detectada correctamente!', 'success');
        },
        (error) => {
            hideLoading();
            showToast('No se pudo obtener la ubicación GPS (permiso denegado).', 'warning');
        },
        { timeout: 10000, enableHighAccuracy: true }
    );
}

/**
 * Selecciona una zona agrícola predefinida
 */
function setPredefinedRegion(regionKey) {
    const presets = {
        losangeles: { lat: -37.47, lon: -72.35, name: 'Los Ángeles (Provincia de Biobío, Chile)', soil: 'franco', size: 65 },
        mulchen: { lat: -37.72, lon: -72.24, name: 'Mulchén (Provincia de Biobío, Chile)', soil: 'franco-arcilloso', size: 90 },
        cabrero: { lat: -37.03, lon: -72.40, name: 'Cabrero / Arenales (Biobío, Chile)', soil: 'arenoso', size: 110 },
        santabarbara: { lat: -37.67, lon: -72.02, name: 'Santa Bárbara (Biobío Precordillera, Chile)', soil: 'franco', size: 50 },
        pergamino: { lat: -33.89, lon: -60.57, name: 'Pergamino (Pampa Húmeda)', soil: 'franco', size: 200 }
    };

    const target = presets[regionKey];
    if (!target) return;

    state.location = { lat: target.lat, lon: target.lon, name: target.name };
    state.soilType = target.soil;
    state.farmSize = target.size;

    const soilSelect = document.getElementById('soil-type');
    if (soilSelect) soilSelect.value = target.soil;

    const sizeInput = document.getElementById('farm-size');
    if (sizeInput) sizeInput.value = target.size;

    updateMapMarker(target.lat, target.lon);
    if (map) {
        map.setView([target.lat, target.lon], 11);
    }

    const locText = document.getElementById('selected-location');
    if (locText) locText.textContent = target.name;

    showToast(`Zona cargada: ${target.name}`, 'success');
}
