"""
scripts/generate_all_app_icons.py
Ejecuta la generación de iconos PWA PNG estándar y maskable para:
- apps/conversor/
- apps/maths/
"""
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from ops.pwa_icon_generator import generate_app_pwa_icons

# -------------------------------------------------------------
# 1. CONVERSOR DE UNIDADES
# -------------------------------------------------------------
conversor_svg_path = ROOT_DIR / "apps" / "conversor" / "icon.svg"
conversor_std_svg = conversor_svg_path.read_text(encoding="utf-8")

# Maskable: Fondo full-bleed sin rx y sin stroke perimetral
conversor_maskable_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b0f17" />
      <stop offset="100%" stop-color="#111827" />
    </linearGradient>
    <linearGradient id="cyanGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="100%" stop-color="#0284c7" />
    </linearGradient>
    <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#818cf8" />
      <stop offset="100%" stop-color="#6366f1" />
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="12" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Full Bleed Background Canvas for Android Adaptive Mask -->
  <rect width="512" height="512" fill="url(#bgGrad)" />

  <!-- Technical Circular Reticle (SI Metrology) Safe-Zone -->
  <circle cx="256" cy="256" r="168" fill="none" stroke="rgba(148, 163, 184, 0.18)" stroke-width="4" stroke-dasharray="8 8" />
  <circle cx="256" cy="256" r="120" fill="none" stroke="rgba(14, 165, 233, 0.25)" stroke-width="2" />

  <!-- Dual Conversion Curved Arrows -->
  <g filter="url(#glow)">
    <!-- Top Arc Arrow (Clockwise) -->
    <path d="M 160 216 A 112 112 0 0 1 352 216" fill="none" stroke="url(#cyanGrad)" stroke-width="28" stroke-linecap="round" />
    <polygon points="364,180 392,232 336,236" fill="#38bdf8" />

    <!-- Bottom Arc Arrow (Counter-Clockwise) -->
    <path d="M 352 296 A 112 112 0 0 1 160 296" fill="none" stroke="url(#accentGrad)" stroke-width="28" stroke-linecap="round" />
    <polygon points="148,332 120,280 176,276" fill="#818cf8" />
  </g>

  <!-- Center Metrology Core Point -->
  <circle cx="256" cy="256" r="14" fill="#f8fafc" />
</svg>"""

print("[*] Generando iconos para Conversor Pro...")
generate_app_pwa_icons(
    app_dir=ROOT_DIR / "apps" / "conversor",
    static_dir=ROOT_DIR / "static" / "apps" / "conversor",
    standard_svg=conversor_std_svg,
    maskable_svg=conversor_maskable_svg
)

# -------------------------------------------------------------
# 2. ÁBACO ARCADE / MATHS
# -------------------------------------------------------------
maths_svg_path = ROOT_DIR / "apps" / "maths" / "icon.svg"
maths_std_svg = maths_svg_path.read_text(encoding="utf-8")

# Maskable: Fondo full-bleed 512x512 y elementos escalados a zona segura Android 80%
maths_maskable_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <linearGradient id="mathsBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3b82f6"/>
      <stop offset="50%" stop-color="#8b5cf6"/>
      <stop offset="100%" stop-color="#ec4899"/>
    </linearGradient>
    <linearGradient id="abacusFrame" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#e2e8f0"/>
    </linearGradient>
    <filter id="dropShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#0f172a" flood-opacity="0.35"/>
    </filter>
  </defs>

  <!-- Fondo full bleed adaptativo -->
  <rect width="512" height="512" fill="url(#mathsBg)"/>

  <!-- Grupo escalado al 78% centrado en la zona segura circular (r <= 204px) -->
  <g transform="translate(256, 256) scale(0.78) translate(-256, -256)">
    <!-- Cuadrícula interior arcade -->
    <rect x="68" y="68" width="376" height="376" rx="64" fill="url(#abacusFrame)" filter="url(#dropShadow)"/>

    <!-- Varillas del ábaco -->
    <line x1="140" y1="110" x2="140" y2="400" stroke="#cbd5e1" stroke-width="12" stroke-linecap="round"/>
    <line x1="256" y1="110" x2="256" y2="400" stroke="#cbd5e1" stroke-width="12" stroke-linecap="round"/>
    <line x1="372" y1="110" x2="372" y2="400" stroke="#cbd5e1" stroke-width="12" stroke-linecap="round"/>
    <line x1="90" y1="240" x2="422" y2="240" stroke="#94a3b8" stroke-width="14" stroke-linecap="round"/>

    <!-- Cuentas / Botones 3D de Colores (Suma, Resta, Multiplica, Divide) -->
    <!-- Columna 1: Suma (Azul) -->
    <circle cx="140" cy="170" r="32" fill="#0ea5e9"/>
    <circle cx="140" cy="300" r="32" fill="#0ea5e9"/>
    <circle cx="140" cy="370" r="32" fill="#0284c7"/>

    <!-- Columna 2: Resta / Multiplica (Ámbar y Verde) -->
    <circle cx="256" cy="180" r="32" fill="#f59e0b"/>
    <circle cx="256" cy="310" r="32" fill="#10b981"/>

    <!-- Columna 3: División (Violeta y Rosa) -->
    <circle cx="372" cy="160" r="32" fill="#8b5cf6"/>
    <circle cx="372" cy="320" r="32" fill="#ec4899"/>
    <circle cx="372" cy="380" r="32" fill="#db2777"/>

    <!-- Símbolos matemáticos superpuestos -->
    <text x="140" y="179" font-family="system-ui, sans-serif" font-size="28" font-weight="900" fill="#ffffff" text-anchor="middle">+</text>
    <text x="256" y="189" font-family="system-ui, sans-serif" font-size="34" font-weight="900" fill="#ffffff" text-anchor="middle">−</text>
    <text x="256" y="320" font-family="system-ui, sans-serif" font-size="28" font-weight="900" fill="#ffffff" text-anchor="middle">×</text>
    <text x="372" y="169" font-family="system-ui, sans-serif" font-size="28" font-weight="900" fill="#ffffff" text-anchor="middle">÷</text>
  </g>
</svg>"""

print("[*] Generando iconos para Ábaco Arcade (Maths)...")
generate_app_pwa_icons(
    app_dir=ROOT_DIR / "apps" / "maths",
    static_dir=ROOT_DIR / "static" / "apps" / "maths",
    standard_svg=maths_std_svg,
    maskable_svg=maths_maskable_svg
)

print("[OK] Todos los iconos PWA generados con éxito.")
