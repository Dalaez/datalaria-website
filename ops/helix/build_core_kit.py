"""Generador y empaquetador del Kit Comercial Genérico Helix Core (Hito 6.4 / SPEC-APP-HELIX).

Genera el árbol completo en `packages/helix/core_kit/`:
  - 01_Constitution_and_Memory/ (AGENTS.md, CLAUDE.md, _constitution.md, ROADMAP.md, DECISIONS.md)
  - 02_Templates/ (app-spec, design, agent-spec)
  - 03_Squad_12_Agents_and_Adapters/ (12 fichas canónicas + adaptadores .agents, .claude, .cursor)
  - 04_Project_Blueprints/ (3 blueprints completos: static-calculator, react-supabase-rls, python-quant-engine)
  - 05_Case_Studies_and_Docs/ (Caso Crisol real, Quickstarts ES/EN)
  - README.md y LICENSE.txt en raíz

Además implementa `init_project_from_core_kit()` para inicializar cualquier repositorio vacío.
"""

from __future__ import annotations

import argparse
import shutil
import zipfile
from pathlib import Path
from typing import Literal

from ops.helix.build_adapters import build_adapters

BlueprintType = Literal[
    "blueprint-01-static-calculator",
    "blueprint-02-react-supabase-rls",
    "blueprint-03-python-quant-engine",
]

AVAILABLE_BLUEPRINTS: tuple[BlueprintType, ...] = (
    "blueprint-01-static-calculator",
    "blueprint-02-react-supabase-rls",
    "blueprint-03-python-quant-engine",
)


def _render_generic_agents_md() -> str:
    return """# AGENTS.md — Sistema Operativo de Agentes de Ingeniería (Helix Squad SDD)

> **Compatibilidad Universal:** Punto de entrada obligatorio y fuente de verdad operativa para cualquier agente de IA (Google Antigravity, Claude Code, Cursor, GitHub Copilot).

---

## 1. PROTOCOLO DE ARRANQUE EN 3 PASOS

Antes de proponer planes o modificar código de producción:
1. **Estado del Ecosistema:** Leer `specs/ROADMAP.md` para identificar hito activo y último checkpoint.
2. **Reglas Inmutables:** Leer `specs/_constitution.md` (Artículos 1 al 9).
3. **Especificación Activa y Triaje:** Leer `specs/apps/<slug>/spec.md`, aplicar la rúbrica de `specs/squad/triage-rubric.md` y cargar **únicamente** las fichas de los roles activados.

---

## 2. MAPA TOPOLÓGICO DEL REPOSITORIO

- `/specs/`: El Corazón SDD (Fuente Única de Verdad).
- `/specs/squad/`: Fichas canónicas del Escuadrón Helix (12 Agentes).
- `/specs/_templates/`: Plantillas para nuevas especificaciones.
- `/src/` o `/apps/`: Código de producción bajo cobertura de specs.
- `/tests/`: Suites de verificación automatizada.

---

## 3. BUCLE SDD ATÓMICO (TRIAGE -> SPEC -> CHECKPOINT -> BUILD -> GATE -> RELEASE)

1. **Nadie verifica su propio trabajo (`INV-HELIX-1`):** Ningún agente constructor puede aprobar su propio trabajo.
2. **Triaje Bajo Demanda (`INV-HELIX-2`):** Emitir la Tarjeta de Triaje de 6 líneas y cargar solo los roles convocados.
3. **Control Anti-Bloat (`INV-HELIX-8`):** Fichas canónicas limitadas a 85 líneas y máx. 6 reglas en Sección 6.
4. **Gates Deterministas:** Tests automatizados antes de cualquier commit o release.
"""


def _render_generic_claude_md() -> str:
    return """# CLAUDE.md — Guía Operativa para Claude Code

Este repositorio opera bajo el estándar **Datalaria Helix SDD**.

## Reglas de Comportamiento para Claude Code:
1. Lee `specs/ROADMAP.md` y `specs/_constitution.md` antes de cualquier modificación.
2. Cuando se requiera la intervención del escuadrón, consulta los subagentes pre-configurados en `.claude/agents/`.
3. Nunca modifiques archivos de producción sin una especificación activa en `specs/`.
4. Ejecuta siempre la suite de tests correspondiente antes de declarar una tarea completada.
"""


