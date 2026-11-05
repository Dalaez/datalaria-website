/**
 * apps/conversor/engine.js
 * Motor Matemático Determinista y Formateador Numérico
 * Datalaria Helix — Strict SI & Metrology Engine
 */

export const SPEED_OF_LIGHT = 299792458; // m/s (CODATA Exact)

export const WAVELENGTH_FACTORS = {
  m: 1,
  km: 1000,
  cm: 0.01,
  mm: 0.001,
  um: 1e-6,
  nm: 1e-9
};

export const FREQ_FACTORS = {
  hz: 1,
  khz: 1e3,
  mhz: 1e6,
  ghz: 1e9,
  thz: 1e12
};

/**
 * Conversión lineal canónica
 * Invariante INV-CONV-1: convert(convert(x, A, B), B, A) == x
 */
export function convertLinear(value, fromUnitKey, toUnitKey, unitsMap) {
  if (value === null || value === undefined || isNaN(value)) return NaN;
  const fromUnit = unitsMap[fromUnitKey];
  const toUnit = unitsMap[toUnitKey];
  if (!fromUnit || !toUnit) {
    throw new Error(`Unidades desconocidas: ${fromUnitKey} -> ${toUnitKey}`);
  }
  const baseValue = Number(value) * fromUnit.factor;
  return baseValue / toUnit.factor;
}

/**
 * Conversión de temperatura (No lineal)
 */
export function convertTemperature(value, fromKey, toKey) {
  if (value === null || value === undefined || isNaN(value)) return NaN;
  const val = Number(value);
  if (fromKey === toKey) return val;

  // 1. A Kelvin
  let kelvin;
  switch (fromKey) {
    case 'c': kelvin = val + 273.15; break;
    case 'f': kelvin = (val - 32) * (5 / 9) + 273.15; break;
    case 'k': kelvin = val; break;
    case 'r': kelvin = val * (5 / 9); break;
    default: throw new Error(`Escala desconocida: ${fromKey}`);
  }

  // 2. De Kelvin a Destino
  switch (toKey) {
    case 'c': return kelvin - 273.15;
    case 'f': return (kelvin - 273.15) * (9 / 5) + 32;
    case 'k': return kelvin;
    case 'r': return kelvin * (9 / 5);
    default: throw new Error(`Escala desconocida: ${toKey}`);
  }
}

/**
 * Conversión de potencia logarítmica RF (dBm ⇔ W / mW / kW)
 */
export function convertRfPower(value, fromKey, toKey) {
  if (value === null || value === undefined || isNaN(value)) return NaN;
  const val = Number(value);
  if (fromKey === toKey) return val;

  // 1. A milivatios (mW)
  let mw;
  switch (fromKey) {
    case 'dbm':
      mw = Math.pow(10, val / 10);
      break;
    case 'mw':
      mw = val;
      break;
    case 'w':
      mw = val * 1000;
      break;
    case 'kw':
      mw = val * 1e6;
      break;
    default:
      throw new Error(`Unidad RF desconocida: ${fromKey}`);
  }

  // 2. De milivatios a Destino
  switch (toKey) {
    case 'dbm':
      if (mw <= 0) return -Infinity;
      return 10 * Math.log10(mw);
    case 'mw':
      return mw;
    case 'w':
      return mw / 1000;
    case 'kw':
      return mw / 1e6;
    default:
      throw new Error(`Unidad RF desconocida: ${toKey}`);
  }
}

/**
 * Conversión Frecuencia ⇔ Longitud de Onda electromagnética en el vacío (λ = c / f)
 * Bidireccional
 */
