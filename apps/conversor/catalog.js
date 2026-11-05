/**
 * apps/conversor/catalog.js
 * Catálogo Canónico de Unidades, Factores SI y Constantes CODATA
 * Datalaria Helix — Single Source of Truth
 */

export const PHYSICAL_CONSTANTS = [
  { id: 'c', symbol: 'c', name: { es: 'Velocidad de la luz en el vacío', en: 'Speed of light in vacuum' }, value: 299792458, unit: 'm/s', exact: true },
  { id: 'g0', symbol: 'g₀', name: { es: 'Gravedad estándar terrestre', en: 'Standard gravity' }, value: 9.80665, unit: 'm/s²', exact: true },
  { id: 'h', symbol: 'h', name: { es: 'Constante de Planck', en: 'Planck constant' }, value: 6.62607015e-34, unit: 'J·s', exact: true },
  { id: 'kb', symbol: 'k_B', name: { es: 'Constante de Boltzmann', en: 'Boltzmann constant' }, value: 1.380649e-23, unit: 'J/K', exact: true },
  { id: 'na', symbol: 'N_A', name: { es: 'Número de Avogadro', en: 'Avogadro constant' }, value: 6.02214076e23, unit: 'mol⁻¹', exact: true },
  { id: 'eps0', symbol: 'ε₀', name: { es: 'Permitividad del vacío', en: 'Vacuum permittivity' }, value: 8.8541878128e-12, unit: 'F/m', exact: false },
  { id: 'r_gas', symbol: 'R', name: { es: 'Constante universal de los gases', en: 'Gas constant' }, value: 8.314462618, unit: 'J/(mol·K)', exact: true },
  { id: 'elem_charge', symbol: 'e', name: { es: 'Carga elemental', en: 'Elementary charge' }, value: 1.602176634e-19, unit: 'C', exact: true }
];

