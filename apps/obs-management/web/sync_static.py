"""Sincronizador determinista Zero-CDN de apps/obs-management/web/ -> static/apps/obs-management/.

Cumple Constitución Art. 2 (Firewall static/) e INV-OBS-1 (< 45 KB gzipped de app shell, cero CDNs externos)
y sincroniza assets PWA completos (manifest.json, sw.js, iconos vectoriales y maskable).

Uso:
  python apps/obs-management/web/sync_static.py          # Sincroniza y verifica presupuesto
  python apps/obs-management/web/sync_static.py --check  # Verifica paridad sin escribir
"""

from __future__ import annotations

import argparse
import gzip
from pathlib import Path
import re
import sys

WEB_DIR = Path(__file__).resolve().parent
REPO_ROOT = WEB_DIR.parents[2]
STATIC_DIR = REPO_ROOT / "static" / "apps" / "obs-management"

CORE_SHELL_FILES: tuple[str, ...] = (
    "index.html",
    "styles.css",
    "i18n.js",
    "engine.js",
    "app.js",
    "manifest.json",
    "sw.js",
)

STATIC_ASSETS: tuple[str, ...] = CORE_SHELL_FILES + (
    "icon.svg",
    "apple-touch-icon.png",
    "icons/icon-192.png",
    "icons/icon-512.png",
    "icons/icon-maskable-192.png",
    "icons/icon-maskable-512.png",
)

FORBIDDEN_SUFFIXES: set[str] = {".py", ".sql", ".env", ".pyc", ".txt", ".mdc"}
MAX_CORE_GZIP_BYTES = 45 * 1024  # INV-OBS-1: < 45 KB gzipped app shell
MAX_CORE_RAW_BYTES = 125 * 1024  # Anti-bloat raw cap para core files


def minify_css(text: str) -> str:
    """Compacta CSS eliminando comentarios y sangría sin alterar cadenas entrecomilladas."""
    text = re.sub(r"/\*[\s\S]*?\*/", "", text)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines) + "\n"


def minify_js(text: str) -> str:
    """Elimina comentarios de línea completa y espacios de sangría preservando sintaxis JS."""
    cleaned: list[str] = []
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("//"):
            continue
        cleaned.append(stripped)
    return "\n".join(cleaned) + "\n"


def minify_html(text: str) -> str:
    """Compacta HTML eliminando comentarios y líneas vacías preservando atributos."""
    text = re.sub(r"<!--[\s\S]*?-->", "", text)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines) + "\n"


def build_artifacts() -> dict[str, bytes]:
    """Construye todos los artefactos deterministas en memoria desde apps/obs-management/web/."""
    out: dict[str, bytes] = {}
    for name in STATIC_ASSETS:
        src = WEB_DIR / name
        if not src.exists():
            raise FileNotFoundError(f"Falta archivo fuente canónico: {src}")
        if name.endswith((".png", ".jpg", ".jpeg", ".ico")):
            out[name] = src.read_bytes()
            continue

        raw = src.read_text(encoding="utf-8")
        if name.endswith(".css"):
            transformed = minify_css(raw)
        elif name.endswith(".js"):
            transformed = minify_js(raw)
        elif name.endswith(".html"):
            transformed = minify_html(raw)
        else:
            transformed = raw

        if "cdn.tailwindcss.com" in transformed.lower():
            raise ValueError(f"Violación INV-OBS-1: CDN prohibido detectado en {name}")
        out[name] = transformed.encode("utf-8")
    return out


def verify_static_firewall() -> list[str]:
    """Verifica que static/apps/obs-management/ no contenga archivos prohibidos."""
    violations: list[str] = []
    if not STATIC_DIR.exists():
        return violations
    for item in STATIC_DIR.rglob("*"):
        if item.is_file() and (item.suffix.lower() in FORBIDDEN_SUFFIXES or item.name == ".env"):
            violations.append(str(item.relative_to(REPO_ROOT)))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Sincroniza frontend Zero-CDN y PWA de obs-management.")
    parser.add_argument("--check", action="store_true", help="Verifica paridad y límites sin escribir.")
    args = parser.parse_args()

    artifacts = build_artifacts()
    core_raw = sum(len(artifacts[k]) for k in CORE_SHELL_FILES)
    core_gzip = sum(len(gzip.compress(artifacts[k], compresslevel=9)) for k in CORE_SHELL_FILES)

    if core_gzip >= MAX_CORE_GZIP_BYTES:
        print(f"ERROR INV-OBS-1: Core shell gzip {core_gzip} B >= {MAX_CORE_GZIP_BYTES} B ({core_gzip / 1024:.2f} KB).")
        return 1
    if core_raw >= MAX_CORE_RAW_BYTES:
        print(f"ERROR INV-OBS-1: Core shell raw {core_raw} B >= {MAX_CORE_RAW_BYTES} B ({core_raw / 1024:.2f} KB).")
        return 1

    violations = verify_static_firewall()
    if violations:
        print(f"ERROR Firewall static/: archivos prohibidos detectados: {violations}")
        return 1

    if args.check:
        drifted: list[str] = []
        for name, expected in artifacts.items():
            dest = STATIC_DIR / name
            if not dest.exists() or dest.read_bytes() != expected:
                drifted.append(name)
        if drifted:
            print(f"ERROR: Desincronización entre apps/obs-management/web/ y static/: {drifted}")
            return 1
        print(
            f"OK --check: {len(artifacts)} artefactos sincronizados "
            f"(shell gzip {core_gzip / 1024:.2f} KB < 45 KB · shell raw {core_raw / 1024:.2f} KB)."
        )
        return 0

    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    for name, payload in artifacts.items():
        dest = STATIC_DIR / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(payload)

    print(
        f"OK sync: {len(artifacts)} artefactos escritos en {STATIC_DIR} "
        f"(shell gzip {core_gzip / 1024:.2f} KB < 45 KB · shell raw {core_raw / 1024:.2f} KB)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