export function convertRfWavFreq(value, mode, fromUnit, toUnit) {
  if (value === null || value === undefined || isNaN(value)) return NaN;
  const val = Number(value);
  if (val <= 0) return NaN;

  if (mode === 'freq_to_wav') {
    // fromUnit es frecuencia (hz, mhz..), toUnit es longitud (m, cm, nm..)
    const freqFactor = FREQ_FACTORS[fromUnit] || 1;
    const wavFactor = WAVELENGTH_FACTORS[toUnit] || 1;
    const fHz = val * freqFactor;
    if (fHz === 0) return Infinity;
    const lambdaMeters = SPEED_OF_LIGHT / fHz;
    return lambdaMeters / wavFactor;
  } else if (mode === 'wav_to_freq') {
    // fromUnit es longitud (m, cm, nm..), toUnit es frecuencia (hz, mhz..)
    const wavFactor = WAVELENGTH_FACTORS[fromUnit] || 1;
    const freqFactor = FREQ_FACTORS[toUnit] || 1;
    const lambdaMeters = val * wavFactor;
    if (lambdaMeters === 0) return Infinity;
    const fHz = SPEED_OF_LIGHT / lambdaMeters;
    return fHz / freqFactor;
  }

  throw new Error(`Modo RF λ-f inválido: ${mode}`);
}

/**
 * Parser numérico robusto
 * Maneja notación científica (1e-4), formatos US (1,234.56), EU (1.234,56),
 * números negativos y extracción limpia de cantidades con unidades ('15.4 bar').
 */
export function parseRobustNumber(str, forceFormat = 'auto') {
  if (!str) return NaN;
  const trimmed = String(str).trim();
  if (!trimmed) return NaN;

  // Extracción del bloque numérico principal (respetando signos y exponente e/E)
  const match = trimmed.match(/[-+]?(?:[\d.,]+(?:[eE][-+]?\d+)?|\d+)/);
  if (!match) return NaN;

  let numStr = match[0];
  const hasDot = numStr.includes('.');
  const hasComma = numStr.includes(',');

  // Separar exponente si existe (ej. 1.23e-4)
  let exponent = '';
  const eIndex = numStr.search(/[eE]/);
  if (eIndex !== -1) {
    exponent = numStr.slice(eIndex);
    numStr = numStr.slice(0, eIndex);
  }

  let finalNumber = NaN;

  if (hasDot && hasComma) {
    // Ambos separadores presentes: el último determina el decimal
    const lastDot = numStr.lastIndexOf('.');
    const lastComma = numStr.lastIndexOf(',');
    if (lastDot > lastComma) {
      // Formato US: 1,234.56 -> comas son miles, punto es decimal
      finalNumber = parseFloat(numStr.replace(/,/g, ''));
    } else {
      // Formato EU: 1.234,56 -> puntos son miles, coma es decimal
      finalNumber = parseFloat(numStr.replace(/\./g, '').replace(',', '.'));
    }
  } else if (hasDot) {
    const parts = numStr.split('.');
    if (forceFormat === 'eu' && parts.length === 2 && parts[1].length === 3 && parts[0].length >= 1) {
      // Usuario forzó EU y es un único punto con 3 dígitos (ej. 1.234 en miles)
      finalNumber = parseFloat(numStr.replace(/\./g, ''));
    } else if (parts.length > 2) {
      // Múltiples puntos: deben ser miles (ej. 1.000.000)
      finalNumber = parseFloat(parts.slice(0, -1).join('') + '.' + parts[parts.length - 1]);
    } else {
      finalNumber = parseFloat(numStr);
    }
  } else if (hasComma) {
    const parts = numStr.split(',');
    if (parts.length > 2) {
      // Múltiples comas: miles US (ej. 1,000,000)
      finalNumber = parseFloat(numStr.replace(/,/g, ''));
    } else if (forceFormat === 'us' && parts[1] && parts[1].length === 3) {
      // Forzado US y 3 dígitos después de coma -> miles
      finalNumber = parseFloat(numStr.replace(/,/g, ''));
    } else {
      // Caso estándar: coma decimal (ej. 1,234 en español o 0,025)
      // FIX del bug anterior donde 1,234 se convertía forzosamente a 1234
      finalNumber = parseFloat(numStr.replace(',', '.'));
    }
  } else {
    finalNumber = parseFloat(numStr);
  }

  if (isNaN(finalNumber)) return NaN;
  if (exponent) {
    return parseFloat(`${finalNumber}${exponent}`);
  }
  return finalNumber;
}

/**
 * Formateador de números científicos y comerciales de alta fidelidad
 * Evita el doble truncamiento de toLocaleString()
 */
