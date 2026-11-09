---
title: "Weather Intelligence v3.1"
description: "Centro de control meteorológico global y laboratorio cuantitativo: 168 estaciones, estacionalidad armónica de Fourier, walk-forward backtesting IA vs. OWM e índice de confort outdoor."
app: "weather"
translationKey: "app-weather"
layout: "single"
---

## 🌟 Novedades de Weather Intelligence v3.1

Weather Intelligence v3.1 incorpora una nueva dimensión de **honestidad estadística y divulgación climática**:

- **Diagnóstico "¿Es normal?":** Cada estación evalúa su temperatura actual frente a la línea base propia de los últimos 375 días ($\pm 7$ días del año excluyendo el propio día, según `INV-WEATHER-11`), determinando si la jornada se sitúa en un percentil extremo ($p \le 10$ o $p \ge 90$) o bate un récord mensual medido desde octubre de 2025.
- **Calendario Térmico (Warming Stripes):** Visualización interactiva de franjas climáticas para los 365 días del año por ciudad, mapeando anomalías térmicas en escala divergente de $\pm 5^\circ\text{C}$ con tooltip dinámico al milisegundo.
- **Marcador Público IA vs. OpenWeatherMap:** Auditoría auditable en dos capas que transparenta el error absoluto medio (MAE) a $D+1..D+5$ y recuenta las victorias semanales de acierto (`INV-WEATHER-12`).
- **Laboratorio ML "¿Por qué predice esto?":** Explicabilidad determinista sin modelos de caja negra, descomponiendo la predicción en contribuciones lineales de inercia térmica, ciclo armónico de Fourier y humedad (`INV-WEATHER-13`).

---

## 🚀 Centro de Control y Acceso Directo por Escenarios (1 Clic)

Weather Intelligence v3.1 incorpora un sistema de **enlaces profundos (*Deep-Linking*)** que te permite saltar de forma instantánea a configuraciones analíticas preparadas sin necesidad de configurar filtros manualmente:

| Escenario Temático | Vista Objetivo | Ciudades & Enfoque | Enlace Directo |
| :--- | :--- | :--- | :--- |
| **🇪🇸 Eje Ibérico** | Observatorio | Madrid, Barcelona, Bilbao, Sevilla y León | [Abrir Escenario España ↗](/apps/weather/?preset=spain&lang=es) |
| **🌍 Hubs Globales** | Observatorio | Madrid, Londres, Nueva York, Tokio y Singapur | [Abrir Hubs Globales ↗](/apps/weather/?preset=global&lang=es) |
| **🔥❄️ Extremos Hoy** | Observatorio | Filtro dinámico de las 2 más cálidas y 2 más frías del planeta | [Explorar Extremos Térmicos ↗](/apps/weather/?preset=extremes&lang=es) |
| **🤖 Duelo IA vs. OWM** | Laboratorio ML | Comparativa Walk-Forward: Regresión Fourier vs. Pronóstico Oficial | [Abrir Laboratorio ML Arena ↗](/apps/weather/?preset=ai_duel&view=arena&lang=es) |
| **🏃‍♂️ Top Confort Outdoor** | Atlas Global | Ranking ordenado de mayor a menor índice bioclimático (0–100) | [Explorar Atlas de Confort ↗](/apps/weather/?preset=comfort&view=atlas&lang=es) |

---

## 📊 Cobertura Geográfica: Red de 168 Estaciones en 6 Regiones

La red de telemetría ingesta datos de **168 estaciones meteorológicas activas** distribuidas por los 5 continentes, garantizando una muestra planetaria heterogénea y de alta fidelidad:

| Región Canónica | Estaciones Auditadas | Ejemplos Representativos | Clima y Comportamiento |
| :--- | :---: | :--- | :--- |
| **🇪🇸 España** | **56** | Madrid, Barcelona, Sevilla, León, Gijón, Santa Cruz de Tenerife | Contrastes mediterráneo, atlántico, continental y subtropical |
| **🇪🇺 Europa** | **47** | Londres, París, Berlín, Reikiavik, Roma, Varsovia, Atenas | Climas templados oceánicos, alpinos, boreales y mediterráneos |
| **🌏 Asia** | **25** | Tokio, Bangkok, Singapur, Dubái, Pekín, Ulán Bator | Monzónicos tropicales, áridos extremos y continentales siberianos |
| **🌎 América** | **23** | Nueva York, Buenos Aires, São Paulo, Bogotá, Vancouver | Gran gradiente latitudinal norte-sur y regímenes andinos |
| **🌍 África** | **13** | El Cairo, Nairobi, Rabat, Abuja, Ciudad del Cabo, Johannesburgo | Ecuatoriales, sahelianos, saharianos y sudafricanos templados |
| **🇦🇺 Oceanía** | **4** | Sídney, Melbourne, Auckland, Wellington | Costeros templados con altas rachas de viento oceánico |