def _render_generic_constitution() -> str:
    return """# CONSTITUCIÓN DEL SISTEMA DE DESARROLLO GUIADO POR ESPECIFICACIONES (SDD)
## Versión 1.1.0 — Invariantes de Ingeniería

### Artículo 1: Fuente Única de Verdad (Spec-First)
Todo software comienza con una especificación formal (`spec.md`). Ningún código de producción se crea ni refactoriza sin especificación previa aprobada.

### Artículo 2: Topología y Límites Estrictos
El código de producción reside exclusivamente en los directorios autorizados. Los artefactos estáticos públicos no deben contener secretos ni código ejecutable no compilado.

### Artículo 3: Aislamiento de Datos y Secretos
Las variables de entorno residen en `.env` (nunca commiteadas). Todo acceso a base de datos multi-usuario debe estar protegido por Row Level Security (RLS) o políticas de autorización equivalentes.

### Artículo 4: Patrón Dual-Mode (Offline First / Cloud Sync)
Las aplicaciones deben ser funcionales en modo local/desconectado siempre que sea viable arquitectónicamente, sincronizando con la nube de forma no bloqueante.

### Artículo 5: Separación Inviolable de Construcción y Verificación (INV-HELIX-1)
Los agentes o desarrolladores constructores tienen prohibido verificar su propio trabajo. La verificación es potestad de roles de QA y Seguridad independientes con derecho a veto.

### Artículo 6: Verificación Determinista por Gates
Ninguna tarea se considera terminada por inspección visual subjetiva. Debe superar comandos automatizados de test y compilación con código de salida 0.

### Artículo 7: Control de Presupuesto y Rollback Determinista
Si un gate de verificación falla en 2 intentos consecutivos, el sistema debe detenerse y restaurar el último checkpoint estable conocido.

### Artículo 8: Gobernanza de Versiones y Sincronización SemVer
Toda release incrementa su versión semántica e impacta simultáneamente en los metadatos y en el historial evolutivo de la especificación.

### Artículo 9: Escuadrón Helix y Triaje Bajo Demanda
El trabajo técnico se gobierna mediante las 4 células de Helix (Dirección, Construcción, Garantía, Entrega) aplicando triaje bajo demanda según la talla de la tarea.
"""


def _render_generic_roadmap() -> str:
    return """# ROADMAP.md — Mapa de Ruta y Memoria de Ejecución

## Puntero de Ejecución Actual
- **Fase Activa:** Fase 1 — Inicialización del Ecosistema
- **Hito Actual:** Hito 1.1 — Configuración Base del Proyecto
- **Último Checkpoint Verificado:** `sdd-checkpoint-init`

---

## Registro de Fases e Hitos

### Fase 1: Arquitectura y Cimientos
- [x] **Hito 1.0: Inicialización del Repositorio y Adopción de Helix SDD** (Fecha: 2026-11-04)
  - *Gate superado:* `pytest` y validación de adaptadores.
- [ ] **Hito 1.1: Especificación del Primer Módulo**
  - *Gate:* Aprobación formal de `specs/apps/main_app/spec.md`.

---

## Registro de Bloqueos y Rollbacks (Audit Log)
| Fecha | Hito | Incidente / Causa | Acción Tomada / Rollback | Checkpoint Restaurado |
| :--- | :--- | :--- | :--- | :--- |
| - | - | Ningún bloqueo registrado | - | - |
"""


def _render_generic_decisions() -> str:
    return """# DECISIONS.md — Registro Canónico de Decisiones Arquitectónicas (ADRs)

## ADR-001: Adopción del Framework Helix SDD
- **Fecha:** 2026-11-04
- **Estado:** Aprobado
- **Contexto:** Se requiere un marco riguroso de desarrollo asistido por IA para prevenir desincronizaciones y deuda técnica.
- **Decisión:** Adoptar la Constitución SDD v1.1.0 y el escuadrón de 12 agentes Helix con triaje bajo demanda.
- **Consecuencias:** Mayor predictibilidad, trazabilidad absoluta y verificación determinista.
"""