export function formatEngineeredNumber(num, precision = 'auto', targetFormat = 'es') {
  if (num === null || num === undefined || isNaN(num)) return '--';
  if (!isFinite(num)) return num > 0 ? '∞' : '-∞';
  if (num === 0) return '0';

  const thousandsSep = targetFormat === 'es' || targetFormat === 'eu' ? '.' : ',';
  const decimalSep = targetFormat === 'es' || targetFormat === 'eu' ? ',' : '.';

  let formattedStr = '';
  const absVal = Math.abs(num);

  if (precision === 'sci' || (precision === 'auto' && (absVal < 1e-4 || absVal >= 1e9))) {
    // Formato científico elegante
    const expStr = num.toExponential(4);
    const [mantissa, exp] = expStr.split('e');
    const localizedMantissa = mantissa.replace('.', decimalSep);
    return `${localizedMantissa} × 10${formatSuperscript(exp)}`;
  }

  if (precision === 'auto') {
    // Si es un entero o casi entero
    if (Number.isInteger(num)) {
      formattedStr = String(num);
    } else {
      // Hasta 6 cifras significativas sin ceros superfluos
      const str = num.toPrecision(6);
      formattedStr = String(parseFloat(str));
    }
  } else {
    const decimals = parseInt(precision, 10);
    if (!isNaN(decimals) && decimals >= 0 && decimals <= 12) {
      formattedStr = num.toFixed(decimals);
    } else {
      formattedStr = String(num);
    }
  }

  // Inyectar separadores de miles y decimales
  const [intPart, decPart] = formattedStr.split('.');
  const formattedInt = intPart.replace(/\B(?=(\d{3})+(?!\d))/g, thousandsSep);

  if (decPart !== undefined && decPart !== '') {
    return `${formattedInt}${decimalSep}${decPart}`;
  }
  return formattedInt;
}

function formatSuperscript(expString) {
  const supers = {
    '-': '⁻',
    '+': '⁺',
    '0': '⁰',
    '1': '¹',
    '2': '²',
    '3': '³',
    '4': '⁴',
    '5': '⁵',
    '6': '⁶',
    '7': '⁷',
    '8': '⁸',
    '9': '⁹'
  };
  return expString.replace(/[-+0-9]/g, char => supers[char] || char);
}

/**
 * Procesador en lote (Batch Scratchpad)
 */
export function processBatchText(rawText, options = {}) {
  const {
    targetFormat = 'eu', // 'eu' o 'us'
    convertUnits = false,
    unitCategory = null,
    fromUnit = null,
    toUnit = null,
    precision = 'auto',
    categoriesCatalog = null
  } = options;

  if (!rawText || !rawText.trim()) {
    return { output: '', count: 0, errors: 0 };
  }

  const lines = rawText.split(/\r?\n/);
  let processedCount = 0;
  let errorCount = 0;

  const resultLines = lines.map((line, idx) => {
    if (!line.trim()) return '';

    const parsed = parseRobustNumber(line);
    if (isNaN(parsed)) {
      errorCount++;
      return `[Línea ${idx + 1}: Entrada inválida '${line.trim()}']`;
    }

    let finalVal = parsed;

    if (convertUnits && unitCategory && fromUnit && toUnit && categoriesCatalog) {
      try {
        if (unitCategory === 'temperature') {
          finalVal = convertTemperature(parsed, fromUnit, toUnit);
        } else if (unitCategory === 'rf_power') {
          finalVal = convertRfPower(parsed, fromUnit, toUnit);
        } else {
          // Linear conversion
          const cat = categoriesCatalog[unitCategory];
          if (cat && cat.units) {
            finalVal = convertLinear(parsed, fromUnit, toUnit, cat.units);
          }
        }
      } catch {
        errorCount++;
        return `[Línea ${idx + 1}: Error de conversión]`;
      }
    }

    processedCount++;
    return formatEngineeredNumber(finalVal, precision, targetFormat);
  });

  return {
    output: resultLines.join('\n'),
    count: processedCount,
    errors: errorCount
  };
}
