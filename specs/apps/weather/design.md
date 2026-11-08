# Especificación de Diseño UX/UI: Weather Service (`weather`)

> **ID de Diseño:** `DESIGN-APP-WEATHER`  
> **Spec Técnica Vinculada:** [`specs/apps/weather/spec.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/apps/weather/spec.md) (`v2.0.0`)  
> **Agente Propietario:** 🎨 [`04-ux-ui` (Diseñador UX/UI)](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/04-ux-ui.md)  
> **Preset Estético Seleccionado:** `Executive Data-Dense` (Observatorio Climático & Laboratorio ML C-Level)

---

## 1. Dirección Estética y Psicología de Usuario

### 1.1 Perfil Visual del Usuario y Contexto de Uso
- **Quién lo usa y dónde:**
  1. **Profesionales técnicos, Data Scientists y lectores de Datalaria** en portátil (`1366×768` a `1920×1080`) o móvil (`390px`) que llegan desde los artículos de la serie o desde el escaparate `/apps/`.
  2. **Planificadores, deportistas (`LifeOps`) y viajeros** que quieren comparar de un vistazo el comportamiento climático real, las anomalías térmicas y la ventana óptima de confort outdoor entre 168 ciudades del mundo.
- **Sensación que debe transmitir en los primeros 3 segundos:** Un **Centro de Control Meteorológico y Cuantitativo de grado ejecutivo** (inspirado en *Windy Pro*, *Linear* y *Bloomberg Weather Terminal*), donde los 377 días y +192.000 registros se perciben vivos, auditables y accionables sin esperas.
- **Preset de Dirección Activo:**
  - [x] **`Executive Data-Dense` (Estándar B2B Datalaria — LifeOps / Pulse / Helix):** Modo oscuro profundo por defecto (`#0b0f17` / `#111827`), bordes sutiles iluminados, tipografía `Outfit + Inter + JetBrains Mono (tabular-nums)`, con soporte completo para conmutar a Modo Claro de alto contraste.

### 1.2 El «Momento Firma» (*Signature Wow Moment*)
- **Descripción del Momento Firma:** **Barra de Escenarios Comparativos en 1 Clic (*1-Click Climate Presets*) + Conmutador Instantáneo de 3 Vistas (`< 16ms`):**
  - Al pulsar cualquiera de los 5 Presets temáticos (`🇪🇸 Eje Ibérico`, `🌍 Hubs Financieros`, `🔥❄️ Extremos del Planeta Hoy`, `🤖 Duelo IA vs OWM`, `🏃‍♂️ Top Confort Outdoor`), el mapa Leaflet vuela suavemente hacia las estaciones seleccionadas, las Super-Cards animan el índice de confort (`0..100`) y las gráficas comparan al instante los perfiles térmicos sin recargar la página.

---

## 2. Sistema de Design Tokens (Variables CSS Canónicas)

> **Regla `INV-UX-1`:** Queda prohibido usar colores hexadecimales arbitrarios fuera de los tokens semánticos declarados en esta tabla.

### 2.1 Paleta Semántica de Color
| Token CSS | Valor (Dark Mode / Default) | Valor (Light Mode / Opcional) | Uso Semántico Exclusivo |
| :--- | :--- | :--- | :--- |
| `--bg-canvas` | `#0b0f17` | `#f8fafc` | Fondo principal de la aplicación |
| `--bg-surface` | `#111827` | `#ffffff` | Tarjetas KPI, paneles de gráficos y tablas |
| `--bg-elevated` | `#1e293b` | `#f1f5f9` | Barra de controles, píldoras inactivas, desplegables |
| `--text-primary` | `#f8fafc` | `#0f172a` | Títulos, cifras KPI principales y encabezados (Contraste $\ge 7:1$) |
| `--text-secondary` | `#94a3b8` | `#475569` | Etiquetas, ejes de gráficos, fechas y subtítulos (Contraste $\ge 4.5:1$) |
| `--accent-primary` | `#0ea5e9` | `#0284c7` | Acción primaria, pestaña activa y enlaces principales |
| `--accent-secondary` | `#8b5cf6` | `#7c3aed` | Badges del Motor IA (Scikit-Learn), Model Arena y upsell Helix |
| `--status-success` | `#10b981` | `#059669` | Confort Outdoor Óptimo ($\ge 75$), alta precisión IA ($\text{MAE} < 1.5^\circ\text{C}$) |
| `--status-warning` | `#f59e0b` | `#d97706` | Confort Moderado ($50\text{–}74$), anomalías térmicas moderadas |
| `--status-danger` | `#ef4444` | `#dc2626` | Extremos térmicos severos, anomalías $> 4^\circ\text{C}$ o viento fuerte |
| `--border-subtle` | `rgba(148, 163, 184, 0.16)` | `rgba(15, 23, 42, 0.12)` | Bordes de tarjetas, divisores de tablas y contenedores |
| `--temp-freezing` | `#38bdf8` | `#0284c7` | Escala térmica mapa/badges: $< 0^\circ\text{C}$ |
| `--temp-cold` | `#60a5fa` | `#2563eb` | Escala térmica mapa/badges: $0^\circ\text{C}\text{ a }10^\circ\text{C}$ |
| `--temp-mild` | `#34d399` | `#059669` | Escala térmica mapa/badges: $10^\circ\text{C}\text{ a }22^\circ\text{C}$ |
| `--temp-warm` | `#fbbf24` | `#d97706` | Escala térmica mapa/badges: $22^\circ\text{C}\text{ a }30^\circ\text{C}$ |
| `--temp-hot` | `#f87171` | `#dc2626` | Escala térmica mapa/badges: $> 30^\circ\text{C}$ |

### 2.2 Escala Tipográfica y Espaciado
- **Fuente de Títulos y KPIs (`--font-display`):** `'Outfit', 'Inter', system-ui, sans-serif` (Pesos `600`, `700`).
- **Fuente de Interfaz y Lectura (`--font-sans`):** `'Inter', system-ui, sans-serif` (Pesos `400`, `500`, `600`).
- **Fuente Monoespaciada / Datos (`--font-mono`):** `'JetBrains Mono', monospace` con `font-variant-numeric: tabular-nums` obligatorio en cifras de KPIs, coordenadas, deltas IA vs. OWM y celdas del Atlas de 168 ciudades.
- **Radios:** `--radius-sm: 6px`, `--radius-md: 10px`, `--radius-lg: 14px`.

---

## 3. Arquitectura de Información y Presupuesto *Above-the-Fold*

### 3.1 Shell Visual Datalaria (Cabecera Compacta `<= 64px`)
1. **Izquierda:** Enlace de retorno `← Datalaria` (`/es/apps/` o `/en/apps/` según idioma activo) + Logo e identidad **`Weather Intelligence v2.0`** con badge de estado en vivo (`🟢 168 Estaciones · +375 Días`).
2. **Centro (Conmutador Segmentado de las 3 Vistas):**
   - `🌍 Observatorio` (`?view=observatory`)
   - `🤖 Laboratorio ML (IA vs OWM)` (`?view=arena`)
   - `🏆 Atlas Global (168)` (`?view=atlas`)
3. **Derecha:** Enlace a la **Ficha Técnica** (`/es/apps/weather/` | `/en/apps/weather/`), enlace a la **Serie de Artículos**, botón `📥 Exportar CSV` y conmutadores `ES | EN` y `🌙 | ☀️`.

### 3.2 Franja de Pulso Global & Presets en 1 Clic (`height <= 56px`)
Debajo de la cabecera se sitúa una barra compacta en dos bloques:
- **Izquierda (1-Click Presets):**
  1. `🇪🇸 Capitales ES` (`Madrid,ES`, `Barcelona,ES`, `Bilbao,ES`, `Sevilla,ES`, `León,ES`)
  2. `🌍 Hubs Globales` (`Madrid,ES`, `London,GB`, `New York,US`, `Tokyo,JP`, `Singapore,SG`)
  3. `🔥❄️ Extremos Hoy` (Selecciona automáticamente las 2 ciudades más cálidas y las 2 más frías del día desde `global_summary.json`)
  4. `🤖 Duelo IA` (Selecciona las ciudades con mayor historial y contraste IA vs. OWM)
  5. `🏃‍♂️ Top Confort Outdoor` (Selecciona las ciudades con mayor `comfort_index` hoy)
- **Derecha (Ticker de Extremos Planetarios en Vivo):** Píldoras clicables con récord cálido, récord frío, máxima anomalía $\Delta_{30\text{d}}$ y mejor confort del planeta hoy.

### 3.3 Layout *Above-the-Fold* en Vista 1 (`Observatorio`)
En lugar de apilar un bloque gigante de controles y un mapa de 450px que oculta los datos:
- **Barra de Filtros Unificada en 1 Fila:** Selector múltiple `Choices.js` (hasta 5 ciudades) + Selector de **7 Métricas** (`Temp`, `Sensación`, `Humedad`, `Viento`, `Nubes`, `Lluvia`, `Visibilidad`) + Rango temporal (**`30D` activo por defecto** en lugar de `Todo`, más `7D`, `90D`, `1A`, `Todo`, `Personalizado`) + Franja horaria (`Todas`, `06h`, `14h`, `22h`).
- **Grid Superior de 2 Columnas en Escritorio (`1440px`):**
  - **Columna Izquierda (45% ancho, `height: 360px`):** Mapa Geoespacial Leaflet con **Selector de Capa Visual** (`Temperatura` · `Viento` · `Humedad` · `Confort 0-100` · `Anomalía 30d`).
  - **Columna Derecha (55% ancho):** **Super-Cards Comparativas** de las ciudades activas con Temperatura actual, Sensación, **Badge de Confort Outdoor (`0..100`)**, Anomalía $\Delta_{30\text{d}}$, Sparkline de 7 días, Pronóstico OWM 5D y **Comparativa IA Mañana (con badge de MAE/$R^2$)**.
- **Sección Inferior de Gráficos Analíticos:**
  1. **Evolución Histórica + Proyección OWM & IA** (Chart.js interactivo).
  2. **Amplitud Térmica Diaria (`Max - Min`) & Matriz Estacional Mensual (12 meses)** para explotar el año completo de datos.

### 3.4 Diseño de la Vista 2 (`🤖 Laboratorio ML: IA vs. OpenWeatherMap`)
- **KPIs del Motor Cuantitativo:** Ciudades entrenadas (`168`), Horizonte medio (`377 días`), MAE medio global (°C), $R^2$ medio global y explicación visual de la **Transformación Armónica de Fourier ($\sin/\cos$)** frente a la regresión lineal clásica.
- **Tabla Comparativa *Model Arena* de las Ciudades Seleccionadas (o Top 20):**
  - Columnas con `tabular-nums`: Ciudad, Días Entrenados, Predicción IA Mañana (Máx / Mín / Media), Pronóstico OWM Mañana, $\Delta\text{ (IA - OWM)}$, $R^2$ del Modelo, Error Medio $\text{MAE}_{30\text{d}}$ y **Pesos de Variables Explicativas** (barras horizontales mostrando el peso de `temp_lag1`, `estacionalidad Fourier`, `humedad_lag1`, `rango_diurno`).

### 3.5 Diseño de la Vista 3 (`🏆 Atlas & Rankings Globales — 168 Ciudades`)
- **Controles del Atlas:** Buscador instantáneo por texto + Filtros rápidos por región (`Todas (168)`, `🇪🇸 España (56)`, `🇪🇺 Europa (47)`, `🌏 Asia (25)`, `🌎 América (23)`, `🌍 África (13)`, `🇦🇺 Oceanía (4)`) + Ordenación por columna.
- **Tabla Ejecutiva de Alta Densidad:**
  - Columnas: `#`, `Ciudad`, `Región`, `Temp Actual`, `Sensación`, `Anomalía 30d (Δ°C)`, `Récord Min/Max Anual`, `Humedad / Viento`, `Confort Outdoor (0-100)`, `Acción (+ Comparar)`.
  - Al hacer clic en `+ Comparar`, añade la ciudad al selector y conmuta o actualiza el Observatorio.

### 3.6 Bloque de Conversión PLG y Exportación
- Al pie del Cockpit se incluye un banner ejecutivo alineado con el resto de Flagships de Datalaria:
  - **Acción 1 (Valor Inmediato Gratis):** Botón `📥 Descargar CSV/JSON Comparativo` de las ciudades seleccionadas.
  - **Acción 2 (Ecosistema & Monetización):** Enlace directo a la **Ficha Técnica y Arquitectura (`/es/apps/weather/` | `/en/apps/weather/`)** y al **Catálogo de Kits Cuantitativos y Datalaria Helix (`/es/recursos/` | `/en/resources/`)** con trazabilidad GA4.

---

## 4. Matriz de Estados de Interfaz (Cero Pantallas Muertas)

| Vista / Componente | Estado Vacío (*Empty State*) | Estado de Carga (*Loading*) | Estado de Error (*Graceful Fallback*) | Estado Poblado (*Ideal*) |
| :--- | :--- | :--- | :--- | :--- |
| **Observatorio (KPIs y Gráficos)** | Mensaje orientativo + botón `⚡ Cargar Preset Capitales ES en 1 clic` | Spinner no bloqueante con preservación de layout (`CLS < 0.1`) | Si `global_summary.json` no responde aún en el CDN, calcula en vivo las métricas desde `city_locations.json` y los CSVs descargados sin mostrar error al usuario | Bento Grid con Mapa multicapa, Super-Cards con índice de confort y gráficas en `30D` |
| **Laboratorio ML (`arena`)** | Si no hay ciudades seleccionadas, muestra el resumen global de las 168 estaciones | Indicador de cálculo de métricas | Si una ciudad tiene `< 10` días, muestra badge `En calibración (N/10 días)` | Scorecard IA vs. OWM con $R^2$, MAE y barras de importancia de features |
| **Atlas Global (`atlas`)** | Si un filtro de búsqueda no arroja resultados, botón `Restablecer filtros (Ver 168 ciudades)` | Skeleton de tabla | Si `global_summary.json` no existe, construye la tabla desde `city_locations.json` + `predicciones.json` | Tabla ordenable de 168 estaciones con badges de anomalía y confort |

---

## 5. Checklist del Gate de Revisión UX/UI (Pre-QA)

- [x] **Modo Oscuro Ejecutivo por Defecto (`#0b0f17`):** Si el usuario no tiene preferencia guardada en `localStorage`, la app inicia en `dark-mode` para máxima legibilidad de datos y coherencia con Datalaria.
- [x] **Responsive en 3 Viewports (`390px`, `768px`, `1440px`):** En móvil, el Bento Grid pasa a 1 columna y las tablas disponen de `overflow-x: auto`.
- [x] **Contraste WCAG 2.2 AA y `tabular-nums`:** Contraste $\ge 4.5:1$ en ambos modos y alineación monoespaciada en todas las cifras comparativas.
- [x] **Sincronización Idiomática URL (`?lang=es|en`):** Prioridad de detección: 1º parámetro URL `?lang=`, 2º `document.referrer` (`/en/` $\rightarrow$ `en`), 3º `localStorage`, 4º `es`.
- [x] **Telemetría GA4 (`gtag`):** Emisión de eventos en selección de presets, cambio de vista, comparación de ciudades, exportación de datos y clic en CTAs.

---

## 6. Arquitectura Visual v3.0: Focus Mode y Divulgación Progresiva

### 6.1 Principio Rector: "Menos Botones, Más Respuestas"
La versión `v3.0` erradica la saturación visual mediante **divulgación progresiva en 3 niveles**:
1. **Nivel 1 — Respuesta Inmediata (Tarjetas de Respuesta):** El usuario obtiene al instante la respuesta a las 3 preguntas clave: "¿Qué tiempo hace hoy?", "¿Es normal para esta época?", y "¿Es buen momento para salir?".
2. **Nivel 2 — Profundización Bajo Demanda (Acordeones `<details>`):** Las gráficas analíticas (Evolución temporal, Amplitud térmica diurna, Matriz estacional de 12 meses y Detalle del modelo IA) se presentan colapsadas por defecto, instanciando los gráficos de Chart.js de forma perezosa al abrir cada bloque.
3. **Nivel 3 — Puerta de Suficiencia (`INV-WEATHER-8`):** Si una estación carece de histórico suficiente (ej. $<7\text{ días}$ o $<2\text{ meses}$), el acordeón se deshabilita con un mensaje explicativo y un medidor de calibración, evitando taxativamente lienzos en blanco o ejes vacíos.

### 6.2 Cabecera de Alta Densidad Simplificada (`<= 4` Grupos de Controles)
La barra superior compacta (`height <= 64px`) se simplifica a un máximo de 4 agrupaciones:
1. **Identidad & Retorno:** Enlace `← Datalaria` + Título `Weather Intelligence v3.0` + Badge de estado/frescura (`INV-WEATHER-7`).
2. **Conmutador de Vistas:** `🌍 Observatorio`, `🤖 Laboratorio ML`, `🏆 Atlas 168`.
3. **Barra de Presets:** Píldoras de 1 clic con desplazamiento horizontal suave (`overflow-x: auto`, `scrollbar-width: none`).
4. **Menú de Acciones Secundarias (`⋯`):** Botón accesible que despliega un menú contextual con:
   - `📥 Exportar CSV` y `📥 Exportar JSON`.
   - Selector idiomático `ES | EN`.
   - Conmutador de tema `🌙 | ☀️`.
   - `📲 Instalar Aplicación` (acción PWA visible cuando está disponible).
   - Enlaces directos a Ficha Técnica y Serie Editorial.

### 6.3 Tarjeta Respuesta de Ciudad (*The Answer Card*)
Cada ciudad activa en el Observatorio (máximo 5) cuenta con una tarjeta ejecutiva que resume:
- Temperatura actual en gran formato (`36px bold`, `tabular-nums`) y sensación térmica.
- **Badge de Anomalía Climática:** Comparativa contra la normal histórica del mes (`derived/climatology.json`):
  - `🔺 +X.X °C sobre lo normal` (Rojo cálido si $> +1.5^\circ\text{C}$).
  - `🔻 -X.X °C bajo lo normal` (Azul frío si $< -1.5^\circ\text{C}$).
  - `≈ En la media histórica` (Verde suave si está en $\pm 1.5^\circ\text{C}$).
- **Píldora de Confort Outdoor (0..100):** Etiqueta semántica (`Óptimo`, `Favorable`, `Desfavorable`) calculada matemáticamente.
- **Mini-Sparkline de 3 Días:** Proyección compacta a 72 horas comparando IA vs. OWM.
- **Frase Sintética i18n:** Mensaje generado mediante plantillas deterministas sin LLM (ej.: *"Más cálido de lo habitual para noviembre · Buenas condiciones para actividad exterior"*).

### 6.4 Acordeones "🔍 Profundizar" y Puerta de Suficiencia (`INV-WEATHER-8`)
- `<details id="accordion-evolution">`: Serie temporal de 7 métricas con Chart.js instanciado al abrir.
- `<details id="accordion-amplitude">`: Amplitud térmica diaria (`max - min` de las 3 lecturas diarias). Requiere $\ge 7\text{ días}$ con lecturas múltiples.
- `<details id="accordion-seasonality">`: Matriz mensual de 12 meses. Requiere $\ge 2\text{ meses}$ con datos válidos.
- `<details id="accordion-ai">`: Scorecard y pesos de variables del modelo Fourier Ridge.
- Estado persistente en URL mediante `?open=evolution,seasonality`.

### 6.5 Experiencia Móvil (`<= 768px`) y PWA
- **Barra Inferior de 4 Pestañas Táctiles:** Pestañas fijas en el pie con altura de toque $\ge 44\text{px}$: `Hoy` (Observatorio 1 ciudad), `Comparar` (Observatorio multiciudad), `Ranking` (Atlas 168), `IA` (Model Arena).
- **Toast No Intrusivo de Instalación PWA:** Notificación emergente discreta a partir de la 2ª visita (`localStorage.weather_visits >= 2`), respetando si el usuario la descarta. Guía paso a paso para iOS Safari integrada en el menú `⋯`.
- **Modo Offline:** Banner flotante superior discreto en caso de pérdida de conexión: *"Sin conexión · Mostrando datos guardados de hace X h"*, sin bloquear la navegación ni emitir alertas modales intrusivas.
