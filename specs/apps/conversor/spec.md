# SPEC-APP-CONVERSOR: Conversor de Unidades ("Engineering Workbench v2.0")

> **Identificador:** `SPEC-APP-CONVERSOR`  
> **Versión:** `v2.0.0` (Estado: `active`)  
> **Fecha:** `2026-11-04`  
> **Clasificación:** Tier `lab` | Scientific & Engineering Toolkit  
> **Ruta Canónica:** `https://datalaria.com/apps/conversor/`  
> **Ficha Técnica:** `https://datalaria.com/es/apps/conversor/` (EN: `/en/apps/conversor/`)  
> **Especificación de Diseño:** [`specs/apps/conversor/design.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/apps/conversor/design.md)

---

## 1. RESUMEN EJECUTIVO Y PROPÓSITO

El **Conversor Universal Pro ("Engineering Workbench v2.0")** es una suite científica y técnica de alta precisión para conversión de magnitudes físicas, metrología de ingeniería, constantes fundamentales y formateo de datos numéricos internacionales. 

Diseñado bajo la **Constitución SDD v1.1.0** para resolver las fricciones de herramientas genéricas con publicidad, el workbench opera enteramente en el cliente (100% offline y de carga instantánea) bajo una arquitectura **Single-Source-of-Truth** que erradica la deuda técnica de archivos HTML duplicados.

### 1.1 Objetivos Clave de la Versión 2.0.0:
1. **Rigor Metrológico SI / CODATA:** Todas las conversiones se normalizan respecto a unidades canónicas del Sistema Internacional (SI) o definiciones oficiales CODATA 2022/NIST, asegurando reversibilidad numérica exacta ($\epsilon \le 10^{-9}$).
2. **Cobertura Completa sin Brechas de Contrato (*Zero Contract Drift*):** Incorporación completa de potencia logarítmica RF (`dBm ⇔ W / mW`), longitud de onda y frecuencia electromagnética bidireccional ($\lambda = c / f$), energía térmica británica (`BTU`), unidades de almacenamiento binarias IEC (`KiB, MiB, GiB, TiB`) frente a decimales SI (`kB, MB, GB, TB`), y presión técnica e hidráulica (`bar, psi, Pa, atm, torr`).
3. **Batch Scratchpad & Formateador Masivo Avanzado:** Procesamiento multilínea de columnas de números pegadas desde hojas de cálculo (Excel, Google Sheets), permitiendo alternar formato decimal/miles (`US ⇔ EU`) y/o convertir unidades físicas de cada fila con exportación en 1 clic.
4. **Shell Datalaria, Ergonomía y Deep-Linking:** Cabecera institucional compacta (`← Datalaria`, selector `ES | EN`, botón `Kits B2B`), atajos de teclado (`⇄ Invertir`, `Copiar`), selector de precisión/notación científica, y persistencia de estado en la URL (`URLSearchParams`) para compartir cálculos reproducibles.
5. **Cero Dependencias de Red Externas:** Eliminación del CDN de Tailwind; estilizado mediante Design Tokens CSS nativos ultraligeros.

---

## 2. ARQUITECTURA DEL SISTEMA

```mermaid
flowchart TD
    subgraph CoreEngine ["apps/conversor/ (Motor Centralizado Single Source of Truth)"]
        CATALOG["Catálogo Canónico de Unidades & Factores SI (catalog.json)"]
        MATH["Motor Matemático Determinista & Fórmulas No Lineales (engine.js)"]
        PARSER["Parser & Formateador Numérico Robusto (US ⇔ EU)"]
        CONSTANTS["Constantes Universales CODATA (c, g0, h, kB, NA, ε0, R, e)"]
        I18N["Diccionario Bilingüe Unificado (ES / EN)"]
    end

    subgraph UI ["Capa de Presentación Web (Vanilla JS + CSS Tokens)"]
        SHELL["Shell Visual Datalaria (Header <= 64px, ES/EN, Post Link, B2B CTA)"]
        TABS["Selector de Disciplinas (6 Físicas + 1 Batch Scratchpad)"]
        OMNI["Omni-Matrix Multi-Escala & Inspector de Fórmula Viva"]
        URLSYNC["Deep-Linking Bidireccional (URLSearchParams)"]
    end

    subgraph StaticDeploy ["static/apps/conversor/ (Distribución Web Hugo)"]
        INDEX["index.html (Workbench v2.0 Unificado SPA)"]
        SHIMS_ES["es/*.html (7 Shims de Redirección Retrocompatible)"]
        SHIMS_EN["en/*_en.html + index.html (7 Shims de Redirección Retrocompatible)"]
    end

    CATALOG --> MATH
    MATH --> UI
    PARSER --> UI
    CONSTANTS --> UI
    I18N --> UI
    UI --> INDEX
    SHIMS_ES -. "301 / Meta Refresh" .-> INDEX
    SHIMS_EN -. "301 / Meta Refresh" .-> INDEX
```

### Componentes Principales:
- **`catalog.js`:** Definición declarativa de las 6 categorías físicas, sus magnitudes, símbolos, factores SI exactos y nombres bilingües.
- **`engine.js`:** Funciones puras de conversión lineal, conversión no lineal (Temperatura, dBm, $\lambda$), cálculo de Omni-Matrix y formateador numérico con detección heurística mejorada.
- **`app.js` / `index.html`:** Interfaz reactiva en Vanilla JS que gobierna eventos, atajos de teclado, sincronización de parámetros de URL (`?lang=es|en&cat=...&mag=...&val=...&from=...&to=...`) y almacenamiento de historial en `localStorage`.
- **Shims de Retrocompatibilidad:** Pequeños archivos HTML estáticos en las rutas históricas de `/es/` y `/en/` que redirigen instantáneamente a la URL canónica preservando los parámetros de categoría e idioma, garantizando **cero enlaces 404** para el portal y el SEO.

---

## 3. CATÁLOGO DE MAGNITUDES Y METROLOGÍA SI

### 3.1 Magnitudes y Factores Canónicos de Conversión

| Disciplina | Magnitud | Unidad Base SI | Unidades Soportadas |
| :--- | :--- | :--- | :--- |
| **Dimensión** | Longitud | Metro ($m$) | $m, km, cm, mm, \mu m, nm, mi, yd, ft, in, NM$ (millas náuticas) |
| | Área | Metro cuadrado ($m^2$) | $m^2, km^2, ha, mi^2, ac, ft^2, in^2$ |
| | Volumen | Metro cúbico ($m^3$) | $m^3, l, ml, cm^3, gal\text{ (US)}, qt\text{ (US)}, pt\text{ (US)}, cup\text{ (US)}, fl\text{ }oz\text{ (US)}$ |
| **Energía** | Energía | Julio ($J$) | $J, kJ, cal, kcal, Wh, kWh, BTU\text{ (IT: }1055.056\text{ J)}, eV, ft\cdot lbf$ |
| | Potencia | Vatio ($W$) | $W, kW, MW, hp\text{ (métrica: 735.49875 W)}, hp\text{ (mecánica: 745.69987 W)}, BTU/h$ |
| | Temperatura | Kelvin ($K$) | Celsius ($^\circ C$), Fahrenheit ($^\circ F$), Kelvin ($K$), Rankine ($^\circ R$) |
| **Tiempo** | Tiempo | Segundo ($s$) | $s, ms, \mu s, ns, min, h, d, w, a\text{ (año estándar 365 d)}, a_j\text{ (año juliano 365.25 d)}$ |
| **Mecánica** | Masa | Kilogramo ($kg$) | $kg, g, mg, \mu g, lb, oz, t\text{ (métrica)}, ton\text{ (US corta)}$ |
| | Fuerza | Newton ($N$) | $N, kN, MN, lbf, dyn, kgf$ |
| | Presión | Pascal ($Pa$) | $Pa, kPa, MPa, bar, mbar, psi, atm, torr\text{ / }mmHg$ |
| **Informática** | Almacenamiento (Decimal SI) | Byte ($B$) | $B, kB\text{ (10}^3\text{)}, MB\text{ (10}^6\text{)}, GB\text{ (10}^9\text{)}, TB\text{ (10}^{12}\text{)}, PB$ |
| | Almacenamiento (Binario IEC) | Byte ($B$) | $B, KiB\text{ (2}^{10}\text{)}, MiB\text{ (2}^{20}\text{)}, GiB\text{ (2}^{30}\text{)}, TiB\text{ (2}^{40}\text{)}, PiB$ |
| | Ancho de Banda | Bit/s ($bps$) | $bps, kbps, Mbps, Gbps, Tbps$ |
| **Radiofrecuencia** | Frecuencia | Hercio ($Hz$) | $Hz, kHz, MHz, GHz, THz$ |
| | Frecuencia ⇔ Longitud Onda | Metros ($m$) | Bidireccional: $\lambda = c / f \iff f = c / \lambda$ ($c = 299\,792\,458\text{ m/s}$) |
| | Potencia Logarítmica | Milivatios ($mW$) | $dBm \iff W, mW, kW$ ($P_{dBm} = 10 \log_{10}(P_{mW})$) |

### 3.2 Constantes Físicas Universales (CODATA 2022)
1. **Velocidad de la luz en el vacío ($c$):** $299\,792\,458\text{ m/s}$ (Exacta).
2. **Aceleración estándar de la gravedad ($g_0$):** $9.80665\text{ m/s}^2$ (Exacta).
3. **Constante de Planck ($h$):** $6.62607015 \times 10^{-34}\text{ J}\cdot\text{s}$ (Exacta).
4. **Constante de Boltzmann ($k_B$):** $1.380649 \times 10^{-23}\text{ J/K}$ (Exacta).
5. **Número de Avogadro ($N_A$):** $6.02214076 \times 10^{23}\text{ mol}^{-1}$ (Exacto).
6. **Permitividad del vacío ($\varepsilon_0$):** $8.8541878128 \times 10^{-12}\text{ F/m}$.
7. **Constante universal de los gases ($R$):** $8.314462618\text{ J/(mol}\cdot\text{K)}$.
8. **Carga elemental ($e$):** $1.602176634 \times 10^{-19}\text{ C}$ (Exacta).

---

## 4. INVARIANTES DE DOMINIO (`INV-CONV-*`)

- **`INV-CONV-1` (Reversibilidad Numérica Estricta):** Para cualquier par de unidades $(A, B)$ dentro de una misma magnitud lineal, $\text{convert}(\text{convert}(x, A, B), B, A) = x$ con error relativo $\le 10^{-9}$.
- **`INV-CONV-2` (Completitud sin Drift):** Los módulos de Radiofrecuencia (dBm ⇔ W, λ ⇔ f bidireccional), Informática (IEC vs SI) y Energía (BTU) deben existir funcionalmente en el código y en la interfaz.
- **`INV-CONV-3` (Cero Dependencias Externas en Runtime):** Queda prohibida la carga de scripts o estilos externos vía CDN (`cdn.tailwindcss.com`, fuentes o librerías de terceros no locales/seguras).
- **`INV-CONV-4` (Retrocompatibilidad 100% de Enlaces Históricos):** Los 14 archivos HTML previos en `static/apps/conversor/es/` y `en/` se reemplazan por shims de redirección válidos que preservan la categoría en la URL (`/apps/conversor/?lang=...&cat=...`).
- **`INV-CONV-5` (Inmunidad XSS en Manipulación de Cadenas):** Ninguna entrada del usuario en el formateador de números o parámetros URL se inyecta en el DOM mediante `innerHTML`.
- **`INV-CONV-6` (Paridad Bilingüe Total):** Todo elemento textual de la interfaz, nombres de unidades y mensajes didácticos debe contar con su correspondiente traducción en el diccionario bilingüe (`es` y `en`).

---

## 5. HISTORIAL DE VERSIONES Y EVOLUCIÓN

- **`v2.0.0` (2026-11-04) — [ESTADO: ACTIVO — ENGINEERING WORKBENCH SDD]:**
  - **Refactorización Arquitectónica:** Migración a arquitectura *Single-Source-of-Truth* en `/apps/conversor/` con compilación estática y 14 shims de redirección retrocompatibles (eliminación del antipatrón de 15 HTML duplicados y corrección de la corrupción de cabecera en `en/mecanica_en.html`).
  - **Cierre de Contract Drift:** Implementación de potencia en dBm ⇔ W/mW, cálculo bidireccional $\lambda \iff f$, soporte de BTU y diferenciación estricta entre almacenamiento decimal SI y binario IEC (KiB..TiB).
  - **Resolución de Bugs Numéricos:** Corrección del truncamiento de 3 decimales provocado por `toLocaleString`, formateador de salida con precisión configurable (`Auto`, `2..8`, `Sci`) y motor de parseo robusto para separadores de miles y decimales que no corrompe entradas de 3 decimales (`1,234`).
  - **Módulo Batch Scratchpad:** Herramienta multilínea para conversión en masa de columnas pegadas desde Excel/CSV (formato de separadores y/o cambio de magnitud física en lote).
  - **Experiencia de Usuario e Integración:** Shell visual Datalaria con navegación institucional `← Datalaria`, fuentes `Outfit`/`Inter`/`JetBrains Mono` con `tabular-nums`, botones rápidos de inversión (`⇄`) y copiado (`✓`), enlaces permanentes por URL (`URLSearchParams`), barra de constantes CODATA y puente PLG no intrusivo hacia el catálogo de Kits B2B de Datalaria.
- **`v1.0.0` (2025-10-04) — [LEGACY FROZEN]:**
  - Versión multipágina original con 6 categorías aisladas en `/es/` y `/en/`.