Cada estación acumula **más de 375 días continuos de registros** muestreados 3 veces al día (06:00, 14:00 y 22:00 UTC), totalizando **más de 192.000 observaciones empíricas** normalizadas en 15 variables meteorológicas canónicas.

---

## 📐 Fundamentos Cuantitativos: Fourier y Confort Bioclimático

### 1. Transformación Estacional Armónica de Fourier ($\sin / \cos$)

Las regresiones meteorológicas tradicionales sobre el día del año ($d \in [1, 365]$) sufren una severa **discontinuidad de fin de año**: entre el 31 de diciembre ($d=365$) y el 1 de enero ($d=1$) el modelo detecta erróneamente un salto artificial de $-364$ unidades. 

Para resolverlo, Weather Intelligence v3.1 proyecta el ciclo anual sobre el círculo unitario mediante dos variables trigonométricas continuas:

$$\sin_{\text{day}} = \sin\left(\frac{2\pi \cdot \text{doy}}{365.25}\right), \quad \cos_{\text{day}} = \cos\left(\frac{2\pi \cdot \text{doy}}{365.25}\right)$$

Al combinar estos armónicos cíclicos con retardos térmicos autoregresivos ($\text{temp}_{\text{lag1}}$, $\text{temp}_{\text{lag2}}$) y el rango diurno ($\text{máx} - \text{mín}$), el coeficiente de determinación del modelo se eleva a:

$$R^2 > 0.85 \quad (\text{alcanzando } R^2 \ge 0.95 \text{ en climas templados})$$

### 2. Formulación Determinista del Índice de Confort Outdoor ($0..100$)

Diseñado bajo la rúbrica bioclimática de *LifeOps* y *Datalaria*, evalúa la idoneidad para actividades al aire libre penalizando factores de estrés ambiental:

1. **Puntaje Base por Desviación Térmica:**
   $$S_{\text{temp}} = \max\left(0, 100 - 3.5 \cdot \left|T_{\text{target}} - 21.0\right|^{1.25}\right)$$
   donde $T_{\text{target}} = 0.6 \cdot T_{\text{sensación}} + 0.4 \cdot T_{\text{aire}}$.
2. **Penalizaciones Ambientales:** Humedad extrema ($<30\%$ o $>70\%$), rachas de viento ($>15\text{ km/h}$), nubosidad densa ($>80\%$), precipitaciones (lluvia/nieve) y visibilidad reducida ($<5\text{ km}$).
3. **Escala de Interpretación:**
   - **$\ge 75$ (Óptimo / Verde):** Condiciones ideales para deporte y actividades exteriores.
   - **$50\text{--}74$ (Moderado / Ámbar):** Condiciones aceptables pero con viento o temperatura mejorable.
   - **$< 50$ (Desfavorable / Rojo):** Extremos de calor/frío, viento severo o precipitación activa.

---

## 💼 Conexión con el Ecosistema B2B de Datalaria

Esta aplicación es el **Caso de Estudio #3** del sistema operativo de ingeniería **Datalaria Helix**, demostrando cómo una arquitectura **100% Serverless de coste cero** puede sostener un activo analítico de nivel empresarial:

- **Evolución Modular:** Para empresas o instituciones que requieren migrar este flujo hacia nubes empresariales (Supabase PostgreSQL, DuckDB-Wasm o Parquet), consulta la metodología de **Datalaria Helix** (lanzamiento oficial en enero de 2027) y los [Kits de Decisión Cuantitativa en Recursos](/es/recursos/).
- **Código Fuente y Reproducibilidad:** El motor completo de ingestión (`read_weather.py`) y la interfaz ejecutiva están sincronizados de forma determinista bajo el contrato `INV-WEATHER-1..6`.