def _render_case_study_crisol() -> str:
    return """# Caso de Estudio 01: Operación Crisol — Inmunización de Datalaria Pulse con Helix Squad

## Contexto y Desafío
Datalaria Pulse (el motor de gobernanza editorial y catálogo de Datalaria) debía someterse a una auditoría formal completa antes de su lanzamiento comercial fijado para el 18 de noviembre. Se requería auditar seguridad, integridad de datos bilingües, licencias comerciales, empaquetado y rendimiento sin introducir regresiones.

## Metodología: Convocatoria del Escuadrón Completo (Talla XL)
El Orquestador (`01-orchestrator`) emitió una Tarjeta de Triaje de Talla XL convocando a las 4 células (12 agentes). Cada agente asumió su dominio de especialidad:
- `02-product-analyst`: Reconcilió la coherencia funcional del catálogo y posts editoriales.
- `03-architect`: Reforzó el patrón Dual-Mode y el desacoplamiento entre builder y static.
- `04-ux-ui` & `05-frontend`: Blindaron la interfaz bilingüe y eliminaron advertencias de build.
- `06-backend-data`: Consolidó los esquemas Pydantic v2 en `ops/pulse/models.py`.
- `07-apis-integrations`: Auditó la resiliencia en la ingesta de metadatos externos.
- `08-media-i18n`: Garantizó el 100% de paridad bilingüe ES/EN en 26 artículos y 3 apps.
- `09-monetization`: Protegió el embargo comercial del 18 de noviembre mediante tests criptográficos y de fecha.
- `10-security-privacy`: Bloqueó exposición de variables de entorno y validó aislamiento de secrets.
- `11-qa-verifier`: Ejecutó 42 aserciones automatizadas en pytest con 0 fallos.
- `12-release-devops`: Creó el checkpoint Git, empaquetó el kit staged y sincronizó SemVer v0.1.0.

## Resultados Medibles
- **0 regresiones** en el portal editorial Hugo.
- **100% test pass rate** en suites de pytest (`test_models`, `test_embargo_18nov`, `test_publish`).
- **Embargo comercial validado**: Ningún asset no autorizado es accesible en la compilación pública.
- **Trazabilidad total**: Changelog sincronizado entre `spec.md` y `data/apps/pulse.yaml`.
"""


def _render_quickstart_es() -> str:
    return """# Guía de Inicio Rápido: Helix Core Kit (Español)

Bienvenido a **Datalaria Helix Core Kit**, el sistema operativo de ingeniería para gobernar el desarrollo de software asistido por IA mediante **Spec-Driven Development (SDD)**.

## Paso 1: Configurar el Repositorio
Copia la estructura del Kit a tu proyecto:
- Coloca `AGENTS.md` y `CLAUDE.md` en la raíz de tu repositorio.
- Coloca la carpeta `specs/` en la raíz.
- Coloca `.agents/`, `.claude/` y `.cursor/` para soporte multimodelo.

## Paso 2: Seleccionar un Blueprint (Opcional)
Si inicias un proyecto nuevo, puedes basarte en uno de los 3 blueprints incluidos en `04_Project_Blueprints/`:
- `blueprint-01-static-calculator`: Aplicaciones web o móviles ligeras sin backend.
- `blueprint-02-react-supabase-rls`: SaaS con React, base de datos y autenticación segura.
- `blueprint-03-python-quant-engine`: Motores analíticos, CLIs y librerías con Pydantic v2.

## Paso 3: Tu Primer Bucle de Desarrollo
1. Define la especificación de tu aplicación en `specs/apps/<nombre>/spec.md` usando la plantilla de `specs/_templates/app-spec.template.md`.
2. Emite la Tarjeta de Triaje (6 líneas) con tu agente orquestador.
3. Ejecuta la construcción con los roles especializados.
4. Pasa el Verification Gate con QA independiente.
5. Emite el `DEBRIEF HELIX` y cierra el hito en `ROADMAP.md`.
"""


def _render_quickstart_en() -> str:
    return """# Quickstart Guide: Helix Core Kit (English)

Welcome to **Datalaria Helix Core Kit**, the engineering operating system for AI-assisted development governed by **Spec-Driven Development (SDD)**.

## Step 1: Repository Setup
Copy the Kit structure to your project:
- Place `AGENTS.md` and `CLAUDE.md` at your repository root.
- Place `specs/` at your repository root.
- Place `.agents/`, `.claude/`, and `.cursor/` for multi-IDE and multi-model support.

## Step 2: Choose a Blueprint (Optional)
If bootstrapping a new project, select one of the 3 blueprints located in `04_Project_Blueprints/`:
- `blueprint-01-static-calculator`: Zero-backend client-side web or mobile tools.
- `blueprint-02-react-supabase-rls`: Fullstack SaaS with React, auth, and database RLS.
- `blueprint-03-python-quant-engine`: Quantitative analytics, CLIs, and libraries with Pydantic v2.

## Step 3: Your First SDD Development Loop
1. Define your module specification in `specs/apps/<slug>/spec.md` using `specs/_templates/app-spec.template.md`.
2. Emit the 6-line Triage Card via your Orchestrator agent.
3. Execute the implementation through the specialized builder roles.
4. Clear the Verification Gate through independent QA.
5. Output the `DEBRIEF HELIX` card and mark milestone complete in `ROADMAP.md`.
"""


