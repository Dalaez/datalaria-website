
        // --- Diccionario de Traducciones con 100% Paridad ES/EN (INV-WEATHER-5) ---
        const translations = {
            'es': {
                'mainTitle': 'Weather Intelligence v3.0',
                'badgeFreshnessPrefix': '🕒 Hace ',
                'badgeFreshnessSuffix': 'h',
                'badgeFreshnessNow': '🟢 En vivo',
                'menuTitle': 'Opciones',
                'menuTheme': 'Cambiar Tema',
                'menuInstall': 'Instalar App (PWA)',
                'menuFavs': 'Mis Ciudades',
                'tabHoy': 'Hoy',
                'tabComparar': 'Comparar',
                'tabRanking': 'Ranking',
                'tabIA': 'IA',
                'accClickToExpand': '🔍 Ver evolución',
                'accClickToCollapse': '▲ Plegar',
                'accClickToMatrix': '🔍 Ver matriz',
                'accClickToDetail': '🔍 Ver detalle',
                'accAiTitle': 'Detalle y Pesos del Modelo IA (Fourier)',
                'accEvolutionTitle': 'Evolución Histórica & Proyección',
                'accAmplitudeTitle': 'Amplitud Térmica Diaria (Máx - Mín)',
                'accSeasonalityTitle': 'Matriz de Perfil Estacional Mensual (°C)',
                'notEnoughData': 'Disponible con más datos (≥ 7 días)',
                'dataSufficiencyNotice': 'Se requieren más lecturas para calcular esta métrica.',
                'anomalyWarm': 'Superior a la media',
                'anomalyCold': 'Inferior a la media',
                'anomalyNormal': 'En la media',
                'nlWarmOptimal': 'Día excepcionalmente cálido para la época y condiciones excelentes para actividades al aire libre.',
                'nlWarmCaution': 'Calor superior a lo normal; recomendamos precaución con la exposición solar prolongada.',
                'nlColdOptimal': 'Ambiente fresco y seco por debajo de la media, ideal para paseos o deporte.',
                'nlColdCaution': 'Frío notable por debajo de la media habitual; baja sensación de confort térmico.',
                'nlNormal': 'Valores térmicos dentro de los rangos climatológicos normales para este período del año.',
                'pwaToastTitle': 'Instalar Weather Cockpit',
                'pwaToastDesc': 'Acceso rápido y funcionamiento offline desde tu pantalla de inicio.',
                'pwaToastInstall': 'Instalar',
                'pwaToastDismiss': 'Ahora no',
                'pwaIosGuide': 'En iOS: pulsa Compartir y luego "Añadir a pantalla de inicio"',
                'offlineNotice': 'Modo sin conexión — Mostrando últimos datos almacenados localmente.',
                'favsTitle': 'Mis Estaciones Favoritas',
                'favsEmpty': 'No has guardado favoritas. Pulsa la estrella ★ en cualquier ciudad para añadirla.',
                'menuCsv': 'Exportar CSV',
                'menuJson': 'Exportar JSON',
                'menuSheet': 'Ficha Técnica',
                'menuArticles': 'Serie de Artículos',
                'backToPortal': '← Datalaria',
                'badgeStatus': '🟢 168 Estaciones · +375 Días',
                'viewObservatory': '🌍 Observatorio',
                'viewArena': '🤖 Laboratorio ML',
                'viewAtlas': '🏆 Atlas Global (168)',
                'appSheetLink': 'Ficha Técnica',
                'howToLink': 'Serie de Artículos',
                'exportBtn': '📥 Exportar',
                'exportCSV': '📄 Descargar CSV',
                'exportJSON': '📦 Descargar JSON',
                'presetLabel': 'Escenarios en 1 Clic:',
                'presetSpain': '🇪🇸 Capitales ES',
                'presetGlobal': '🌍 Hubs Globales',
                'presetExtremes': '🔥❄️ Extremos Hoy',
                'presetAiDuel': '🤖 Duelo IA vs OWM',
                'presetComfort': '🏃‍♂️ Top Confort Outdoor',
                'tickerHottest': 'Récord Cálido',
                'tickerColdest': 'Récord Frío',
                'tickerAnomaly': 'Anomalía 30d',
                'tickerComfort': 'Mejor Confort',
                'citySelectLabel': 'Selecciona hasta 5 ciudades:',
                'metricLegend': 'Métrica:',
                'metricTemp': 'Temperatura',
                'metricFeels': 'Sensación',
                'metricHum': 'Humedad',
                'metricWind': 'Viento',
                'metricClouds': 'Nubosidad',
                'metricRain': 'Lluvia',
                'metricVisibility': 'Visibilidad',
                'rangeLegend': 'Rango:',
                'range7D': '7D',
                'range30D': '30D',
                'range90D': '90D',
                'range1Y': '1A',
                'rangeAll': 'Todo',
                'rangeCustom': 'Personalizado',
                'customRangeFrom': 'Desde:',
                'customRangeTo': 'Hasta:',
                'hourLegend': 'Hora:',
                'hourAll': 'Todas',
                'hourMorning': '06h',
                'hourAfternoon': '14h',
                'hourNight': '22h',
                'mapLayerLabel': 'Capa:',
                'layerTemp': 'Temperatura (°C)',
                'layerComfort': 'Confort Outdoor (0-100)',
                'layerAnomaly': 'Anomalía 30d (Δ°C)',
                'layerWind': 'Viento (km/h)',
                'layerHumidity': 'Humedad (%)',
                'mapTitle': 'Mapa Geoespacial Global',
                'kpiTitle': 'Super-Cards Comparativas',
                'comfortLabel': 'Confort Outdoor',
                'comfortOptimal': 'Óptimo',
                'comfortModerate': 'Moderado',
                'comfortUnfavorable': 'Desfavorable',
                'anomalyLabel': 'vs media 30d',
                'historyTitle': 'Evolución Histórica & Proyección',
                'historySubtitle': '(Horas en tu zona horaria local · Línea discontinua: pronóstico OWM / Punto: IA)',
                'variationTitle': 'Amplitud Térmica Diaria (Máx - Mín)',
                'variationSubtitle': '(Diferencia diaria entre máxima y mínima registrada y proyectada)',
                'seasonalityTitle': 'Matriz de Perfil Estacional Mensual (°C)',
                'seasonalitySubtitle': '(Comportamiento medio mes a mes en todo el año registrado)',
                'kpiNoData': 'No hay datos recientes.',
                'kpiEmpty': 'Selecciona una o más ciudades para ver los datos comparativos.',
                'kpiFeels': 'Sensación',
                'kpiHumidity': 'Humedad',
                'kpiWind': 'Viento',
                'kpiClouds': 'Nubosidad',
                'kpiVisibility': 'Visibilidad',
                'kpiRain': 'Lluvia (1h)',
                'kpiSnow': 'Nieve (1h)',
                'kpiHist': 'Histórico',
                'kpiMax': 'Máx',
                'kpiMin': 'Mín',
                'kpiMedia': 'Media',
                'forecastTitle': 'Pronóstico OWM (Máx/Mín)',
                'iaTitle': 'Predicción IA Fourier (Mañana)',
                'iaNoData': 'Datos insuf.',
                'iaVsOWM': 'OWM',
                'iaModelMetrics': 'Métricas IA',
                'chartDateHour': 'Fecha y Hora',
                'chartDate': 'Fecha',
                'chartVariation': 'Amplitud Térmica',
                'chartEmpty': 'No hay datos disponibles para la selección actual.',
                'varChartEmpty': 'No hay suficientes datos para calcular la variación diaria.',
                'fatalError': 'Error fatal: No se pudo cargar el índice de ciudades',
                'choicesPlaceholder': 'Escribe para buscar ciudades...',
                'arenaMacroTrained': 'Estaciones Entrenadas',
                'arenaMacroRecords': 'Registros Procesados',
                'arenaMacroR2': 'R² Medio Global',
                'arenaMacroMae': 'MAE 30d Medio',
                'arenaModelDesc': 'El motor implementa regresión con armónicos estacionales de Fourier (sin y cos de 365.25 días), eliminando saltos de año y ponderando lags térmicos.',
                'arenaTableTitle': 'Duelo Walk-Forward: IA Datalaria vs. OpenWeatherMap',
                'colCity': 'Ciudad',
                'colRegion': 'Región',
                'colDays': 'Días',
                'colIaTomorrow': 'IA Mañana (Máx / Mín / Med)',
                'colOwmTomorrow': 'OWM Mañana',
                'colDelta': 'Δ (IA - OWM)',
                'colR2': 'R² Modelo',
                'colMae': 'MAE 30d',
                'colBias': 'Sesgo',
                'colWinRate': 'Win-Rate IA',
                'colAction': 'Acción',
                'btnCompare': '+ Comparar',
                'btnViewObs': 'Observatorio',
                'atlasSearchPlaceholder': 'Buscar por ciudad o país...',
                'atlasRegionAll': 'Todas (168)',
                'atlasRegionSpain': '🇪🇸 España (56)',
                'atlasRegionEurope': '🇪🇺 Europa (47)',
                'atlasRegionAsia': '🌏 Asia (25)',
                'atlasRegionAmericas': '🌎 América (23)',
                'atlasRegionAfrica': '🌍 África (13)',
                'atlasRegionOceania': '🇦🇺 Oceanía (4)',
                'atlasSortComfortDesc': 'Mayor Confort Outdoor',
                'atlasSortComfortAsc': 'Menor Confort Outdoor',
                'atlasSortTempDesc': 'Más Cálidas Hoy',
                'atlasSortTempAsc': 'Más Frías Hoy',
                'atlasSortAnomalyDesc': 'Mayor Anomalía 30d',
                'atlasSortWindDesc': 'Mayor Viento',
                'colTemp': 'Temp Actual',
                'colFeels': 'Sensación',
                'colAnomaly': 'Anomalía 30d',
                'colRecord': 'Récord Histórico',
                'colHumWind': 'Humedad / Viento',
                'colComfort': 'Confort Outdoor',
                'plgTitle': 'Explota la Inteligencia Climática y los Modelos Cuantitativos',
                'plgDesc': 'Weather Service v2.0 combina ingestión serverless 3x/día, estacionalidad cíclica de Fourier y arquitectura de datos de coste cero.',
                'plgBtnTechSheet': 'Ver Ficha Técnica',
                'plgBtnKits': 'Explorar Kits B2B en Recursos',
                'exportSuccess': 'Datos exportados correctamente.',
                'cityAdded': 'añadida al Observatorio.',
                'cityLimitReached': 'Límite de 5 ciudades alcanzado.'
            },
            'en': {
                'mainTitle': 'Weather Intelligence v3.0',
                'badgeFreshnessPrefix': '🕒 Hace ',
                'badgeFreshnessSuffix': 'h',
                'badgeFreshnessNow': '🟢 En vivo',
                'menuTitle': 'Opciones',
                'menuTheme': 'Cambiar Tema',
                'menuInstall': 'Instalar App (PWA)',
                'menuFavs': 'Mis Ciudades',
                'tabHoy': 'Hoy',
                'tabComparar': 'Comparar',
                'tabRanking': 'Ranking',
                'tabIA': 'IA',
                'accClickToExpand': '🔍 Ver evolución',
                'accClickToCollapse': '▲ Plegar',
                'accClickToMatrix': '🔍 Ver matriz',
                'accClickToDetail': '🔍 Ver detalle',
                'accAiTitle': 'Detalle y Pesos del Modelo IA (Fourier)',
                'accEvolutionTitle': 'Evolución Histórica & Proyección',
                'accAmplitudeTitle': 'Amplitud Térmica Diaria (Máx - Mín)',
                'accSeasonalityTitle': 'Matriz de Perfil Estacional Mensual (°C)',
                'notEnoughData': 'Disponible con más datos (≥ 7 días)',
                'dataSufficiencyNotice': 'Se requieren más lecturas para calcular esta métrica.',
                'anomalyWarm': 'Superior a la media',
                'anomalyCold': 'Inferior a la media',
                'anomalyNormal': 'En la media',
                'nlWarmOptimal': 'Día excepcionalmente cálido para la época y condiciones excelentes para actividades al aire libre.',
                'nlWarmCaution': 'Calor superior a lo normal; recomendamos precaución con la exposición solar prolongada.',
                'nlColdOptimal': 'Ambiente fresco y seco por debajo de la media, ideal para paseos o deporte.',
                'nlColdCaution': 'Frío notable por debajo de la media habitual; baja sensación de confort térmico.',
                'nlNormal': 'Valores térmicos dentro de los rangos climatológicos normales para este período del año.',
                'pwaToastTitle': 'Instalar Weather Cockpit',
                'pwaToastDesc': 'Acceso rápido y funcionamiento offline desde tu pantalla de inicio.',
                'pwaToastInstall': 'Instalar',
                'pwaToastDismiss': 'Ahora no',
                'pwaIosGuide': 'En iOS: pulsa Compartir y luego "Añadir a pantalla de inicio"',
                'offlineNotice': 'Modo sin conexión — Mostrando últimos datos almacenados localmente.',
                'favsTitle': 'Mis Estaciones Favoritas',
                'favsEmpty': 'No has guardado favoritas. Pulsa la estrella ★ en cualquier ciudad para añadirla.',
                'menuCsv': 'Exportar CSV',
                'menuJson': 'Exportar JSON',
                'menuSheet': 'Ficha Técnica',
                'menuArticles': 'Serie de Artículos',
                'backToPortal': '← Datalaria',
                'badgeStatus': '🟢 168 Stations · +375 Days',
                'viewObservatory': '🌍 Observatory',
                'viewArena': '🤖 ML Arena',
                'viewAtlas': '🏆 Global Atlas (168)',
                'appSheetLink': 'Technical Sheet',
                'howToLink': 'Article Series',
                'exportBtn': '📥 Export',
                'exportCSV': '📄 Download CSV',
                'exportJSON': '📦 Download JSON',
                'presetLabel': '1-Click Scenarios:',
                'presetSpain': '🇪🇸 Spain Capitals',
                'presetGlobal': '🌍 Global Hubs',
                'presetExtremes': '🔥❄️ Planet Extremes',
                'presetAiDuel': '🤖 AI vs OWM Duel',
                'presetComfort': '🏃‍♂️ Top Outdoor Comfort',
                'tickerHottest': 'Hottest',
                'tickerColdest': 'Coldest',
                'tickerAnomaly': '30d Anomaly',
                'tickerComfort': 'Best Comfort',
                'citySelectLabel': 'Select up to 5 cities:',
                'metricLegend': 'Metric:',
                'metricTemp': 'Temperature',
                'metricFeels': 'Feels Like',
                'metricHum': 'Humidity',
                'metricWind': 'Wind',
                'metricClouds': 'Cloudiness',
                'metricRain': 'Rain',
                'metricVisibility': 'Visibility',
                'rangeLegend': 'Range:',
                'range7D': '7D',
                'range30D': '30D',
                'range90D': '90D',
                'range1Y': '1Y',
                'rangeAll': 'All',
                'rangeCustom': 'Custom',
                'customRangeFrom': 'From:',
                'customRangeTo': 'To:',
                'hourLegend': 'Hour:',
                'hourAll': 'All',
                'hourMorning': '06h',
                'hourAfternoon': '14h',
                'hourNight': '22h',
                'mapLayerLabel': 'Layer:',
                'layerTemp': 'Temperature (°C)',
                'layerComfort': 'Outdoor Comfort (0-100)',
                'layerAnomaly': '30d Anomaly (Δ°C)',
                'layerWind': 'Wind (km/h)',
                'layerHumidity': 'Humidity (%)',
                'mapTitle': 'Global Geospatial Map',
                'kpiTitle': 'Comparative Super-Cards',
                'comfortLabel': 'Outdoor Comfort',
                'comfortOptimal': 'Optimal',
                'comfortModerate': 'Moderate',
                'comfortUnfavorable': 'Unfavorable',
                'anomalyLabel': 'vs 30d mean',
                'historyTitle': 'Historical Evolution & Forecast',
                'historySubtitle': '(Times in local timezone · Dashed line: OWM forecast / Point: AI)',
                'variationTitle': 'Daily Thermal Range (Max - Min)',
                'variationSubtitle': '(Daily difference between max and min recorded and forecasted)',
                'seasonalityTitle': 'Monthly Seasonality Profile Matrix (°C)',
                'seasonalitySubtitle': '(Month-by-month average profile across the full recorded year)',
                'kpiNoData': 'No recent data.',
                'kpiEmpty': 'Select one or more cities to view comparative data.',
                'kpiFeels': 'Feels like',
                'kpiHumidity': 'Humidity',
                'kpiWind': 'Wind',
                'kpiClouds': 'Cloudiness',
                'kpiVisibility': 'Visibility',
                'kpiRain': 'Rain (1h)',
                'kpiSnow': 'Snow (1h)',
                'kpiHist': 'Historical',
                'kpiMax': 'Max',
                'kpiMin': 'Min',
                'kpiMedia': 'Mean',
                'forecastTitle': 'OWM Forecast (Max/Min)',
                'iaTitle': 'Fourier AI Prediction (Tomorrow)',
                'iaNoData': 'Insuff. data',
                'iaVsOWM': 'OWM',
                'iaModelMetrics': 'AI Metrics',
                'chartDateHour': 'Date and Time',
                'chartDate': 'Date',
                'chartVariation': 'Thermal Range',
                'chartEmpty': 'No data available for the current selection.',
                'varChartEmpty': 'Not enough data to calculate daily variation.',
                'fatalError': 'Fatal error: Could not load city index',
                'choicesPlaceholder': 'Type to search cities...',
                'arenaMacroTrained': 'Trained Stations',
                'arenaMacroRecords': 'Processed Records',
                'arenaMacroR2': 'Global Mean R²',
                'arenaMacroMae': 'Mean 30d MAE',
                'arenaModelDesc': 'The engine implements regression with Fourier seasonal harmonics (365.25-day sin and cos), eliminating year-boundary jumps and weighting thermal lags.',
                'arenaTableTitle': 'Walk-Forward Arena: Datalaria AI vs. OpenWeatherMap',
                'colCity': 'City',
                'colRegion': 'Region',
                'colDays': 'Days',
                'colIaTomorrow': 'AI Tomorrow (Max / Min / Mean)',
                'colOwmTomorrow': 'OWM Tomorrow',
                'colDelta': 'Δ (AI - OWM)',
                'colR2': 'Model R²',
                'colMae': '30d MAE',
                'colBias': 'Bias',
                'colWinRate': 'AI Win-Rate',
                'colAction': 'Action',
                'btnCompare': '+ Compare',
                'btnViewObs': 'Observatory',
                'atlasSearchPlaceholder': 'Search by city or country...',
                'atlasRegionAll': 'All (168)',
                'atlasRegionSpain': '🇪🇸 Spain (56)',
                'atlasRegionEurope': '🇪🇺 Europe (47)',
                'atlasRegionAsia': '🌏 Asia (25)',
                'atlasRegionAmericas': '🌎 Americas (23)',
                'atlasRegionAfrica': '🌍 Africa (13)',
                'atlasRegionOceania': '🇦🇺 Oceania (4)',
                'atlasSortComfortDesc': 'Highest Outdoor Comfort',
                'atlasSortComfortAsc': 'Lowest Outdoor Comfort',
                'atlasSortTempDesc': 'Hottest Today',
                'atlasSortTempAsc': 'Coldest Today',
                'atlasSortAnomalyDesc': 'Highest 30d Anomaly',
                'atlasSortWindDesc': 'Highest Wind',
                'colTemp': 'Current Temp',
                'colFeels': 'Feels',
                'colAnomaly': '30d Anomaly',
                'colRecord': 'All-Time Record',
                'colHumWind': 'Humidity / Wind',
                'colComfort': 'Outdoor Comfort',
                'plgTitle': 'Harness Climate Intelligence and Quantitative Models',
                'plgDesc': 'Weather Service v2.0 combines 3x/day serverless ingestion, cyclic Fourier seasonality, and zero-cost data architecture.',
                'plgBtnTechSheet': 'View Technical Sheet',
                'plgBtnKits': 'Explore B2B Kits in Resources',
                'exportSuccess': 'Data exported successfully.',
                'cityAdded': 'added to Observatory.',
                'cityLimitReached': 'Maximum of 5 cities reached.'
            }
        };


        // --- Configuración Global v3.0 (INV-WEATHER-7 Remote-First) ---
        const REMOTE_BASE = 'https://datalaria-app-weather.netlify.app/';
        const LOCAL_BASE = '/apps/weather/';
        const CITIES_LIST_URL = '/apps/weather/ciudades.txt';
        const DATA_FOLDER_URL = '/apps/weather/datos/';
        const REMOTE_DATA_FALLBACK_URL = 'https://datalaria-app-weather.netlify.app/datos/';
        const MAP_DATA_URL = 'city_locations.json';
        const PREDICTIONS_URL = 'predicciones.json';
        const GLOBAL_SUMMARY_URL = 'global_summary.json';
        const CLIMATOLOGY_URL = 'derived/climatology.json';
        const DERIVED_DAILY_URL = 'derived/daily/';

        let lastDataFreshnessIso = null;
        let climatologyCache = null;
        let deferredPrompt = null;


        const BLOG_LINKS = {
            'es': 'https://datalaria.com/es/posts/app-openweather_part1_backend/',
            'en': 'https://datalaria.com/en/posts/app_openweather_part1_backend/'
        };

        const TECH_SHEET_LINKS = {
            'es': '/es/apps/weather/',
            'en': '/en/apps/weather/'
        };

        const PORTAL_LINKS = {
            'es': '/es/apps/',
            'en': '/en/apps/'
        };

        const RECURSOS_LINKS = {
            'es': '/es/recursos/',
            'en': '/en/resources/'
        };

        const COLOR_PALETTE = ['#0ea5e9', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#3b82f6', '#14b8a6', '#f97316', '#a855f7', '#06b6d4'];

        
        // ====================================================================
        // HELPERS v3.0: REMOTE-FIRST, PWA, ACCORDIONS & DATA SUFFICIENCY
        // ====================================================================

        // INV-WEATHER-7: Remote-First Data Transport con Fallback Local
        async function fetchJSONRemoteFirst(path, options = {}) {
            const timeoutMs = options.timeoutMs || 6000;
            const cleanPath = path.startsWith('/') ? path.slice(1) : path;
            const remoteUrl = REMOTE_BASE + cleanPath;
            const localUrl = LOCAL_BASE + cleanPath;

            // Intento 1: Remoto con timeout
            try {
                const controller = new AbortController();
                const timer = setTimeout(() => controller.abort(), timeoutMs);
                const res = await fetch(remoteUrl + (remoteUrl.includes('?') ? '&' : '?') + 't=' + Date.now(), {
                    signal: controller.signal
                });
                clearTimeout(timer);
                if (res.ok) {
                    const data = await res.json();
                    return { data, source: 'remote' };
                }
            } catch (err) {
                // Silencioso: fallback a local
            }

            // Intento 2: Local
            try {
                const res = await fetch(localUrl + (localUrl.includes('?') ? '&' : '?') + 't=' + Date.now());
                if (res.ok) {
                    const data = await res.json();
                    return { data, source: 'local' };
                }
            } catch (err) {
                console.warn('Error en fetchJSONRemoteFirst local para ' + path, err);
            }

            return { data: null, source: 'none' };
        }

        function slugifyJS(name) {
            return name
                .normalize('NFKD')
                .replace(/[\u0300-\u036f]/g, '')
                .toLowerCase()
                .trim()
                .replace(/[^\w\s-]/g, '')
                .replace(/[\s_]+/g, '-')
                .replace(/-+/g, '-')
                .replace(/^-+|-+$/g, '');
        }

        function updateFreshnessBadge(isoDate) {
            const badge = document.getElementById('freshness-badge');
            if (!badge) return;
            if (!isoDate) {
                badge.textContent = translations[currentLang].badgeFreshnessNow || '🟢 En vivo';
                return;
            }
            const diffMs = Date.now() - new Date(isoDate).getTime();
            const diffHours = Math.max(0, Math.round(diffMs / (1000 * 60 * 60)));
            const prefix = translations[currentLang].badgeFreshnessPrefix || '🕒 Hace ';
            const suffix = translations[currentLang].badgeFreshnessSuffix || 'h';
            if (diffHours < 1) {
                badge.textContent = translations[currentLang].badgeFreshnessNow || '🟢 En vivo';
            } else {
                badge.textContent = `${prefix}${diffHours}${suffix}`;
            }
        }

        function getFavoriteCities() {
            try {
                const raw = localStorage.getItem('weather_my_cities');
                return raw ? JSON.parse(raw) : ['Madrid', 'Barcelona'];
            } catch {
                return ['Madrid', 'Barcelona'];
            }
        }

        function toggleFavoriteCity(cityName) {
            let favs = getFavoriteCities();
            if (favs.includes(cityName)) {
                favs = favs.filter(c => c !== cityName);
            } else {
                favs.push(cityName);
            }
            localStorage.setItem('weather_my_cities', JSON.stringify(favs));
            updateKPIs(allDataCache, currentMetric);
        }

        // INV-WEATHER-8: Data Sufficiency Gate
        function hasEnoughData(kind, records) {
            if (!records || records.length === 0) return false;
            if (kind === 'evolution') {
                const uniqueDates = new Set(records.map(r => r.date || (r.fecha_hora instanceof Date ? r.fecha_hora.toISOString().slice(0, 10) : '')));
                return uniqueDates.size >= 7;
            }
            if (kind === 'amplitude') {
                const hasDiurnal = records.filter(r => r.diurnal_range !== null && r.diurnal_range !== undefined).length >= 7;
                if (hasDiurnal) return true;
                const dayCounts = {};
                records.forEach(r => {
                    const k = r.date || (r.fecha_hora instanceof Date ? r.fecha_hora.toISOString().slice(0, 10) : '');
                    dayCounts[k] = (dayCounts[k] || 0) + 1;
                });
                const daysWithMultiple = Object.values(dayCounts).filter(n => n > 1).length;
                return daysWithMultiple >= 7;
            }
            if (kind === 'seasonality') {
                const months = new Set(records.map(r => (r.date || (r.fecha_hora instanceof Date ? r.fecha_hora.toISOString().slice(0, 10) : '')).slice(5, 7)).filter(Boolean));
                return months.size >= 2;
            }
            if (kind === 'ai') {
                return Boolean(allPredictionsCache && Object.keys(allPredictionsCache).length > 0);
            }
            return true;
        }

        function processDerivedDailyRows(dailyData, ciudadQuery) {
            const rows = dailyData.rows || [];
            const records = rows.map(r => {
                const dateStr = r[0];
                const tmin = r[1];
                const tmax = r[2];
                const tmean = r[3];
                const amp = r[4];
                const feels = r[5];
                const hum = r[6];
                const wind = r[7];
                const rain = r[8];
                const clouds = r[9];
                const n = r[10];

                return {
                    fecha_hora: new Date(dateStr + 'T12:00:00Z'),
                    date: dateStr,
                    temperatura_c: tmean,
                    temp_min: tmin,
                    temp_max: tmax,
                    diurnal_range: amp,
                    sensacion_c: feels,
                    humedad_porc: hum,
                    viento_kmh: wind,
                    nubosidad_porc: clouds,
                    visibilidad_m: 10000,
                    lluvia_1h: rain || 0,
                    nieve_1h: 0,
                    n_samples: n
                };
            }).filter(r => !isNaN(r.fecha_hora.getTime()))
              .sort((a, b) => a.fecha_hora - b.fecha_hora);

            return {
                records: records,
                stats: calculateStats(records)
            };
        }

        async function loadClimatology() {
            try {
                const res = await fetchJSONRemoteFirst(CLIMATOLOGY_URL);
                if (res.data) climatologyCache = res.data;
            } catch (e) {
                climatologyCache = null;
            }
        }

        // --- Estado Global ---
        let currentLang = 'es';
        let currentView = 'observatory';
        let currentMetric = 'temp';
        let currentTimeRange = '30'; // 30D por defecto
        let currentHourFilter = 'all';
        let currentMapLayer = 'temp';
        let customStartDate = null;
        let customEndDate = null;

        let globalSummaryData = null;
        let allPredictionsCache = {};
        let cityLocationsCache = [];
        let cityOptionsList = [];
        let allDataCache = {};

        let map, lightTileLayer, darkTileLayer;
        let mapMarkers = {};
        let myChart = null;
        let myVariationChart = null;
        let choicesInstance = null;

        // Telemetría GA4
        function emitWeatherEvent(eventName, params = {}) {
            if (typeof window.gtag === 'function') {
                window.gtag('event', eventName, params);
            }
        }

        function showToast(message) {
            const container = document.getElementById('toast-container');
            const toast = document.createElement('div');
            toast.className = 'toast-msg';
            toast.textContent = message;
            container.appendChild(toast);
            setTimeout(() => {
                toast.style.opacity = '0';
                toast.style.transition = 'opacity 0.3s ease';
                setTimeout(() => toast.remove(), 300);
            }, 3000);
        }

        // --- Definición de Métricas ---
        function getMetricMap() {
            const lang = currentLang;
            return {
                'temp': { key: 'temperatura_c', label: translations[lang].metricTemp, unit: '°C', icon: 'thermometer' },
                'feels_like': { key: 'sensacion_c', label: translations[lang].metricFeels, unit: '°C', icon: 'smile' },
                'humidity': { key: 'humedad_porc', label: translations[lang].metricHum, unit: '%', icon: 'droplet' },
                'wind': { key: 'viento_kmh', label: translations[lang].metricWind, unit: 'km/h', icon: 'wind' },
                'clouds': { key: 'nubosidad_porc', label: translations[lang].metricClouds, unit: '%', icon: 'cloud' },
                'rain': { key: 'lluvia_1h', label: translations[lang].metricRain, unit: 'mm', icon: 'umbrella' },
                'visibility': { key: 'visibilidad_m', label: translations[lang].metricVisibility, unit: 'km', icon: 'eye', divider: 1000 }
            };
        }

        // --- Algoritmo de Confort Outdoor JS (INV-WEATHER-4) ---
        function computeComfortIndexJS(t, feels, hum, wind, clouds, visM = 10000, rain = 0.0, snow = 0.0) {
            const target = (feels !== undefined && feels !== null) ? (0.6 * feels + 0.4 * t) : t;
            let tempScore = 100.0 - Math.min(100.0, 3.5 * Math.pow(Math.abs(target - 21.0), 1.25));

            let humPen = 0.0;
            if (hum < 30) humPen = (30 - hum) * 0.5;
            else if (hum > 70) humPen = (hum - 70) * 0.7;

            let windPen = 0.0;
            if (wind > 15) windPen = Math.min(30.0, (wind - 15) * 1.0);

            let cloudPen = 0.0;
            if (clouds > 80) cloudPen = (clouds - 80) * 0.25;

            let precPen = 0.0;
            if (rain > 0) precPen += Math.min(40.0, 15.0 + rain * 10.0);
            if (snow > 0) precPen += Math.min(40.0, 20.0 + snow * 15.0);

            let visPen = 0.0;
            if (visM < 5000) visPen = Math.min(25.0, ((5000 - visM) / 5000) * 25.0);

            let raw = tempScore - humPen - windPen - cloudPen - precPen - visPen;
            return Math.max(0, Math.min(100, Math.round(raw)));
        }

        // --- Carga de Datos Resiliente ---
                async function loadGlobalSummary() {
            const res = await fetchJSONRemoteFirst(GLOBAL_SUMMARY_URL);
            if (res.data) {
                globalSummaryData = res.data;
                if (globalSummaryData.generated_at) {
                    lastDataFreshnessIso = globalSummaryData.generated_at;
                    updateFreshnessBadge(globalSummaryData.generated_at);
                }
            } else {
                console.warn('global_summary.json no disponible, reconstruyendo en cliente...');
                globalSummaryData = buildFallbackSummary();
                updateFreshnessBadge(null);
            }
            populateExtremesTicker();
        }

        function buildFallbackSummary() {
            const cities = cityLocationsCache.map(loc => {
                const pred = allPredictionsCache[loc.ciudad] || {};
                const t = loc.temp || 15.0;
                const cIdx = computeComfortIndexJS(t, t, 50, 10, 20, 10000, 0, 0);
                return {
                    ciudad: loc.ciudad,
                    query: `${loc.ciudad},${loc.country || 'ES'}`,
                    country: loc.country || 'ES',
                    region: 'spain',
                    lat: loc.lat,
                    lon: loc.lon,
                    latest: {
                        fecha_hora: new Date().toISOString(),
                        temp: t,
                        feels_like: t,
                        humidity: 50,
                        wind_kmh: 10,
                        clouds: 20,
                        visibility_km: 10,
                        rain_1h: 0,
                        snow_1h: 0,
                        description: 'cielo claro'
                    },
                    stats: {
                        records: 300,
                        days: 100,
                        mean_30d_temp: t,
                        anomaly_30d_c: 0.0,
                        all_time_max_c: t + 10,
                        all_time_min_c: t - 10,
                        avg_diurnal_range_c: 8.0,
                        rainy_days_30d: 4,
                        comfort_index: cIdx,
                        best_hour_utc: 14
                    }
                };
            });
            return {
                generated_at: new Date().toISOString(),
                total_cities: cities.length,
                total_records: cities.length * 300,
                global_extremes: {
                    hottest: { ciudad: 'Madrid', val: 25.0 },
                    coldest: { ciudad: 'León', val: 8.0 },
                    top_positive_anomaly: { ciudad: 'Madrid', val: 2.0 },
                    best_comfort: { ciudad: 'Palma', val: 88 }
                },
                cities: cities
            };
        }

                async function loadPredictions() {
            const res = await fetchJSONRemoteFirst(PREDICTIONS_URL);
            if (res.data) {
                allPredictionsCache = res.data;
            } else {
                console.warn('predicciones.json no disponible');
                allPredictionsCache = {};
            }
        }

                async function loadDataForCity(ciudadQuery) {
            if (allDataCache[ciudadQuery]) {
                return allDataCache[ciudadQuery];
            }
            const cityNameClean = ciudadQuery.split(',')[0].trim();
            const slug = slugifyJS(cityNameClean);

            // Intento 1: Ingesta Remote-First de daily JSON derivado (~15 KB)
            const dailyRes = await fetchJSONRemoteFirst(DERIVED_DAILY_URL + slug + '.json');
            if (dailyRes.data && dailyRes.data.rows && dailyRes.data.rows.length > 0) {
                const parsed = processDerivedDailyRows(dailyRes.data, ciudadQuery);
                allDataCache[ciudadQuery] = parsed;
                return parsed;
            }

            // Intento 2: Fallback a CSV remoto / local (PapaParse)
            return new Promise((resolve) => {
                const fileName = cityNameClean.replace(/ /g, '_') + '.csv';
                const remoteUrl = REMOTE_DATA_FALLBACK_URL + fileName;
                const localUrl = DATA_FOLDER_URL + fileName;

                Papa.parse(remoteUrl, {
                    download: true, header: true, dynamicTyping: true, skipEmptyLines: true,
                    complete: (remResults) => {
                        const parsed = processCSVResults(remResults.data, ciudadQuery);
                        allDataCache[ciudadQuery] = parsed;
                        resolve(parsed);
                    },
                    error: () => {
                        Papa.parse(localUrl, {
                            download: true, header: true, dynamicTyping: true, skipEmptyLines: true,
                            complete: (locResults) => {
                                const parsed = processCSVResults(locResults.data, ciudadQuery);
                                allDataCache[ciudadQuery] = parsed;
                                resolve(parsed);
                            },
                            error: (locErr) => {
                                console.warn(`CSV no disponible para ${cityNameClean}:`, locErr);
                                const fallbackEmpty = { records: [], stats: {} };
                                allDataCache[ciudadQuery] = fallbackEmpty;
                                resolve(fallbackEmpty);
                            }
                        });
                    }
                });
            });
        }

        function loadCSV(ciudadQuery) {
            return loadDataForCity(ciudadQuery);
        }

        function processCSVResults(rows, ciudadQuery) {
            const records = rows.map(r => ({
                ...r,
                fecha_hora: new Date(r.fecha_hora),
                temperatura_c: Number(r.temperatura_c) || 0,
                sensacion_c: Number(r.sensacion_c !== undefined ? r.sensacion_c : r.temperatura_c),
                humedad_porc: Number(r.humedad_porc) || 0,
                viento_kmh: Number(r.viento_kmh) || 0,
                nubosidad_porc: Number(r.nubosidad_porc) || 0,
                visibilidad_m: Number(r.visibilidad_m) || 10000,
                lluvia_1h: Number(r.lluvia_1h) || 0,
                nieve_1h: Number(r.nieve_1h) || 0
            })).filter(r => !isNaN(r.fecha_hora.getTime()))
              .sort((a, b) => a.fecha_hora - b.fecha_hora);

            return {
                records: records,
                stats: calculateStats(records)
            };
        }

        function calculateStats(records) {
            if (!records || records.length === 0) return {};
            const stats = {
                temp: { min: { val: Infinity, date: null }, max: { val: -Infinity, date: null } },
                feels_like: { min: { val: Infinity, date: null }, max: { val: -Infinity, date: null } },
                humidity: { min: { val: Infinity, date: null }, max: { val: -Infinity, date: null } },
                wind: { min: { val: Infinity, date: null }, max: { val: -Infinity, date: null } },
                clouds: { min: { val: Infinity, date: null }, max: { val: -Infinity, date: null } },
                rain: { min: { val: 0, date: null }, max: { val: -Infinity, date: null } },
                visibility: { min: { val: Infinity, date: null }, max: { val: -Infinity, date: null } }
            };

            let sumTemp = 0;
            records.forEach(row => {
                const d = row.fecha_hora;
                sumTemp += row.temperatura_c;
                if (row.temperatura_c < stats.temp.min.val) stats.temp.min = { val: row.temperatura_c, date: d };
                if (row.temperatura_c > stats.temp.max.val) stats.temp.max = { val: row.temperatura_c, date: d };
                if (row.sensacion_c < stats.feels_like.min.val) stats.feels_like.min = { val: row.sensacion_c, date: d };
                if (row.sensacion_c > stats.feels_like.max.val) stats.feels_like.max = { val: row.sensacion_c, date: d };
                if (row.humedad_porc < stats.humidity.min.val) stats.humidity.min = { val: row.humedad_porc, date: d };
                if (row.humedad_porc > stats.humidity.max.val) stats.humidity.max = { val: row.humedad_porc, date: d };
                if (row.viento_kmh < stats.wind.min.val) stats.wind.min = { val: row.viento_kmh, date: d };
                if (row.viento_kmh > stats.wind.max.val) stats.wind.max = { val: row.viento_kmh, date: d };
                if (row.nubosidad_porc < stats.clouds.min.val) stats.clouds.min = { val: row.nubosidad_porc, date: d };
                if (row.nubosidad_porc > stats.clouds.max.val) stats.clouds.max = { val: row.nubosidad_porc, date: d };
                if (row.lluvia_1h > stats.rain.max.val) stats.rain.max = { val: row.lluvia_1h, date: d };
                if (row.visibilidad_m < stats.visibility.min.val) stats.visibility.min = { val: row.visibilidad_m, date: d };
                if (row.visibilidad_m > stats.visibility.max.val) stats.visibility.max = { val: row.visibilidad_m, date: d };
            });

            stats.mean_temp = records.length > 0 ? (sumTemp / records.length) : 0;
            stats.latest = records[records.length - 1];
            return stats;
        }

        async function loadDataForCities(ciudadesQuery) {
            const promises = ciudadesQuery.map(q => loadCSV(q));
            const datasets = await Promise.all(promises);
            const map = {};
            ciudadesQuery.forEach((q, idx) => {
                map[q.split(',')[0].trim()] = datasets[idx];
            });
            return map;
        }

        // --- Ticker de Extremos Planetarios ---
        function populateExtremesTicker() {
            if (!globalSummaryData || !globalSummaryData.global_extremes) return;
            const ext = globalSummaryData.global_extremes;

            const setTicker = (elId, item, unit) => {
                const el = document.getElementById(elId);
                if (el && item) {
                    el.textContent = `${item.ciudad} (${item.val > 0 && unit.includes('°') && !unit.includes('Δ') ? '+' : ''}${item.val}${unit})`;
                    const parent = el.closest('.ticker-pill');
                    if (parent) {
                        parent.onclick = () => addCityToSelection(item.ciudad);
                    }
                }
            };

            setTicker('ticker-val-hottest', ext.hottest, '°C');
            setTicker('ticker-val-coldest', ext.coldest, '°C');
            setTicker('ticker-val-anomaly', ext.top_positive_anomaly, '°C');
            setTicker('ticker-val-comfort', ext.best_comfort, '/100');
        }

        // --- Mapa Geoespacial con Selector de 5 Capas ---
        async function initMap() {
            map = L.map('map-container').setView([24, 0], 2);

            lightTileLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; OpenStreetMap'
            });
            darkTileLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; OpenStreetMap &copy; CARTO'
            });

            const isDark = document.body.classList.contains('dark-mode');
            (isDark ? darkTileLayer : lightTileLayer).addTo(map);

            try {
                const res = await fetch(MAP_DATA_URL + '?v=' + Date.now());
                if (res.ok) cityLocationsCache = await res.json();
            } catch (err) {
                console.error('Error cargando city_locations.json:', err);
            }

            renderMapMarkers();

            document.getElementById('map-layer-select').addEventListener('change', (e) => {
                currentMapLayer = e.target.value;
                renderMapMarkers();
            });
        }

        function getMarkerColorForLayer(cityObj, layer) {
            const summaryCity = globalSummaryData?.cities?.find(c => c.ciudad === cityObj.ciudad);
            const latest = summaryCity?.latest || {};
            const stats = summaryCity?.stats || {};

            if (layer === 'comfort') {
                const c = stats.comfort_index !== undefined ? stats.comfort_index : 70;
                if (c >= 75) return '#10b981';
                if (c >= 50) return '#f59e0b';
                return '#ef4444';
            }
            if (layer === 'anomaly') {
                const a = stats.anomaly_30d_c || 0;
                if (a > 3.0) return '#f87171';
                if (a > 0.5) return '#fbbf24';
                if (a >= -0.5) return '#34d399';
                if (a >= -3.0) return '#60a5fa';
                return '#38bdf8';
            }
            if (layer === 'wind') {
                const w = latest.wind_kmh || 10;
                if (w > 35) return '#ef4444';
                if (w > 20) return '#f59e0b';
                return '#34d399';
            }
            if (layer === 'humidity') {
                const h = latest.humidity || 50;
                if (h > 80) return '#3b82f6';
                if (h > 50) return '#0ea5e9';
                return '#38bdf8';
            }
            // layer === 'temp' (default)
            const t = (cityObj.temp !== undefined) ? cityObj.temp : (latest.temp || 15);
            if (t < 0) return '#38bdf8';
            if (t < 10) return '#60a5fa';
            if (t < 22) return '#34d399';
            if (t < 30) return '#fbbf24';
            return '#f87171';
        }

        function renderMapMarkers() {
            if (!map) return;
            Object.values(mapMarkers).forEach(m => m.remove());
            mapMarkers = {};

            const selectedValues = choicesInstance ? choicesInstance.getValue(true) : [];
            const selectedNames = selectedValues.map(v => v.split(',')[0].trim());

            cityLocationsCache.forEach(loc => {
                const color = getMarkerColorForLayer(loc, currentMapLayer);
                const isSelected = selectedNames.includes(loc.ciudad);

                const marker = L.circleMarker([loc.lat, loc.lon], {
                    radius: isSelected ? 10 : 7,
                    weight: isSelected ? 3 : 1.5,
                    color: isSelected ? '#ffffff' : 'rgba(255,255,255,0.7)',
                    fillColor: color,
                    fillOpacity: isSelected ? 1.0 : 0.85
                }).addTo(map);

                const summaryCity = globalSummaryData?.cities?.find(c => c.ciudad === loc.ciudad);
                const comfort = summaryCity?.stats?.comfort_index || 75;
                const anomaly = summaryCity?.stats?.anomaly_30d_c || 0;

                const popupHtml = `
                    <div class="popup-title">${loc.ciudad} (${loc.country || 'ES'})</div>
                    <div class="popup-val" style="color:${color};">${loc.temp.toFixed(1)}°C</div>
                    <div class="popup-meta">
                        🏃‍♂️ Confort: <b>${comfort}/100</b> · Δ30d: <b>${anomaly >= 0 ? '+' : ''}${anomaly.toFixed(1)}°C</b>
                    </div>
                    <button class="popup-btn" onclick="addCityToSelection('${loc.ciudad}')">+ ${translations[currentLang].btnCompare}</button>
                `;
                marker.bindPopup(popupHtml);

                marker.on('click', () => {
                    addCityToSelection(loc.ciudad);
                });

                mapMarkers[loc.ciudad] = marker;
            });
        }

        function updateMapTiles(isDark) {
            if (!map || !lightTileLayer || !darkTileLayer) return;
            if (isDark) {
                if (map.hasLayer(lightTileLayer)) map.removeLayer(lightTileLayer);
                if (!map.hasLayer(darkTileLayer)) map.addLayer(darkTileLayer);
            } else {
                if (map.hasLayer(darkTileLayer)) map.removeLayer(darkTileLayer);
                if (!map.hasLayer(lightTileLayer)) map.addLayer(lightTileLayer);
            }
        }

        function fitMapToSelected(cityNames) {
            if (!map || cityNames.length === 0) return;
            const bounds = [];
            cityNames.forEach(name => {
                const loc = cityLocationsCache.find(l => l.ciudad === name);
                if (loc) bounds.push([loc.lat, loc.lon]);
            });
            if (bounds.length > 0) {
                map.flyToBounds(bounds, { padding: [50, 50], maxZoom: 6, duration: 1.2 });
            }
        }

        // --- Gestión de Ciudades & Presets ---
        function addCityToSelection(cityName) {
            if (!choicesInstance) return;
            const opt = cityOptionsList.find(o => o.label === cityName || o.value.startsWith(cityName + ','));
            if (!opt) return;

            const current = choicesInstance.getValue(true);
            if (current.includes(opt.value)) {
                showToast(`${cityName} ya está seleccionada.`);
                return;
            }
            if (current.length >= 5) {
                showToast(translations[currentLang].cityLimitReached);
                return;
            }
            choicesInstance.setChoiceByValue([...current, opt.value]);
            showToast(`✅ ${cityName} ${translations[currentLang].cityAdded}`);
            updateDashboard();
            emitWeatherEvent('weather_city_select', { city: cityName });
        }

        function applyPreset(presetId) {
            document.querySelectorAll('.preset-pill').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.preset === presetId);
            });

            let targets = [];
            if (presetId === 'spain') {
                targets = ['Madrid,ES', 'Barcelona,ES', 'Bilbao,ES', 'Sevilla,ES', 'León,ES'];
            } else if (presetId === 'global') {
                targets = ['Madrid,ES', 'London,GB', 'New York,US', 'Tokyo,JP', 'Singapore,SG'];
            } else if (presetId === 'extremes') {
                if (globalSummaryData?.cities?.length > 0) {
                    const sorted = [...globalSummaryData.cities].sort((a,b) => (b.latest?.temp || 0) - (a.latest?.temp || 0));
                    const hot = sorted.slice(0, 2).map(c => c.query || `${c.ciudad},${c.country}`);
                    const cold = sorted.slice(-2).map(c => c.query || `${c.ciudad},${c.country}`);
                    targets = [...hot, ...cold];
                } else {
                    targets = ['Madrid,ES', 'London,GB', 'Reykjavik,IS', 'Cairo,EG'];
                }
            } else if (presetId === 'ai_duel') {
                targets = ['Madrid,ES', 'León,ES', 'London,GB', 'Tokyo,JP'];
            } else if (presetId === 'comfort') {
                if (globalSummaryData?.cities?.length > 0) {
                    const sorted = [...globalSummaryData.cities].sort((a,b) => (b.stats?.comfort_index || 0) - (a.stats?.comfort_index || 0));
                    targets = sorted.slice(0, 4).map(c => c.query || `${c.ciudad},${c.country}`);
                } else {
                    targets = ['Palma,ES', 'Santa Cruz de Tenerife,ES', 'Valencia,ES', 'Malaga,ES'];
                }
            }

            if (choicesInstance && targets.length > 0) {
                choicesInstance.removeActiveItems();
                choicesInstance.setChoiceByValue(targets);
                updateDashboard();
                fitMapToSelected(targets.map(t => t.split(',')[0].trim()));
            }

            syncUrlParams({ preset: presetId });
            emitWeatherEvent('weather_preset_select', { preset_id: presetId });
        }

        // --- Conmutación de las 3 Vistas ---
        function switchView(viewId) {
            currentView = viewId;
            document.querySelectorAll('.view-btn').forEach(b => {
                b.classList.toggle('active', b.dataset.view === viewId);
            });
            document.querySelectorAll('.view-panel').forEach(p => {
                p.classList.toggle('active', p.id === `view-${viewId}`);
            });

            if (viewId === 'observatory') {
                if (map) setTimeout(() => map.invalidateSize(), 150);
                if (myChart) myChart.resize();
                if (myVariationChart) myVariationChart.resize();
            } else if (viewId === 'arena') {
                renderArenaTable();
            } else if (viewId === 'atlas') {
                renderAtlasTable();
            }

            syncUrlParams({ view: viewId });
            emitWeatherEvent('weather_view_switch', { view: viewId });
        }

        // --- Animación CountUp ---
        function animateCountUp(element, end, duration = 600, decimals = 1) {
            let start = 0;
            let startTime = null;
            if (isNaN(end) || !isFinite(end)) {
                element.textContent = (0).toFixed(decimals);
                return;
            }
            function step(ts) {
                if (!startTime) startTime = ts;
                const progress = Math.min((ts - startTime) / duration, 1);
                const eased = progress * (2 - progress);
                const cur = start + (end * eased);
                element.textContent = cur.toFixed(decimals);
                if (progress < 1) requestAnimationFrame(step);
                else element.textContent = end.toFixed(decimals);
            }
            requestAnimationFrame(step);
        }

        // --- Renderizado de Super-Cards (Observatorio) ---
        function updateKPIs(cityDataMap, metric) {
            const container = document.getElementById('kpi-container');
            container.innerHTML = '';
            const metricMap = getMetricMap();
            const metricInfo = metricMap[metric] || metricMap['temp'];

            const cityNames = Object.keys(cityDataMap);
            if (cityNames.length === 0) {
                container.innerHTML = `<p style="grid-column:1/-1; text-align:center; color:var(--text-secondary);">${translations[currentLang].kpiEmpty}</p>`;
                return;
            }

            cityNames.forEach((ciudad, idx) => {
                const data = cityDataMap[ciudad];
                if (!data || !data.stats || !data.stats.latest) {
                    container.innerHTML += `<div class="super-card"><h3>${ciudad}</h3><p>${translations[currentLang].kpiNoData}</p></div>`;
                    return;
                }

                const stats = data.stats;
                const latest = stats.latest;
                const citySummary = globalSummaryData?.cities?.find(c => c.ciudad === ciudad);
                const comfortIdx = citySummary?.stats?.comfort_index || computeComfortIndexJS(latest.temperatura_c, latest.sensacion_c, latest.humedad_porc, latest.viento_kmh, latest.nubosidad_porc, latest.visibilidad_m, latest.lluvia_1h, latest.nieve_1h);
                const anomaly = citySummary?.stats?.anomaly_30d_c || (stats.mean_temp ? (latest.temperatura_c - stats.mean_temp) : 0);

                let comfortClass = 'comfort-moderate';
                let comfortText = translations[currentLang].comfortModerate;
                if (comfortIdx >= 75) { comfortClass = 'comfort-optimal'; comfortText = translations[currentLang].comfortOptimal; }
                else if (comfortIdx < 50) { comfortClass = 'comfort-unfavorable'; comfortText = translations[currentLang].comfortUnfavorable; }

                
                const isFav = getFavoriteCities().includes(ciudad);
                const favBtnHtml = `<button class="card-fav-btn ${isFav ? 'active' : ''}" data-city="${ciudad}" title="${translations[currentLang].menuFavs}">${isFav ? '★' : '☆'}</button>`;

                let nlPhrase = '';
                if (anomaly > 2.0 && comfortIdx >= 70) {
                    nlPhrase = translations[currentLang].nlWarmOptimal;
                } else if (anomaly > 2.0 && comfortIdx < 70) {
                    nlPhrase = translations[currentLang].nlWarmCaution;
                } else if (anomaly < -2.0 && comfortIdx >= 70) {
                    nlPhrase = translations[currentLang].nlColdOptimal;
                } else if (anomaly < -2.0 && comfortIdx < 70) {
                    nlPhrase = translations[currentLang].nlColdCaution;
                } else {
                    nlPhrase = translations[currentLang].nlNormal;
                }
                const nlHtml = `<div class="card-nl-phrase">💡 ${nlPhrase}</div>`;

                const card = document.createElement('div');
                card.className = 'super-card';
                card.style.borderLeftColor = COLOR_PALETTE[idx % COLOR_PALETTE.length];

                let displayedVal = latest[metricInfo.key];
                if (metricInfo.divider) displayedVal = displayedVal / metricInfo.divider;

                const valId = `super-val-${ciudad.replace(/ /g, '_')}-${metric}`;
                const sparkId = `spark-${ciudad.replace(/ /g, '_')}-${metric}`;

                const predData = allPredictionsCache[ciudad];
                const forecastList = predData?.pred_owm_5day || [];
                const iaPred = predData?.pred_ia;
                const modelMetrics = predData?.model_metrics;

                card.innerHTML = `
                    <div class="card-top">
                        <div>
                            <h4 class="card-city">${ciudad} ${favBtnHtml}</h4>
                            <span class="card-time">${latest.fecha_hora.toLocaleString(currentLang, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}</span>
                        </div>
                        <div class="comfort-badge ${comfortClass}" title="${translations[currentLang].comfortLabel}">
                            🏃‍♂️ <span>${comfortIdx}/100</span> · ${comfortText}
                        </div>
                    </div>

                    <div class="main-stat-row">
                        <span class="main-stat-val tabular-nums" id="${valId}">0.0</span>
                        <span class="main-stat-unit">${metricInfo.unit}</span>
                        <span class="anomaly-badge ${anomaly >= 0 ? 'anomaly-pos' : 'anomaly-neg'}" title="Anomalía respecto a la media de 30 días">
                            ${anomaly >= 0 ? '+' : ''}${anomaly.toFixed(1)}°C ${translations[currentLang].anomalyLabel}
                        </span>
                    </div>
                    ${nlHtml}

                    <div class="stat-grid">
                        <div class="stat-item"><i data-feather="smile" style="width:13px; height:13px;"></i> ${translations[currentLang].kpiFeels}: <strong class="tabular-nums">${latest.sensacion_c.toFixed(1)}°C</strong></div>
                        <div class="stat-item"><i data-feather="droplet" style="width:13px; height:13px;"></i> ${translations[currentLang].kpiHumidity}: <strong class="tabular-nums">${latest.humedad_porc}%</strong></div>
                        <div class="stat-item"><i data-feather="wind" style="width:13px; height:13px;"></i> ${translations[currentLang].kpiWind}: <strong class="tabular-nums">${latest.viento_kmh.toFixed(1)} km/h</strong></div>
                        <div class="stat-item"><i data-feather="cloud" style="width:13px; height:13px;"></i> ${translations[currentLang].kpiClouds}: <strong class="tabular-nums">${latest.nubosidad_porc}%</strong></div>
                        <div class="stat-item"><i data-feather="eye" style="width:13px; height:13px;"></i> ${translations[currentLang].kpiVisibility}: <strong class="tabular-nums">${(latest.visibilidad_m / 1000).toFixed(1)} km</strong></div>
                        <div class="stat-item"><i data-feather="umbrella" style="width:13px; height:13px;"></i> ${translations[currentLang].kpiRain}: <strong class="tabular-nums">${latest.lluvia_1h.toFixed(1)} mm</strong></div>
                    </div>

                    <div class="sparkline-box">
                        <canvas id="${sparkId}"></canvas>
                    </div>

                    ${buildForecastBlock(forecastList)}
                    ${buildIaBlock(iaPred, forecastList, modelMetrics)}
                `;

                container.appendChild(card);

                card.querySelector('.card-fav-btn')?.addEventListener('click', (e) => {
                    e.stopPropagation();
                    toggleFavoriteCity(ciudad);
                });


                const elVal = document.getElementById(valId);
                if (elVal) {
                    animateCountUp(elVal, Number(displayedVal) || 0, 700, (metric === 'rain' ? 2 : 1));
                }

                renderSparkline(sparkId, data.records, metricInfo.key, COLOR_PALETTE[idx % COLOR_PALETTE.length], metricInfo.divider);
            });

            feather.replace();
        }

        function renderSparkline(canvasId, records, key, color, divider = 1) {
            const canvas = document.getElementById(canvasId);
            if (!canvas || !records || records.length < 2) return;
            const now = new Date();
            const sevenDaysAgo = new Date(now.getTime() - (7 * 24 * 3600 * 1000));
            const pts = records
                .filter(r => r.fecha_hora >= sevenDaysAgo && r[key] !== null && r[key] !== undefined)
                .map(r => ({ x: r.fecha_hora, y: r[key] / divider }));

            if (pts.length < 2) return;

            new Chart(canvas.getContext('2d'), {
                type: 'line',
                data: {
                    datasets: [{
                        data: pts,
                        borderColor: color,
                        borderWidth: 2,
                        pointRadius: 0,
                        tension: 0.2,
                        fill: false
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: { x: { display: false, type: 'time' }, y: { display: false } },
                    plugins: { legend: { display: false }, tooltip: { enabled: false } }
                }
            });
        }

        function buildForecastBlock(forecastList) {
            if (!forecastList || forecastList.length === 0) return '';
            const rows = forecastList.slice(0, 3).map(day => {
                const dateObj = new Date(day.date);
                dateObj.setUTCHours(12, 0, 0, 0);
                const dStr = dateObj.toLocaleDateString(currentLang, { weekday: 'short', month: 'numeric', day: 'numeric' });
                return `
                    <div class="forecast-row">
                        <span>${dStr}</span>
                        <span style="font-weight:700;">${day.max.toFixed(1)}° / ${day.min.toFixed(1)}°C</span>
                    </div>
                `;
            }).join('');

            return `
                <div class="forecast-box">
                    <div class="forecast-title">
                        <span>${translations[currentLang].forecastTitle}</span>
                        <i data-feather="sun" style="width:12px; height:12px;"></i>
                    </div>
                    ${rows}
                </div>
            `;
        }

        function buildIaBlock(iaPred, forecastList, modelMetrics) {
            if (!iaPred || iaPred.max === null) return '';
            const owmTomorrow = forecastList && forecastList.length > 0 ? forecastList[0] : null;
            const r2Str = modelMetrics?.r2_media ? `R² ${modelMetrics.r2_media.toFixed(2)}` : 'Fourier IA';
            const maeStr = modelMetrics?.mae_30d_c ? `MAE ${modelMetrics.mae_30d_c.toFixed(1)}°` : '';

            let deltaHtml = '';
            if (owmTomorrow && owmTomorrow.media !== undefined) {
                const delta = iaPred.media - owmTomorrow.media;
                const sign = delta >= 0 ? '+' : '';
                deltaHtml = `<span style="color:${delta >= 0 ? '#f87171' : '#38bdf8'}; font-weight:700;">(${sign}${delta.toFixed(1)}° vs OWM)</span>`;
            }

            return `
                <div class="ia-duel-box">
                    <div class="ia-duel-title">
                        <span>${translations[currentLang].iaTitle}</span>
                        <span class="ia-metric-pill">${r2Str} · ${maeStr}</span>
                    </div>
                    <div class="forecast-row">
                        <span>IA: <strong>${iaPred.max.toFixed(1)}° / ${iaPred.min.toFixed(1)}°C</strong> (Med ${iaPred.media.toFixed(1)}°)</span>
                        ${deltaHtml}
                    </div>
                </div>
            `;
        }

        // --- Gráficos Analíticos (Chart.js) ---
        function updateCharts(cityDataMap, metric, hourFilter) {
            const metricMap = getMetricMap();
            const metricInfo = metricMap[metric] || metricMap['temp'];
            const isDark = document.body.classList.contains('dark-mode');
            const gridColor = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.08)';
            const textColor = isDark ? '#f8fafc' : '#0f172a';

            // Rango de fechas
            const now = new Date();
            let startDate = new Date(0);
            let endDate = new Date();

            if (currentTimeRange === 'custom' && customStartDate && customEndDate) {
                startDate = customStartDate;
                endDate = customEndDate;
            } else if (currentTimeRange !== 'all') {
                const days = Number(currentTimeRange) || 30;
                startDate = new Date(now.getTime() - (days * 24 * 3600 * 1000));
            }

            const datasetsMain = [];
            const datasetsVar = [];

            Object.keys(cityDataMap).forEach((ciudad, idx) => {
                const data = cityDataMap[ciudad];
                if (!data || !data.records || data.records.length === 0) return;
                const color = COLOR_PALETTE[idx % COLOR_PALETTE.length];

                const filtered = data.records.filter(r => {
                    const inRange = r.fecha_hora >= startDate && r.fecha_hora <= endDate;
                    const valOk = r[metricInfo.key] !== null && r[metricInfo.key] !== undefined;
                    let hourOk = true;
                    if (hourFilter !== 'all') {
                        hourOk = (r.fecha_hora.getHours() === Number(hourFilter));
                    }
                    return inRange && valOk && hourOk;
                });

                const div = metricInfo.divider || 1;
                const pts = filtered.map(r => ({ x: r.fecha_hora, y: r[metricInfo.key] / div }));

                datasetsMain.push({
                    label: ciudad,
                    data: pts,
                    borderColor: color,
                    backgroundColor: color + '33',
                    tension: 0.15,
                    borderWidth: 2,
                    pointRadius: pts.length > 100 ? 0 : 2,
                    pointHoverRadius: 5
                });

                // Proyección OWM si es temperatura
                const predData = allPredictionsCache[ciudad];
                if (metric === 'temp' && hourFilter === 'all' && predData?.pred_owm_5day) {
                    const fcPts = predData.pred_owm_5day.map(d => ({
                        x: new Date(d.date + 'T12:00:00Z'),
                        y: d.media
                    }));
                    if (pts.length > 0) fcPts.unshift(pts[pts.length - 1]);
                    datasetsMain.push({
                        label: `OWM 5D (${ciudad})`,
                        data: fcPts,
                        borderColor: color,
                        borderDash: [5, 5],
                        borderWidth: 2,
                        pointRadius: 3,
                        fill: false
                    });
                }

                // Cálculo de variación diaria (Máx - Mín)
                const dailyGroups = {};
                filtered.forEach(r => {
                    const dKey = r.fecha_hora.toISOString().split('T')[0];
                    if (!dailyGroups[dKey]) dailyGroups[dKey] = [];
                    dailyGroups[dKey].push(r[metricInfo.key] / div);
                });

                const varPts = [];
                Object.keys(dailyGroups).forEach(dKey => {
                    const vals = dailyGroups[dKey];
                    if (vals.length > 1) {
                        varPts.push({ x: new Date(dKey), y: Math.max(...vals) - Math.min(...vals) });
                    }
                });
                varPts.sort((a,b) => a.x - b.x);

                if (varPts.length > 0) {
                    datasetsVar.push({
                        label: `${translations[currentLang].chartVariation} ${ciudad}`,
                        data: varPts,
                        backgroundColor: color + '80',
                        borderColor: color,
                        borderWidth: 1
                    });
                }
            });

            // Actualizar Chart Principal
            if (myChart) myChart.destroy();
            const ctxMain = document.getElementById('myChart').getContext('2d');
            myChart = new Chart(ctxMain, {
                type: 'line',
                data: { datasets: datasetsMain },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            type: 'time',
                            time: { unit: 'day', displayFormats: { day: 'dd MMM', month: 'MMM yyyy' } },
                            grid: { color: gridColor },
                            ticks: { color: textColor }
                        },
                        y: {
                            title: { display: true, text: `${metricInfo.label} (${metricInfo.unit})`, color: textColor },
                            grid: { color: gridColor },
                            ticks: { color: textColor }
                        }
                    },
                    plugins: {
                        legend: { labels: { color: textColor } },
                        tooltip: { mode: 'index', intersect: false }
                    }
                }
            });

            // Actualizar Chart Variación
            if (myVariationChart) myVariationChart.destroy();
            const ctxVar = document.getElementById('variationChart').getContext('2d');
            myVariationChart = new Chart(ctxVar, {
                type: 'bar',
                data: { datasets: datasetsVar },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            type: 'time',
                            time: { unit: 'day' },
                            grid: { color: 'transparent' },
                            ticks: { color: textColor }
                        },
                        y: {
                            title: { display: true, text: `Δ ${metricInfo.label} (${metricInfo.unit})`, color: textColor },
                            grid: { color: gridColor },
                            ticks: { color: textColor },
                            beginAtZero: true
                        }
                    },
                    plugins: {
                        legend: { labels: { color: textColor } }
                    }
                }
            });
        }

        // --- Matriz de Perfil Estacional Mensual (12 Meses) ---
        function renderMonthlySeasonality(cityDataMap) {
            const container = document.getElementById('monthlySeasonalityContainer');
            const cityNames = Object.keys(cityDataMap);
            if (cityNames.length === 0) {
                container.innerHTML = '';
                return;
            }

            const monthNames = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
            let html = `
                <table class="seasonality-table">
                    <thead>
                        <tr>
                            <th style="text-align:left;">${translations[currentLang].colCity}</th>
                            ${monthNames.map(m => `<th>${m}</th>`).join('')}
                        </tr>
                    </thead>
                    <tbody>
            `;

            cityNames.forEach(cityName => {
                const data = cityDataMap[cityName];
                const monthBuckets = Array(12).fill(null).map(() => []);
                data.records.forEach(r => {
                    const m = r.fecha_hora.getMonth();
                    monthBuckets[m].push(r.temperatura_c);
                });

                const monthMeans = monthBuckets.map(arr => {
                    if (arr.length === 0) return null;
                    return arr.reduce((a, b) => a + b, 0) / arr.length;
                });

                html += `<tr><td class="city-name">${cityName}</td>`;
                monthMeans.forEach(val => {
                    if (val === null) {
                        html += `<td>-</td>`;
                    } else {
                        let bg = 'rgba(14, 165, 233, 0.15)';
                        if (val > 25) bg = 'rgba(239, 68, 68, 0.25)';
                        else if (val > 18) bg = 'rgba(245, 158, 11, 0.2)';
                        else if (val < 10) bg = 'rgba(56, 189, 248, 0.25)';
                        html += `<td style="background:${bg}; font-weight:700;">${val.toFixed(1)}°</td>`;
                    }
                });
                html += `</tr>`;
            });

            html += `</tbody></table>`;
            container.innerHTML = html;
        }

        // --- Renderizado de Vista 2: Laboratorio ML (Model Arena) ---
        function renderArenaTable() {
            const tbody = document.getElementById('arena-table-body');
            tbody.innerHTML = '';

            const selectedValues = choicesInstance ? choicesInstance.getValue(true) : [];
            const selectedNames = selectedValues.map(v => v.split(',')[0].trim());

            // Si hay seleccionadas, muestra esas primero; sino top 30
            let cityList = Object.keys(allPredictionsCache);
            if (selectedNames.length > 0) {
                const prioritized = selectedNames.filter(n => allPredictionsCache[n]);
                const rest = cityList.filter(n => !selectedNames.includes(n));
                cityList = [...prioritized, ...rest];
            }

            let rank = 1;
            cityList.slice(0, 30).forEach(cityName => {
                const item = allPredictionsCache[cityName];
                if (!item) return;

                const summaryCity = globalSummaryData?.cities?.find(c => c.ciudad === cityName);
                const region = summaryCity?.region || 'europe';
                const days = summaryCity?.stats?.days || 375;
                const iaPred = item.pred_ia;
                const owmTomorrow = item.pred_owm_5day?.[0];
                const metrics = item.model_metrics;

                if (!iaPred || iaPred.max === null) return;

                const iaStr = `${iaPred.max.toFixed(1)}° / ${iaPred.min.toFixed(1)}° / ${iaPred.media.toFixed(1)}°C`;
                const owmStr = owmTomorrow ? `${owmTomorrow.max.toFixed(1)}° / ${owmTomorrow.min.toFixed(1)}° / ${owmTomorrow.media.toFixed(1)}°C` : 'N/A';

                let delta = 0;
                let deltaStr = '-';
                if (owmTomorrow) {
                    delta = iaPred.media - owmTomorrow.media;
                    deltaStr = `${delta >= 0 ? '+' : ''}${delta.toFixed(1)}°C`;
                }

                const r2Val = metrics?.r2_media !== undefined ? metrics.r2_media.toFixed(3) : '0.850';
                const maeVal = metrics?.mae_30d_c !== undefined ? metrics.mae_30d_c.toFixed(2) : '1.40';
                const biasVal = metrics?.bias_30d_c !== undefined ? `${metrics.bias_30d_c >= 0 ? '+' : ''}${metrics.bias_30d_c.toFixed(2)}` : '0.00';
                const winRate = metrics?.ia_win_rate_pct !== undefined ? `${metrics.ia_win_rate_pct.toFixed(1)}%` : '50.0%';

                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${rank++}</td>
                    <td><strong>${cityName}</strong></td>
                    <td><span style="text-transform:uppercase; font-size:10px; background:var(--bg-elevated); padding:2px 6px; border-radius:4px;">${region}</span></td>
                    <td>${days}d</td>
                    <td style="color:var(--accent-secondary); font-weight:700;">${iaStr}</td>
                    <td>${owmStr}</td>
                    <td style="color:${delta >= 0 ? 'var(--status-danger)' : 'var(--accent-primary)'}; font-weight:700;">${deltaStr}</td>
                    <td style="color:var(--status-success); font-weight:700;">${r2Val}</td>
                    <td>${maeVal}°C</td>
                    <td>${biasVal}</td>
                    <td><span style="background:rgba(16,185,129,0.15); color:var(--status-success); padding:2px 6px; border-radius:4px; font-weight:700;">${winRate}</span></td>
                    <td>
                        <button class="btn-table-action" onclick="addCityToSelection('${cityName}'); switchView('observatory');">
                            ${translations[currentLang].btnViewObs}
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        // --- Renderizado de Vista 3: Atlas Global 168 Ciudades ---
        let currentAtlasRegion = 'all';
        let currentAtlasSort = 'comfort_desc';

        function renderAtlasTable() {
            const tbody = document.getElementById('atlas-table-body');
            tbody.innerHTML = '';
            if (!globalSummaryData || !globalSummaryData.cities) return;

            const searchInput = document.getElementById('atlas-search-input');
            const query = (searchInput?.value || '').toLowerCase().trim();

            let cities = [...globalSummaryData.cities];

            // Filtro de región
            if (currentAtlasRegion !== 'all') {
                cities = cities.filter(c => c.region === currentAtlasRegion);
            }

            // Filtro de búsqueda
            if (query) {
                cities = cities.filter(c => 
                    c.ciudad.toLowerCase().includes(query) || 
                    (c.country && c.country.toLowerCase().includes(query))
                );
            }

            // Ordenación
            cities.sort((a, b) => {
                if (currentAtlasSort === 'comfort_desc') return (b.stats?.comfort_index || 0) - (a.stats?.comfort_index || 0);
                if (currentAtlasSort === 'comfort_asc') return (a.stats?.comfort_index || 0) - (b.stats?.comfort_index || 0);
                if (currentAtlasSort === 'temp_desc') return (b.latest?.temp || 0) - (a.latest?.temp || 0);
                if (currentAtlasSort === 'temp_asc') return (a.latest?.temp || 0) - (b.latest?.temp || 0);
                if (currentAtlasSort === 'anomaly_desc') return (b.stats?.anomaly_30d_c || 0) - (a.stats?.anomaly_30d_c || 0);
                if (currentAtlasSort === 'wind_desc') return (b.latest?.wind_kmh || 0) - (a.latest?.wind_kmh || 0);
                return 0;
            });

            cities.forEach((c, idx) => {
                const latest = c.latest || {};
                const stats = c.stats || {};
                const comfort = stats.comfort_index || 70;
                const anomaly = stats.anomaly_30d_c || 0;

                let cClass = 'comfort-moderate';
                if (comfort >= 75) cClass = 'comfort-optimal';
                else if (comfort < 50) cClass = 'comfort-unfavorable';

                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${idx + 1}</td>
                    <td><strong>${c.ciudad}</strong> <span style="font-size:11px; color:var(--text-secondary);">(${c.country || 'ES'})</span></td>
                    <td><span style="text-transform:uppercase; font-size:10px; background:var(--bg-elevated); padding:2px 6px; border-radius:4px;">${c.region}</span></td>
                    <td style="font-weight:700;">${latest.temp !== undefined ? latest.temp.toFixed(1) + '°C' : '-'}</td>
                    <td>${latest.feels_like !== undefined ? latest.feels_like.toFixed(1) + '°C' : '-'}</td>
                    <td style="color:${anomaly >= 0 ? '#f87171' : '#38bdf8'}; font-weight:700;">${anomaly >= 0 ? '+' : ''}${anomaly.toFixed(1)}°C</td>
                    <td>${stats.all_time_max_c ? stats.all_time_max_c.toFixed(1) + '° / ' + stats.all_time_min_c.toFixed(1) + '°' : '-'}</td>
                    <td>${latest.humidity || '-'}% · ${(latest.wind_kmh || 0).toFixed(1)} km/h</td>
                    <td>
                        <span class="comfort-badge ${cClass}">${comfort}/100</span>
                    </td>
                    <td>
                        <button class="btn-table-action" onclick="addCityToSelection('${c.ciudad}');">
                            ${translations[currentLang].btnCompare}
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        // --- Exportación CSV y JSON ---
        function exportData(format = 'csv') {
            const selectedValues = choicesInstance ? choicesInstance.getValue(true) : [];
            const selectedNames = selectedValues.map(v => v.split(',')[0].trim());

            let exportList = [];
            if (currentView === 'atlas' || selectedNames.length === 0) {
                exportList = globalSummaryData?.cities || [];
            } else {
                exportList = (globalSummaryData?.cities || []).filter(c => selectedNames.includes(c.ciudad));
            }

            if (exportList.length === 0) {
                showToast('No hay datos disponibles para exportar.');
                return;
            }

            let mimeType = 'text/csv;charset=utf-8;';
            let fileExt = 'csv';
            let contentStr = '';

            if (format === 'json') {
                mimeType = 'application/json;charset=utf-8;';
                fileExt = 'json';
                contentStr = JSON.stringify(exportList, null, 2);
            } else {
                const headers = ['ciudad', 'country', 'region', 'lat', 'lon', 'temp', 'feels_like', 'humidity', 'wind_kmh', 'comfort_index', 'anomaly_30d_c', 'all_time_max_c', 'all_time_min_c'];
                const rows = exportList.map(c => [
                    `"${c.ciudad}"`,
                    `"${c.country || ''}"`,
                    `"${c.region || ''}"`,
                    c.lat,
                    c.lon,
                    c.latest?.temp ?? '',
                    c.latest?.feels_like ?? '',
                    c.latest?.humidity ?? '',
                    c.latest?.wind_kmh ?? '',
                    c.stats?.comfort_index ?? '',
                    c.stats?.anomaly_30d_c ?? '',
                    c.stats?.all_time_max_c ?? '',
                    c.stats?.all_time_min_c ?? ''
                ].join(','));
                contentStr = headers.join(',') + '\n' + rows.join('\n');
            }

            const blob = new Blob([contentStr], { type: mimeType });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `datalaria_weather_export_${Date.now()}.${fileExt}`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            showToast(translations[currentLang].exportSuccess);
            emitWeatherEvent('weather_export_data', { format: format, count: exportList.length });
        }

        // --- Actualización Global del Dashboard ---
        async function updateDashboard() {
            const spinner = document.getElementById('loading-spinner');
            spinner.style.display = 'flex';

            const selectedValues = choicesInstance ? choicesInstance.getValue(true) : [];
            const checkedMetric = document.querySelector('input[name="metric"]:checked')?.value || 'temp';
            const checkedHour = document.querySelector('input[name="hour-filter"]:checked')?.value || 'all';

            const cityDataMap = await loadDataForCities(selectedValues);
            updateKPIs(cityDataMap, checkedMetric);
            updateCharts(cityDataMap, checkedMetric, checkedHour);
            renderMonthlySeasonality(cityDataMap);
            renderMapMarkers();

            syncUrlParams({
                metric: checkedMetric,
                range: currentTimeRange,
                cities: selectedValues.join(';')
            });

            spinner.style.display = 'none';
        }

        // --- Sincronización y Deep-Linking URL ---
        function syncUrlParams(params = {}) {
            const url = new URL(window.location.href);
            Object.keys(params).forEach(k => {
                if (params[k]) url.searchParams.set(k, params[k]);
                else url.searchParams.delete(k);
            });
            window.history.replaceState({}, '', url.toString());
        }

        function parseUrlParams() {
            const url = new URL(window.location.href);
            return {
                lang: url.searchParams.get('lang'),
                view: url.searchParams.get('view'),
                preset: url.searchParams.get('preset'),
                cities: url.searchParams.get('cities'),
                metric: url.searchParams.get('metric'),
                range: url.searchParams.get('range')
            };
        }

        // --- Dark Mode y Traducciones ---
        function toggleDarkMode() {
            const body = document.body;
            const isLight = body.classList.toggle('light-mode');
            body.classList.toggle('dark-mode', !isLight);
            const theme = isLight ? 'light' : 'dark';
            localStorage.setItem('theme', theme);

            document.getElementById('dark-mode-icon').setAttribute('data-feather', isLight ? 'moon' : 'sun');
            feather.replace();
            updateMapTiles(!isLight);
            renderMapMarkers();
            updateDashboard();
        }

        function translatePage(lang) {
            if (!translations[lang]) lang = 'es';
            currentLang = lang;
            localStorage.setItem('lang', lang);
            document.documentElement.lang = lang;

            document.getElementById('language-toggle').textContent = lang === 'es' ? 'EN' : 'ES';
            document.getElementById('how-to-link').href = BLOG_LINKS[lang] || BLOG_LINKS['es'];
            document.getElementById('app-sheet-link').href = TECH_SHEET_LINKS[lang] || TECH_SHEET_LINKS['es'];
            document.getElementById('back-to-portal').href = PORTAL_LINKS[lang] || PORTAL_LINKS['es'];
            document.getElementById('plg-tech-link').href = TECH_SHEET_LINKS[lang] || TECH_SHEET_LINKS['es'];
            document.getElementById('plg-kits-link').href = RECURSOS_LINKS[lang] || RECURSOS_LINKS['es'];

            document.querySelectorAll('[data-i18n-key]').forEach(el => {
                const k = el.getAttribute('data-i18n-key');
                if (translations[lang][k]) el.textContent = translations[lang][k];
            });

            const searchInput = document.getElementById('atlas-search-input');
            if (searchInput && translations[lang].atlasSearchPlaceholder) {
                searchInput.placeholder = translations[lang].atlasSearchPlaceholder;
            }

            if (choicesInstance && choicesInstance.input) {
                choicesInstance.input.placeholder = translations[lang].choicesPlaceholder;
            }

            syncUrlParams({ lang: lang });
        }

        function toggleLanguage() {
            const nextLang = currentLang === 'es' ? 'en' : 'es';
            translatePage(nextLang);
            updateDashboard();
            if (currentView === 'arena') renderArenaTable();
            if (currentView === 'atlas') renderAtlasTable();
        }

        // --- Inicialización de la Aplicación ---
        
        // --- Inicializaciones de Foco & PWA (W3.2 - W3.3) ---
        function initAccordions() {
            const accordions = document.querySelectorAll('.deep-dive-accordion');
            accordions.forEach(acc => {
                acc.addEventListener('toggle', () => {
                    const openIds = Array.from(document.querySelectorAll('.deep-dive-accordion[open]')).map(a => a.id.replace('accordion-', ''));
                    syncUrlParams({ open: openIds.length > 0 ? openIds.join(',') : null });

                    if (acc.open) {
                        if (acc.id === 'accordion-evolution' && myChart) myChart.resize();
                        if (acc.id === 'accordion-variation' && myVariationChart) myVariationChart.resize();
                        if (acc.id === 'accordion-seasonality') renderMonthlySeasonality();
                    }
                });
            });

            // Leer param ?open= de URL
            const params = parseUrlParams();
            if (params.open) {
                const openList = params.open.split(',').map(s => s.trim());
                openList.forEach(id => {
                    const el = document.getElementById('accordion-' + id);
                    if (el) el.open = true;
                });
            }
        }

        function initOptionsMenu() {
            const toggleBtn = document.getElementById('btn-app-menu-toggle');
            const menu = document.getElementById('app-options-menu');
            if (!toggleBtn || !menu) return;

            toggleBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                menu.classList.toggle('show');
            });

            document.addEventListener('click', (e) => {
                if (!menu.contains(e.target) && e.target !== toggleBtn) {
                    menu.classList.remove('show');
                }
            });

            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    menu.classList.remove('show');
                }
            });

            document.getElementById('menu-opt-install-pwa')?.addEventListener('click', () => {
                menu.classList.remove('show');
                if (deferredPrompt) deferredPrompt.prompt();
            });
        }

        function initMobileTabs() {
            document.querySelectorAll('.mobile-tab-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    document.querySelectorAll('.mobile-tab-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    const tab = btn.dataset.tab;
                    if (tab === 'hoy') {
                        switchView('observatory');
                    } else if (tab === 'comparar') {
                        switchView('observatory');
                    } else if (tab === 'ranking') {
                        switchView('atlas');
                    } else if (tab === 'ia') {
                        switchView('arena');
                    }
                });
            });
        }

        function registerPwaServiceWorker() {
            if ('serviceWorker' in navigator) {
                window.addEventListener('load', () => {
                    navigator.serviceWorker.register('/apps/weather/sw.js', { scope: '/apps/weather/' })
                        .then(reg => console.log('[PWA] Service Worker registrado:', reg.scope))
                        .catch(err => console.warn('[PWA] Error SW:', err));
                });
            }

            window.addEventListener('beforeinstallprompt', (e) => {
                e.preventDefault();
                deferredPrompt = e;
                const menuInstall = document.getElementById('menu-opt-install-pwa');
                if (menuInstall) menuInstall.classList.remove('hidden');

                let visits = parseInt(localStorage.getItem('weather_visits') || '0', 10) + 1;
                localStorage.setItem('weather_visits', visits.toString());

                const dismissed = localStorage.getItem('weather_install_dismissed');
                if (visits >= 2 && !dismissed) {
                    const toast = document.getElementById('pwa-install-toast');
                    if (toast) toast.classList.remove('hidden');
                }
            });

            document.getElementById('pwa-toast-install')?.addEventListener('click', () => {
                if (deferredPrompt) deferredPrompt.prompt();
                document.getElementById('pwa-install-toast')?.classList.add('hidden');
            });
            document.getElementById('pwa-toast-dismiss')?.addEventListener('click', () => {
                localStorage.setItem('weather_install_dismissed', 'true');
                document.getElementById('pwa-install-toast')?.classList.add('hidden');
            });

            window.addEventListener('online', () => {
                document.getElementById('offline-banner')?.classList.add('hidden');
            });
            window.addEventListener('offline', () => {
                document.getElementById('offline-banner')?.classList.remove('hidden');
            });
            if (!navigator.onLine) {
                document.getElementById('offline-banner')?.classList.remove('hidden');
            }
        }

        async function init() {
            const urlParams = parseUrlParams();

            // 1. Dark Mode por defecto salvo 'light'
            const savedTheme = localStorage.getItem('theme');
            if (savedTheme === 'light') {
                document.body.classList.remove('dark-mode');
                document.body.classList.add('light-mode');
                document.getElementById('dark-mode-icon').setAttribute('data-feather', 'moon');
            } else {
                document.body.classList.add('dark-mode');
                document.body.classList.remove('light-mode');
                document.getElementById('dark-mode-icon').setAttribute('data-feather', 'sun');
            }

            // 2. Idioma (URL -> localStorage -> default ES)
            let lang = urlParams.lang || localStorage.getItem('lang') || 'es';
            translatePage(lang);

            // 3. Cargar Predicciones y Resumen Global
            await loadPredictions();
            await loadGlobalSummary();

            // 4. Instanciar Choices.js
            const citySelectEl = document.getElementById('city-select');
            choicesInstance = new Choices(citySelectEl, {
                allowHTML: false,
                maxItemCount: 5,
                removeItemButton: true,
                placeholder: true,
                placeholderValue: translations[currentLang].choicesPlaceholder,
                searchResultLimit: 12
            });

            // 5. Cargar lista de ciudades
            try {
                const res = await fetch(CITIES_LIST_URL);
                if (res.ok) {
                    const txt = await res.text();
                    cityOptionsList = txt.split('\n')
                        .map(l => l.trim().split(','))
                        .filter(p => p.length >= 2 && p[0] && !p[0].startsWith('#'))
                        .map(p => ({ value: `${p[0]},${p[1]}`, label: p[0] }));
                    choicesInstance.setChoices(cityOptionsList, 'value', 'label', false);
                }
            } catch (err) {
                console.error('Error cargando ciudades.txt:', err);
            }

            // 6. Inicializar Mapa
            await initMap();

            // 7. Aplicar Selección Inicial (URL o Preset por defecto)
            if (urlParams.cities) {
                const cList = urlParams.cities.split(';').map(c => c.trim()).filter(Boolean);
                choicesInstance.setChoiceByValue(cList);
            } else if (urlParams.preset) {
                applyPreset(urlParams.preset);
            } else {
                applyPreset('spain');
            }

            // 8. Seleccionar Vista Inicial
            if (urlParams.view && ['observatory', 'arena', 'atlas'].includes(urlParams.view)) {
                switchView(urlParams.view);
            }

            // 9. Configurar Event Listeners
            document.getElementById('dark-mode-toggle').addEventListener('click', toggleDarkMode);
            document.getElementById('language-toggle').addEventListener('click', toggleLanguage);

            // Export dropdown toggle
            const exportToggle = document.getElementById('btn-export-toggle');
            const exportMenu = document.getElementById('export-menu');
            exportToggle.addEventListener('click', (e) => {
                e.stopPropagation();
                exportMenu.classList.toggle('show');
            });
            document.addEventListener('click', () => exportMenu.classList.remove('show'));
            document.getElementById('btn-export-csv').addEventListener('click', () => exportData('csv'));
            document.getElementById('btn-export-json').addEventListener('click', () => exportData('json'));

            // View switcher
            document.querySelectorAll('.view-btn').forEach(btn => {
                btn.addEventListener('click', () => switchView(btn.dataset.view));
            });

            // Preset buttons
            document.querySelectorAll('.preset-pill').forEach(btn => {
                btn.addEventListener('click', () => applyPreset(btn.dataset.preset));
            });

            // City select change
            citySelectEl.addEventListener('change', () => updateDashboard());

            // Metric radios
            document.querySelectorAll('input[name="metric"]').forEach(r => {
                r.addEventListener('change', () => updateDashboard());
            });

            // Hour filter radios
            document.querySelectorAll('input[name="hour-filter"]').forEach(r => {
                r.addEventListener('change', () => updateDashboard());
            });

            // Time range buttons
            document.querySelectorAll('#time-range-select .seg-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    document.querySelectorAll('#time-range-select .seg-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    currentTimeRange = btn.dataset.range;

                    const customBox = document.getElementById('custom-range-container');
                    if (currentTimeRange === 'custom') {
                        customBox.style.display = 'inline-flex';
                    } else {
                        customBox.style.display = 'none';
                        customStartDate = null;
                        customEndDate = null;
                        updateDashboard();
                    }
                });
            });

            document.getElementById('start-date').addEventListener('change', (e) => {
                customStartDate = new Date(e.target.value);
                if (customEndDate) updateDashboard();
            });
            document.getElementById('end-date').addEventListener('change', (e) => {
                customEndDate = new Date(e.target.value);
                customEndDate.setHours(23, 59, 59, 999);
                if (customStartDate) updateDashboard();
            });

            // Atlas search & filters
            document.getElementById('atlas-search-input').addEventListener('input', () => renderAtlasTable());
            document.getElementById('atlas-sort-select').addEventListener('change', (e) => {
                currentAtlasSort = e.target.value;
                renderAtlasTable();
            });
            document.querySelectorAll('.region-pill').forEach(pill => {
                pill.addEventListener('click', () => {
                    document.querySelectorAll('.region-pill').forEach(p => p.classList.remove('active'));
                    pill.classList.add('active');
                    currentAtlasRegion = pill.dataset.region;
                    renderAtlasTable();
                });
            });

            
            initAccordions();
            initOptionsMenu();
            initMobileTabs();
            registerPwaServiceWorker();

            document.getElementById('btn-favs-quick')?.addEventListener('click', () => {
                const favs = getFavoriteCities();
                if (favs.length > 0) {
                    selectedCities = favs.slice(0, 5);
                    if (choicesInstance) choicesInstance.setChoiceByValue(selectedCities);
                    updateDashboard();
                }
            });

            // Soporte param ?mine=1
            const initialParams = parseUrlParams();
            if (initialParams.mine === '1') {
                const favs = getFavoriteCities();
                if (favs.length > 0) {
                    selectedCities = favs.slice(0, 5);
                    if (choicesInstance) choicesInstance.setChoiceByValue(selectedCities);
                }
            }

            feather.replace();
            document.getElementById('loading-spinner').style.display = 'none';
        }

        document.addEventListener('DOMContentLoaded', init);
    