export const CATEGORIES = {
  dimension: {
    id: 'dimension',
    icon: '📐',
    title: { es: 'Dimensión', en: 'Dimension' },
    magnitudes: {
      length: {
        id: 'length',
        title: { es: 'Longitud', en: 'Length' },
        baseUnit: 'm',
        units: {
          m: { id: 'm', symbol: 'm', factor: 1, name: { es: 'Metros (m)', en: 'Meters (m)' } },
          km: { id: 'km', symbol: 'km', factor: 1000, name: { es: 'Kilómetros (km)', en: 'Kilometers (km)' } },
          cm: { id: 'cm', symbol: 'cm', factor: 0.01, name: { es: 'Centímetros (cm)', en: 'Centimeters (cm)' } },
          mm: { id: 'mm', symbol: 'mm', factor: 0.001, name: { es: 'Milímetros (mm)', en: 'Millimeters (mm)' } },
          um: { id: 'um', symbol: 'µm', factor: 1e-6, name: { es: 'Micrómetros (µm)', en: 'Micrometers (µm)' } },
          nm: { id: 'nm', symbol: 'nm', factor: 1e-9, name: { es: 'Nanómetros (nm)', en: 'Nanometers (nm)' } },
          mi: { id: 'mi', symbol: 'mi', factor: 1609.344, name: { es: 'Millas (mi)', en: 'Miles (mi)' } },
          yd: { id: 'yd', symbol: 'yd', factor: 0.9144, name: { es: 'Yardas (yd)', en: 'Yards (yd)' } },
          ft: { id: 'ft', symbol: 'ft', factor: 0.3048, name: { es: 'Pies (ft)', en: 'Feet (ft)' } },
          in: { id: 'in', symbol: 'in', factor: 0.0254, name: { es: 'Pulgadas (in)', en: 'Inches (in)' } },
          nmi: { id: 'nmi', symbol: 'NM', factor: 1852, name: { es: 'Millas náuticas (NM)', en: 'Nautical Miles (NM)' } }
        },
        defaultFrom: 'm',
        defaultTo: 'ft'
      },
      area: {
        id: 'area',
        title: { es: 'Área', en: 'Area' },
        baseUnit: 'm2',
        units: {
          m2: { id: 'm2', symbol: 'm²', factor: 1, name: { es: 'Metros² (m²)', en: 'Square Meters (m²)' } },
          km2: { id: 'km2', symbol: 'km²', factor: 1e6, name: { es: 'Kilómetros² (km²)', en: 'Square Kilometers (km²)' } },
          ha: { id: 'ha', symbol: 'ha', factor: 10000, name: { es: 'Hectáreas (ha)', en: 'Hectares (ha)' } },
          mi2: { id: 'mi2', symbol: 'mi²', factor: 2589988.110336, name: { es: 'Millas² (mi²)', en: 'Square Miles (mi²)' } },
          ac: { id: 'ac', symbol: 'ac', factor: 4046.8564224, name: { es: 'Acres (ac)', en: 'Acres (ac)' } },
          yd2: { id: 'yd2', symbol: 'yd²', factor: 0.83612736, name: { es: 'Yardas² (yd²)', en: 'Square Yards (yd²)' } },
          ft2: { id: 'ft2', symbol: 'ft²', factor: 0.09290304, name: { es: 'Pies² (ft²)', en: 'Square Feet (ft²)' } },
          in2: { id: 'in2', symbol: 'in²', factor: 0.00064516, name: { es: 'Pulgadas² (in²)', en: 'Square Inches (in²)' } }
        },
        defaultFrom: 'm2',
        defaultTo: 'ft2'
      },
      volume: {
        id: 'volume',
        title: { es: 'Volumen', en: 'Volume' },
        baseUnit: 'm3',
        units: {
          m3: { id: 'm3', symbol: 'm³', factor: 1, name: { es: 'Metros³ (m³)', en: 'Cubic Meters (m³)' } },
          l: { id: 'l', symbol: 'L', factor: 0.001, name: { es: 'Litros (L)', en: 'Liters (L)' } },
          ml: { id: 'ml', symbol: 'mL', factor: 1e-6, name: { es: 'Mililitros (mL)', en: 'Milliliters (mL)' } },
          cm3: { id: 'cm3', symbol: 'cm³', factor: 1e-6, name: { es: 'Centímetros³ (cm³)', en: 'Cubic Centimeters (cm³)' } },
          gal_us: { id: 'gal_us', symbol: 'gal (US)', factor: 0.003785411784, name: { es: 'Galones US (gal)', en: 'Gallons US (gal)' } },
          qt_us: { id: 'qt_us', symbol: 'qt (US)', factor: 0.000946352946, name: { es: 'Cuartos US (qt)', en: 'Quarts US (qt)' } },
          pt_us: { id: 'pt_us', symbol: 'pt (US)', factor: 0.000473176473, name: { es: 'Pintas US (pt)', en: 'Pints US (pt)' } },
          cup_us: { id: 'cup_us', symbol: 'taza (US)', factor: 0.0002365882365, name: { es: 'Tazas US', en: 'Cups US' } },
          floz_us: { id: 'floz_us', symbol: 'fl oz (US)', factor: 2.95735295625e-5, name: { es: 'Onzas fluidas US (fl oz)', en: 'Fluid Ounces US (fl oz)' } }
        },
        defaultFrom: 'l',
        defaultTo: 'gal_us'
      }
    }
  },

  energia: {
    id: 'energia',
    icon: '⚡',
    title: { es: 'Energía', en: 'Energy' },
    magnitudes: {
      energy: {
        id: 'energy',
        title: { es: 'Energía', en: 'Energy' },
        baseUnit: 'j',
        units: {
          j: { id: 'j', symbol: 'J', factor: 1, name: { es: 'Julios (J)', en: 'Joules (J)' } },
          kj: { id: 'kj', symbol: 'kJ', factor: 1000, name: { es: 'Kilojulios (kJ)', en: 'Kilojoules (kJ)' } },
          mj: { id: 'mj', symbol: 'MJ', factor: 1e6, name: { es: 'Megajulios (MJ)', en: 'Megajoules (MJ)' } },
          cal: { id: 'cal', symbol: 'cal', factor: 4.184, name: { es: 'Calorías (cal)', en: 'Calories (cal)' } },
          kcal: { id: 'kcal', symbol: 'kcal', factor: 4184, name: { es: 'Kilocalorías (kcal)', en: 'Kilocalories (kcal)' } },
          wh: { id: 'wh', symbol: 'Wh', factor: 3600, name: { es: 'Vatios-hora (Wh)', en: 'Watt-hours (Wh)' } },
          kwh: { id: 'kwh', symbol: 'kWh', factor: 3.6e6, name: { es: 'Kilovatios-hora (kWh)', en: 'Kilowatt-hours (kWh)' } },
          btu: { id: 'btu', symbol: 'BTU', factor: 1055.056, name: { es: 'BTU (Tabla Internacional)', en: 'BTU (IT)' } },
          ev: { id: 'ev', symbol: 'eV', factor: 1.602176634e-19, name: { es: 'Electronvoltios (eV)', en: 'Electronvolts (eV)' } },
          ftlbf: { id: 'ftlbf', symbol: 'ft·lbf', factor: 1.3558179483314004, name: { es: 'Pies-libra fuerza (ft·lbf)', en: 'Foot-pounds force (ft·lbf)' } }
        },
        defaultFrom: 'kwh',
        defaultTo: 'btu'
      },
      power: {
        id: 'power',
        title: { es: 'Potencia', en: 'Power' },
        baseUnit: 'w',
        units: {
          w: { id: 'w', symbol: 'W', factor: 1, name: { es: 'Vatios (W)', en: 'Watts (W)' } },
          kw: { id: 'kw', symbol: 'kW', factor: 1000, name: { es: 'Kilovatios (kW)', en: 'Kilowatts (kW)' } },
          mw: { id: 'mw', symbol: 'MW', factor: 1e6, name: { es: 'Megavatios (MW)', en: 'Megawatts (MW)' } },
          hp_m: { id: 'hp_m', symbol: 'CV', factor: 735.49875, name: { es: 'Caballos de vapor (CV métrico)', en: 'Metric Horsepower (CV)' } },
          hp_mech: { id: 'hp_mech', symbol: 'HP', factor: 745.69987158227022, name: { es: 'Caballos de fuerza (HP mecánico)', en: 'Mechanical Horsepower (HP)' } },
          btu_h: { id: 'btu_h', symbol: 'BTU/h', factor: 0.29307107, name: { es: 'BTU por hora (BTU/h)', en: 'BTU per hour (BTU/h)' } }
        },
        defaultFrom: 'kw',
        defaultTo: 'hp_mech'
      },
      temperature: {
        id: 'temperature',
        title: { es: 'Temperatura', en: 'Temperature' },
        isNonLinear: true,
        baseUnit: 'k',
        units: {
          c: { id: 'c', symbol: '°C', name: { es: 'Grados Celsius (°C)', en: 'Degrees Celsius (°C)' } },
          f: { id: 'f', symbol: '°F', name: { es: 'Grados Fahrenheit (°F)', en: 'Degrees Fahrenheit (°F)' } },
          k: { id: 'k', symbol: 'K', name: { es: 'Kelvin (K)', en: 'Kelvin (K)' } },
          r: { id: 'r', symbol: '°R', name: { es: 'Rankine (°R)', en: 'Rankine (°R)' } }
        },
        defaultFrom: 'c',
        defaultTo: 'f'
      }
    }
  },

  tiempo: {
    id: 'tiempo',
    icon: '⏱️',
    title: { es: 'Tiempo', en: 'Time' },
    magnitudes: {
      time: {
        id: 'time',
        title: { es: 'Tiempo y Duración', en: 'Time & Duration' },
        baseUnit: 's',
        units: {
          s: { id: 's', symbol: 's', factor: 1, name: { es: 'Segundos (s)', en: 'Seconds (s)' } },
          ms: { id: 'ms', symbol: 'ms', factor: 0.001, name: { es: 'Milisegundos (ms)', en: 'Milliseconds (ms)' } },
          us: { id: 'us', symbol: 'µs', factor: 1e-6, name: { es: 'Microsegundos (µs)', en: 'Microseconds (µs)' } },
          ns: { id: 'ns', symbol: 'ns', factor: 1e-9, name: { es: 'Nanosegundos (ns)', en: 'Nanoseconds (ns)' } },
          min: { id: 'min', symbol: 'min', factor: 60, name: { es: 'Minutos (min)', en: 'Minutes (min)' } },
          h: { id: 'h', symbol: 'h', factor: 3600, name: { es: 'Horas (h)', en: 'Hours (h)' } },
          d: { id: 'd', symbol: 'd', factor: 86400, name: { es: 'Días (d)', en: 'Days (d)' } },
          w: { id: 'w', symbol: 'sem', factor: 604800, name: { es: 'Semanas', en: 'Weeks' } },
          y: { id: 'y', symbol: 'a', factor: 31536000, name: { es: 'Años estándar (365 d)', en: 'Standard Years (365 d)' } },
          yj: { id: 'yj', symbol: 'a_jul', factor: 31557600, name: { es: 'Años julianos (365.25 d)', en: 'Julian Years (365.25 d)' } }
        },
        defaultFrom: 'h',
        defaultTo: 'min'
      }
    }
  },

  mecanica: {
    id: 'mecanica',
    icon: '⚙️',
    title: { es: 'Mecánica', en: 'Mechanics' },
    magnitudes: {
      mass: {
        id: 'mass',
        title: { es: 'Masa', en: 'Mass' },
        baseUnit: 'kg',
        units: {
          kg: { id: 'kg', symbol: 'kg', factor: 1, name: { es: 'Kilogramos (kg)', en: 'Kilograms (kg)' } },
          g: { id: 'g', symbol: 'g', factor: 0.001, name: { es: 'Gramos (g)', en: 'Grams (g)' } },
          mg: { id: 'mg', symbol: 'mg', factor: 1e-6, name: { es: 'Miligramos (mg)', en: 'Milligrams (mg)' } },
          ug: { id: 'ug', symbol: 'µg', factor: 1e-9, name: { es: 'Microgramos (µg)', en: 'Micrograms (µg)' } },
          lb: { id: 'lb', symbol: 'lb', factor: 0.45359237, name: { es: 'Libras (lb)', en: 'Pounds (lb)' } },
          oz: { id: 'oz', symbol: 'oz', factor: 0.028349523125, name: { es: 'Onzas (oz)', en: 'Ounces (oz)' } },
          t: { id: 't', symbol: 't', factor: 1000, name: { es: 'Toneladas métricas (t)', en: 'Metric Tonnes (t)' } },
          ton_us: { id: 'ton_us', symbol: 'ton (US)', factor: 907.18474, name: { es: 'Toneladas cortas US', en: 'Short Tons US' } }
        },
        defaultFrom: 'kg',
        defaultTo: 'lb'
      },
      force: {
        id: 'force',
        title: { es: 'Fuerza', en: 'Force' },
        baseUnit: 'n',
        units: {
          n: { id: 'n', symbol: 'N', factor: 1, name: { es: 'Newtons (N)', en: 'Newtons (N)' } },
          kn: { id: 'kn', symbol: 'kN', factor: 1000, name: { es: 'Kilonewtons (kN)', en: 'Kilonewtons (kN)' } },
          mn: { id: 'mn', symbol: 'MN', factor: 1e6, name: { es: 'Meganewtons (MN)', en: 'Meganewtons (MN)' } },
          lbf: { id: 'lbf', symbol: 'lbf', factor: 4.4482216152605, name: { es: 'Libras-fuerza (lbf)', en: 'Pounds-force (lbf)' } },
          dyn: { id: 'dyn', symbol: 'dyn', factor: 1e-5, name: { es: 'Dinas (dyn)', en: 'Dynes (dyn)' } },
          kgf: { id: 'kgf', symbol: 'kgf', factor: 9.80665, name: { es: 'Kilogramos-fuerza (kgf)', en: 'Kilograms-force (kgf)' } }
        },
        defaultFrom: 'n',
        defaultTo: 'lbf'
      },
      pressure: {
        id: 'pressure',
        title: { es: 'Presión', en: 'Pressure' },
        baseUnit: 'pa',
        units: {
          pa: { id: 'pa', symbol: 'Pa', factor: 1, name: { es: 'Pascales (Pa)', en: 'Pascals (Pa)' } },
          kpa: { id: 'kpa', symbol: 'kPa', factor: 1000, name: { es: 'Kilopascales (kPa)', en: 'Kilopascals (kPa)' } },
          mpa: { id: 'mpa', symbol: 'MPa', factor: 1e6, name: { es: 'Megapascales (MPa)', en: 'Megapascals (MPa)' } },
          bar: { id: 'bar', symbol: 'bar', factor: 100000, name: { es: 'Bares (bar)', en: 'Bars (bar)' } },
          mbar: { id: 'mbar', symbol: 'mbar', factor: 100, name: { es: 'Milibares (mbar)', en: 'Millibars (mbar)' } },
          psi: { id: 'psi', symbol: 'psi', factor: 6894.757293168, name: { es: 'PSI (lbf/in²)', en: 'PSI (lbf/in²)' } },
          atm: { id: 'atm', symbol: 'atm', factor: 101325, name: { es: 'Atmósferas estándar (atm)', en: 'Standard Atmospheres (atm)' } },
          torr: { id: 'torr', symbol: 'Torr', factor: 133.322368421, name: { es: 'Torr / mmHg', en: 'Torr / mmHg' } }
        },
        defaultFrom: 'bar',
        defaultTo: 'psi'
      }
    }
  },

  informatica: {
    id: 'informatica',
    icon: '💻',
    title: { es: 'Informática', en: 'Computing' },
    magnitudes: {
      storage_binary: {
        id: 'storage_binary',
        title: { es: 'Almacenamiento Binario (IEC: 1024)', en: 'Binary Storage (IEC: 1024)' },
        baseUnit: 'b',
        units: {
          b: { id: 'b', symbol: 'B', factor: 1, name: { es: 'Bytes (B)', en: 'Bytes (B)' } },
          kib: { id: 'kib', symbol: 'KiB', factor: 1024, name: { es: 'Kibibytes (KiB)', en: 'Kibibytes (KiB)' } },
          mib: { id: 'mib', symbol: 'MiB', factor: 1048576, name: { es: 'Mebibytes (MiB)', en: 'Mebibytes (MiB)' } },
          gib: { id: 'gib', symbol: 'GiB', factor: 1073741824, name: { es: 'Gibibytes (GiB)', en: 'Gibibytes (GiB)' } },
          tib: { id: 'tib', symbol: 'TiB', factor: 1099511627776, name: { es: 'Tebibytes (TiB)', en: 'Tebibytes (TiB)' } },
          pib: { id: 'pib', symbol: 'PiB', factor: 1125899906842624, name: { es: 'Pebibytes (PiB)', en: 'Pebibytes (PiB)' } }
        },
        defaultFrom: 'gib',
        defaultTo: 'mib'
      },
      storage_decimal: {
        id: 'storage_decimal',
        title: { es: 'Almacenamiento Decimal (SI: 1000)', en: 'Decimal Storage (SI: 1000)' },
        baseUnit: 'b',
        units: {
          b: { id: 'b', symbol: 'B', factor: 1, name: { es: 'Bytes (B)', en: 'Bytes (B)' } },
          kb: { id: 'kb', symbol: 'kB', factor: 1000, name: { es: 'Kilobytes (kB)', en: 'Kilobytes (kB)' } },
          mb: { id: 'mb', symbol: 'MB', factor: 1e6, name: { es: 'Megabytes (MB)', en: 'Megabytes (MB)' } },
          gb: { id: 'gb', symbol: 'GB', factor: 1e9, name: { es: 'Gigabytes (GB)', en: 'Gigabytes (GB)' } },
          tb: { id: 'tb', symbol: 'TB', factor: 1e12, name: { es: 'Terabytes (TB)', en: 'Terabytes (TB)' } },
          pb: { id: 'pb', symbol: 'PB', factor: 1e15, name: { es: 'Petabytes (PB)', en: 'Petabytes (PB)' } }
        },
        defaultFrom: 'gb',
        defaultTo: 'mb'
      },
      bandwidth: {
        id: 'bandwidth',
        title: { es: 'Ancho de Banda / Red', en: 'Bandwidth & Data Rate' },
        baseUnit: 'bps',
        units: {
          bps: { id: 'bps', symbol: 'bps', factor: 1, name: { es: 'Bits por segundo (bps)', en: 'Bits per second (bps)' } },
          kbps: { id: 'kbps', symbol: 'kbps', factor: 1000, name: { es: 'Kilobits por segundo (kbps)', en: 'Kilobits per second (kbps)' } },
          mbps: { id: 'mbps', symbol: 'Mbps', factor: 1e6, name: { es: 'Megabits por segundo (Mbps)', en: 'Megabits per second (Mbps)' } },
          gbps: { id: 'gbps', symbol: 'Gbps', factor: 1e9, name: { es: 'Gigabits por segundo (Gbps)', en: 'Gigabits per second (Gbps)' } },
          tbps: { id: 'tbps', symbol: 'Tbps', factor: 1e12, name: { es: 'Terabits por segundo (Tbps)', en: 'Terabits per second (Tbps)' } }
        },
        defaultFrom: 'mbps',
        defaultTo: 'kbps'
      }
    }
  },

  radiofrecuencia: {
    id: 'radiofrecuencia',
    icon: '📡',
    title: { es: 'Radiofrecuencia', en: 'Radiofrequency' },
    magnitudes: {
      frequency: {
        id: 'frequency',
        title: { es: 'Frecuencia', en: 'Frequency' },
        baseUnit: 'hz',
        units: {
          hz: { id: 'hz', symbol: 'Hz', factor: 1, name: { es: 'Hertz (Hz)', en: 'Hertz (Hz)' } },
          khz: { id: 'khz', symbol: 'kHz', factor: 1000, name: { es: 'Kilohertz (kHz)', en: 'Kilohertz (kHz)' } },
          mhz: { id: 'mhz', symbol: 'MHz', factor: 1e6, name: { es: 'Megahertz (MHz)', en: 'Megahertz (MHz)' } },
          ghz: { id: 'ghz', symbol: 'GHz', factor: 1e9, name: { es: 'Gigahertz (GHz)', en: 'Gigahertz (GHz)' } },
          thz: { id: 'thz', symbol: 'THz', factor: 1e12, name: { es: 'Terahertz (THz)', en: 'Terahertz (THz)' } }
        },
        defaultFrom: 'mhz',
        defaultTo: 'khz'
      },
      wavelength_freq: {
        id: 'wavelength_freq',
        title: { es: 'Frecuencia ⇔ Longitud de Onda (λ = c/f)', en: 'Frequency ⇔ Wavelength (λ = c/f)' },
        isSpecialRfWav: true,
        defaultFrom: '100_mhz',
        defaultTo: 'm'
      },
      rf_power: {
        id: 'rf_power',
        title: { es: 'Potencia RF (dBm ⇔ W / mW)', en: 'RF Power (dBm ⇔ W / mW)' },
        isSpecialRfPower: true,
        units: {
          dbm: { id: 'dbm', symbol: 'dBm', name: { es: 'Decibelios-milivatio (dBm)', en: 'Decibel-milliwatts (dBm)' } },
          mw: { id: 'mw', symbol: 'mW', name: { es: 'Milivatios (mW)', en: 'Milliwatts (mW)' } },
          w: { id: 'w', symbol: 'W', name: { es: 'Vatios (W)', en: 'Watts (W)' } },
          kw: { id: 'kw', symbol: 'kW', name: { es: 'Kilovatios (kW)', en: 'Kilowatts (kW)' } }
        },
        defaultFrom: 'dbm',
        defaultTo: 'w'
      }
    }
  },

  scratchpad: {
    id: 'scratchpad',
    icon: '📋',
    title: { es: 'Batch Scratchpad', en: 'Batch Scratchpad' },
    isBatchMode: true
  }
};