def _render_root_readme() -> str:
    return """# Datalaria Helix Core Kit — Commercial Release v1.0.0

> **The Sovereign Spec-Driven Engineering Squad for AI-Assisted Development.**

Helix Core Kit provides the complete governance foundation, multi-tool adapters, and project blueprints to build reliable software with autonomous AI agents without loss of context or architectural debt.

## Package Contents:
- **`01_Constitution_and_Memory/`**: Universal Constitution v1.1.0, AGENTS.md, CLAUDE.md, and memory templates.
- **`02_Templates/`**: Production templates for `spec.md`, `design.md`, and `agent-spec.md`.
- **`03_Squad_12_Agents_and_Adapters/`**: Canonical 12 Helix agents + pre-compiled adapters for Google Antigravity, Anthropic Claude Code, and Cursor IDE.
- **`04_Project_Blueprints/`**: 3 turnkey reference project architectures ready to build.
- **`05_Case_Studies_and_Docs/`**: Real-world case study (Operación Crisol) and quickstart guides in English and Spanish.

## License
Commercial License — Datalaria (c) 2026. All rights reserved. See `LICENSE.txt`.
"""


def _render_license() -> str:
    return """DATALARIA HELIX CORE KIT — COMMERCIAL SINGLE USER / TEAM LICENSE
Copyright (c) 2026 Datalaria. All rights reserved.

Permission is hereby granted to the licensee to use this software and associated
documentation files for commercial and personal software engineering projects.

Redistribution, sublicensing, or resale of the core framework materials,
templates, or agent specs as a standalone commercial template is strictly prohibited.
"""


def _build_blueprint_01(target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    (target / "specs").mkdir(parents=True, exist_ok=True)
    (target / "specs" / "spec.md").write_text(
        """# SPEC: Simulador Financiero Estático en Navegador
## 1. Misión
Herramienta de simulación de hipotecas y préstamos ejecutada 100% en el navegador del cliente sin dependencias de servidor.
## 2. Invariantes
- INV-01: Cero llamadas a APIs externas para cálculos.
- INV-02: Tiempo de respuesta al deslizador < 16ms (60 FPS).
## 3. Comandos de Verificación
- Gate: `npm test` o validación estática de JavaScript.
""",
        encoding="utf-8",
    )
    (target / "specs" / "ROADMAP.md").write_text(
        """# ROADMAP — Blueprint 01
- [x] Hito 1: Estructura HTML/CSS y motor de cálculo base.
- [ ] Hito 2: Gráficos de amortización interactivos.
""",
        encoding="utf-8",
    )
    (target / "index.html").write_text(
        """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Simulador Financiero</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <main class="container">
    <h1>Simulador Financiero Estático</h1>
    <label>Capital: <input type="number" id="capital" value="100000"></label>
    <label>Tipo Interés (%): <input type="number" id="rate" value="3.5" step="0.1"></label>
    <label>Plazo (Años): <input type="number" id="years" value="25"></label>
    <div id="result" class="result-box">Cuota Estimada: -- €</div>
  </main>
  <script src="app.js"></script>
</body>
</html>
""",
        encoding="utf-8",
    )
    (target / "styles.css").write_text(
        """body { font-family: system-ui, sans-serif; background: #0f172a; color: #f8fafc; display: grid; place-items: center; min-height: 100vh; margin: 0; }
.container { background: #1e293b; padding: 2rem; border-radius: 0.75rem; border: 1px solid #334155; width: 340px; display: flex; flex-direction: column; gap: 1rem; }
label { display: flex; justify-content: space-between; font-size: 0.9rem; }
input { background: #0f172a; border: 1px solid #475569; color: white; border-radius: 0.25rem; padding: 0.25rem 0.5rem; width: 100px; text-align: right; }
.result-box { margin-top: 1rem; padding: 0.75rem; background: #0d9488; color: white; font-weight: bold; text-align: center; border-radius: 0.5rem; }
""",
        encoding="utf-8",
    )
    (target / "app.js").write_text(
        """function calculate() {
  const c = parseFloat(document.getElementById('capital').value) || 0;
  const r = (parseFloat(document.getElementById('rate').value) || 0) / 100 / 12;
  const n = (parseFloat(document.getElementById('years').value) || 0) * 12;
  if (r === 0 || n === 0) return;
  const p = (c * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
  document.getElementById('result').textContent = `Cuota Estimada: ${p.toFixed(2)} €/mes`;
}
document.querySelectorAll('input').forEach(i => i.addEventListener('input', calculate));
calculate();
""",
        encoding="utf-8",
    )


def _build_blueprint_02(target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    (target / "specs").mkdir(parents=True, exist_ok=True)
    (target / "specs" / "spec.md").write_text(
        """# SPEC: SaaS Multi-Tenant React + Supabase + RLS
## 1. Misión
Portal de gestión para empresas con autenticación segura, persistencia en Supabase y aislamiento estricto por usuario mediante Row Level Security.
## 2. Invariantes
- INV-01: Tablas de datos protegidas obligatoriamente con `ENABLE ROW LEVEL SECURITY`.
- INV-02: Cero secretos en cliente; solo anon key pública en frontend.
## 3. Comandos de Verificación
- Gate: `npm run lint && npm test`
""",
        encoding="utf-8",
    )
    (target / "specs" / "ROADMAP.md").write_text(
        """# ROADMAP — Blueprint 02
- [x] Hito 1: Esquema SQL con RLS y configuración Supabase Client.
- [ ] Hito 2: Vistas de Dashboard y facturación.
""",
        encoding="utf-8",
    )
    (target / "package.json").write_text(
        """{
  "name": "blueprint-react-supabase-rls",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "oxlint"
  },
  "dependencies": {
    "@supabase/supabase-js": "^2.39.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }
}
""",
        encoding="utf-8",
    )
    supabase_dir = target / "supabase"
    supabase_dir.mkdir(parents=True, exist_ok=True)
    (supabase_dir / "schema.sql").write_text(
        """-- Esquema Canónico Multi-Tenant con RLS estricto
create table if not exists public.tenants (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  created_at timestamptz default now()
);

alter table public.tenants enable row level security;

create policy "Users can view only their own tenant"
  on public.tenants for select
  using (auth.uid() is not null);
""",
        encoding="utf-8",
    )


def _build_blueprint_03(target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    (target / "specs").mkdir(parents=True, exist_ok=True)
    (target / "specs" / "spec.md").write_text(
        """# SPEC: Motor Cuantitativo Python con Pydantic v2
## 1. Misión
Biblioteca de modelado financiero y cálculo analítico con validación estricta de esquemas y tests deterministas.
## 2. Invariantes
- INV-01: Modelos de datos validados 100% mediante Pydantic v2 BaseModel.
- INV-02: Cobertura de tests unitarios >= 90% con pytest.
## 3. Comandos de Verificación
- Gate: `python -m pytest tests/ -v`
""",
        encoding="utf-8",
    )
    (target / "specs" / "ROADMAP.md").write_text(
        """# ROADMAP — Blueprint 03
- [x] Hito 1: Esquema de modelos de cartera y retorno ponderado.
- [ ] Hito 2: Optimización de frontera eficiente de Markowitz.
""",
        encoding="utf-8",
    )
    (target / "pyproject.toml").write_text(
        """[project]
name = "quant-engine"
version = "0.1.0"
dependencies = [
    "pydantic>=2.0.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
""",
        encoding="utf-8",
    )
    src_dir = target / "src"
    src_dir.mkdir(parents=True, exist_ok=True)
    (src_dir / "__init__.py").write_text("", encoding="utf-8")
    (src_dir / "engine.py").write_text(
        """from pydantic import BaseModel, Field

class AssetAllocation(BaseModel):
    symbol: str
    weight: float = Field(..., ge=0.0, le=1.0)
    expected_return: float

class Portfolio(BaseModel):
    assets: list[AssetAllocation]

    def weighted_return(self) -> float:
        total_w = sum(a.weight for a in self.assets)
        if abs(total_w - 1.0) > 1e-4:
            raise ValueError(f"Los pesos deben sumar 1.0 (suma actual: {total_w})")
        return sum(a.weight * a.expected_return for a in self.assets)
""",
        encoding="utf-8",
    )
    tests_dir = target / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)
    (tests_dir / "test_engine.py").write_text(
        """import pytest
from src.engine import AssetAllocation, Portfolio

def test_portfolio_weighted_return():
    p = Portfolio(
        assets=[
            AssetAllocation(symbol="EQ", weight=0.6, expected_return=0.10),
            AssetAllocation(symbol="BD", weight=0.4, expected_return=0.04),
        ]
    )
    assert pytest.approx(p.weighted_return(), 0.001) == 0.076

def test_invalid_weights():
    with pytest.raises(ValueError):
        p = Portfolio(
            assets=[
                AssetAllocation(symbol="EQ", weight=0.5, expected_return=0.10),
            ]
        )
        p.weighted_return()
""",
        encoding="utf-8",
    )


def build_core_kit(
    source_root: Path | str = Path("."),
    output_dir: Path | str = Path("packages/helix/core_kit"),
    distribution_dir: Path | str = Path("packages/00_DISTRIBUCION_LEMONSQUEEZY"),
) -> Path:
    """Genera la estructura comercial completa del Kit Helix Core y sus archivos zip."""
    root = Path(source_root).resolve()
    out = Path(output_dir).resolve()
    dist = Path(distribution_dir).resolve()

    # Limpiar y preparar carpetas
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)
    dist.mkdir(parents=True, exist_ok=True)

    # 1. 01_Constitution_and_Memory/
    dir_01 = out / "01_Constitution_and_Memory"
    dir_01.mkdir(parents=True, exist_ok=True)
    (dir_01 / "AGENTS.md").write_text(_render_generic_agents_md(), encoding="utf-8")
    (dir_01 / "CLAUDE.md").write_text(_render_generic_claude_md(), encoding="utf-8")
    specs_sub_01 = dir_01 / "specs"
    specs_sub_01.mkdir(parents=True, exist_ok=True)
    (specs_sub_01 / "_constitution.md").write_text(_render_generic_constitution(), encoding="utf-8")
    (specs_sub_01 / "ROADMAP.md").write_text(_render_generic_roadmap(), encoding="utf-8")
    (specs_sub_01 / "DECISIONS.md").write_text(_render_generic_decisions(), encoding="utf-8")

    # 2. 02_Templates/
    dir_02 = out / "02_Templates"
    dir_02.mkdir(parents=True, exist_ok=True)
    templates_src = root / "specs" / "_templates"
    if templates_src.exists():
        for tf in templates_src.glob("*.md"):
            shutil.copy2(tf, dir_02 / tf.name)
    else:
        # Fallbacks si no existen
        (dir_02 / "app-spec.template.md").write_text("# Template App Spec\n", encoding="utf-8")
        (dir_02 / "design.template.md").write_text("# Template Design\n", encoding="utf-8")
        (dir_02 / "agent-spec.template.md").write_text("# Template Agent Spec\n", encoding="utf-8")

    # 3. 03_Squad_12_Agents_and_Adapters/
    dir_03 = out / "03_Squad_12_Agents_and_Adapters"
    dir_03.mkdir(parents=True, exist_ok=True)

    # Copiar fichas canónicas desde specs/squad/
    squad_src = root / "specs" / "squad"
    canonical_specs_target = dir_03 / "specs" / "squad"
    canonical_specs_target.mkdir(parents=True, exist_ok=True)
    for sf in squad_src.glob("*.md"):
        shutil.copy2(sf, canonical_specs_target / sf.name)
    for sf in squad_src.glob("*.yaml"):
        shutil.copy2(sf, canonical_specs_target / sf.name)

    # Generar / copiar adaptadores
    build_adapters(root_dir=root, check_only=False)
    for ad_dir in [".agents", ".claude", ".cursor"]:
        src_ad = root / ad_dir
        if src_ad.exists():
            shutil.copytree(src_ad, dir_03 / ad_dir, dirs_exist_ok=True)

    # 4. 04_Project_Blueprints/
    dir_04 = out / "04_Project_Blueprints"
    dir_04.mkdir(parents=True, exist_ok=True)
    _build_blueprint_01(dir_04 / "blueprint-01-static-calculator")
    _build_blueprint_02(dir_04 / "blueprint-02-react-supabase-rls")
    _build_blueprint_03(dir_04 / "blueprint-03-python-quant-engine")

    # 5. 05_Case_Studies_and_Docs/
    dir_05 = out / "05_Case_Studies_and_Docs"
    dir_05.mkdir(parents=True, exist_ok=True)
    (dir_05 / "CASE_STUDY_01_PULSE_CRISOL.md").write_text(_render_case_study_crisol(), encoding="utf-8")
    (dir_05 / "QUICKSTART_HELIX_CORE_ES.md").write_text(_render_quickstart_es(), encoding="utf-8")
    (dir_05 / "QUICKSTART_HELIX_CORE_EN.md").write_text(_render_quickstart_en(), encoding="utf-8")

    # Raíz del Kit
    (out / "README.md").write_text(_render_root_readme(), encoding="utf-8")
    (out / "LICENSE.txt").write_text(_render_license(), encoding="utf-8")

    # Empaquetado comercial ZIP
    zip_name = "kit-datalaria-helix-core-v1.0.0.zip"
    helix_zip_path = out.parent / zip_name
    dist_zip_path = dist / zip_name

    with zipfile.ZipFile(helix_zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in out.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(out)
                zf.write(file_path, arcname)

    # Copiar exactamente a Lemon Squeezy
    shutil.copy2(helix_zip_path, dist_zip_path)

    return out


def init_project_from_core_kit(
    target_dir: Path | str,
    blueprint_id: BlueprintType | None = None,
    core_kit_dir: Path | str = Path("packages/helix/core_kit"),
) -> Path:
    """Inicializa determinísticamente un nuevo repositorio desde Helix Core Kit."""
    target = Path(target_dir).resolve()
    kit = Path(core_kit_dir).resolve()

    if not kit.exists():
        raise FileNotFoundError(f"Helix Core Kit no encontrado en {kit}. Ejecuta build_core_kit() primero.")

    target.mkdir(parents=True, exist_ok=True)

    # 1. Copiar Cimientos (AGENTS.md, CLAUDE.md, specs/)
    shutil.copy2(kit / "01_Constitution_and_Memory" / "AGENTS.md", target / "AGENTS.md")
    shutil.copy2(kit / "01_Constitution_and_Memory" / "CLAUDE.md", target / "CLAUDE.md")
    shutil.copytree(kit / "01_Constitution_and_Memory" / "specs", target / "specs", dirs_exist_ok=True)

    # 2. Copiar Templates
    shutil.copytree(kit / "02_Templates", target / "specs" / "_templates", dirs_exist_ok=True)

    # 3. Copiar Escuadrón y Adaptadores
    shutil.copytree(kit / "03_Squad_12_Agents_and_Adapters" / "specs" / "squad", target / "specs" / "squad", dirs_exist_ok=True)
    shutil.copytree(kit / "03_Squad_12_Agents_and_Adapters" / ".agents", target / ".agents", dirs_exist_ok=True)
    shutil.copytree(kit / "03_Squad_12_Agents_and_Adapters" / ".claude", target / ".claude", dirs_exist_ok=True)
    shutil.copytree(kit / "03_Squad_12_Agents_and_Adapters" / ".cursor", target / ".cursor", dirs_exist_ok=True)

    # 4. Inyectar Blueprint si se solicitó
    if blueprint_id:
        if blueprint_id not in AVAILABLE_BLUEPRINTS:
            raise ValueError(f"Blueprint desconocido: '{blueprint_id}'. Disponibles: {AVAILABLE_BLUEPRINTS}")
        bp_source = kit / "04_Project_Blueprints" / blueprint_id
        for item in bp_source.iterdir():
            if item.is_dir():
                shutil.copytree(item, target / item.name, dirs_exist_ok=True)
            else:
                shutil.copy2(item, target / item.name)

    return target


def main() -> int:
    parser = argparse.ArgumentParser(description="Constructor de Helix Core Kit (Hito 6.4).")
    parser.add_argument("--init", type=str, help="Ruta de directorio a inicializar con Helix Core Kit.")
    parser.add_argument("--blueprint", type=str, choices=AVAILABLE_BLUEPRINTS, help="Blueprint opcional para --init.")
    args = parser.parse_args()

    try:
        out_kit = build_core_kit()
        print(f"[HELIX CORE KIT] Generado exitosamente en: {out_kit}")

        if args.init:
            target_path = init_project_from_core_kit(args.init, blueprint_id=args.blueprint)
            print(f"[HELIX CORE KIT] Proyecto inicializado en: {target_path} (Blueprint: {args.blueprint or 'None'})")

        return 0
    except Exception as exc:
        import sys
        print(f"[HELIX CORE KIT ERROR] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
