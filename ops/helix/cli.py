"""CLI multiplataforma de Datalaria Helix en Python puro (INV-HELIX-5).

Zero dependencias externas: opera exclusivamente con la librería estándar de Python >= 3.10.
Provee los 7 subcomandos canónicos:
  - init
  - triage
  - new-spec
  - checkpoint
  - verify
  - rollback
  - status
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Any, Sequence

EXPECTED_AGENT_IDS: tuple[str, ...] = (
    "01-orchestrator",
    "02-product-analyst",
    "03-architect",
    "04-ux-ui",
    "05-frontend",
    "06-backend-data",
    "07-apis-integrations",
    "08-media-i18n",
    "09-monetization",
    "10-security-privacy",
    "11-qa-verifier",
    "12-release-devops",
)

SURFACE_TO_BUILDER: dict[str, str] = {
    "docs": "08-media-i18n",
    "ui": "04-ux-ui",
    "frontend": "05-frontend",
    "backend": "06-backend-data",
    "data_sql": "06-backend-data",
    "apis": "07-apis-integrations",
    "media_i18n": "08-media-i18n",
    "monetization": "09-monetization",
    "auth_security": "06-backend-data",
}

AVAILABLE_BLUEPRINTS: tuple[str, ...] = (
    "blueprint-01-static-calculator",
    "blueprint-02-react-supabase-rls",
    "blueprint-03-python-quant-engine",
)

MAX_AGENT_SPEC_LINES = 85
MAX_FRICTION_RULES = 6
FORBIDDEN_STATIC_SUFFIXES = {".py", ".sql", ".env", ".pyc", ".mdc"}


# ============================================================================
# 1. Motor Determinista SpecQualityScore (0..100) — SPEC-APP-HELIX §4.2
# ============================================================================

def score_spec_markdown(markdown_text: str) -> dict[str, Any]:
    """Evalúa la calidad determinista de una especificación Markdown (0..100)."""
    text = markdown_text or ""
    lower = text.lower()

    # Pilar 1: Problema / Propósito y Usuario (20 pts)
    p1 = 0
    if re.search(r"##\s+(?:1\.\s+)?(?:propósito|resumen|problema|objetivo|misión)", lower):
        p1 += 10
    if re.search(r"(?:usuario|audiencia|profesional|cliente|business\s+context|target)", lower):
        p1 += 10

    # Pilar 2: Non-Goals y Límites (20 pts)
    p2 = 0
    if re.search(r"##\s+(?:.*)?(?:non-goals|no-objetivos|fuera\s+de\s+alcance|límites|prohibiciones)", lower):
        p2 = 20
    elif "non-goal" in lower or "fuera de alcance" in lower or "prohibido" in lower:
        p2 = 10

    # Pilar 3: Contratos tipados y Arquitectura (20 pts)
    p3 = 0
    if re.search(r"##\s+(?:.*)?(?:arquitectura|contrato|modelo\s+de\s+datos|componente|estructura)", lower):
        p3 += 10
    has_code_block = bool(re.search(r"```(?:yaml|json|python|typescript|ts|js|sql|mermaid)", lower))
    has_schema_table = bool(re.search(r"\|[^\n]+\|[^\n]+\|\n\|(?:\s*[:-]+[-| :]*)\|\n\|", text))
    if has_code_block or has_schema_table:
        p3 += 10

    # Pilar 4: Invariantes Formales INV-* (20 pts)
    invariants = sorted(list(set(re.findall(r"\bINV-[A-Z0-9-]+\b", text))))
    if len(invariants) >= 3:
        p4 = 20
    elif len(invariants) >= 1:
        p4 = 10
    else:
        p4 = 0

    # Pilar 5: Comandos Ejecutables de Verificación (20 pts)
    p5 = 0
    if re.search(r"##\s+(?:.*)?(?:verificaci|criterios\s+de\s+aceptaci|gate|pruebas)", lower):
        p5 += 10
    if re.search(r"(?:pytest|hugo|npm\s+(?:run\s+)?(?:lint|test|build)|oxlint|python\s+-m)", text):
        p5 += 10

    total_score = p1 + p2 + p3 + p4 + p5
    return {
        "total_score": total_score,
        "passed": total_score >= 70,
        "pillars": {
            "problem": p1,
            "nongoals": p2,
            "contracts": p3,
            "invariants": p4,
            "gates": p5,
        },
        "invariants_found": invariants,
    }


# ============================================================================
# 2. Algoritmo Determinista de Triaje (Réplica Estándar sin Pydantic)
# ============================================================================

def std_calculate_triage(
    milestone_id: str,
    estimated_files: int,
    surfaces: Sequence[str],
    spec_contract_change: bool = False,
    is_new_app: bool = False,
    verification_gate: str = "python -m pytest && hugo --renderToMemory",
) -> dict[str, Any]:
    """Calcula determinísticamente la talla y selección de agentes Helix."""
    if estimated_files < 1:
        raise ValueError("estimated_files debe ser >= 1")
    if not surfaces:
        raise ValueError("Debe especificarse al menos una superficie afectada.")

    unique_surfaces = list(dict.fromkeys(surfaces))

    # 1. Asignación de Talla
    if is_new_app:
        size = "XL"
    elif spec_contract_change or len(unique_surfaces) >= 3:
        size = "L"
    elif len(unique_surfaces) == 2 or estimated_files > 3:
        size = "M"
    elif estimated_files <= 3 and len(unique_surfaces) == 1 and estimated_files > 1:
        size = "S"
    else:
        size = "XS"

    # 2. Selección de Agentes
    active_set: set[str] = {"01-orchestrator", "11-qa-verifier"}
    for s in unique_surfaces:
        if s in SURFACE_TO_BUILDER:
            active_set.add(SURFACE_TO_BUILDER[s])

    if size in {"M", "L", "XL"}:
        active_set.add("03-architect")
        active_set.add("12-release-devops")
    if size in {"L", "XL"}:
        active_set.add("02-product-analyst")
        active_set.add("04-ux-ui")
    if size == "XL":
        active_set.update(EXPECTED_AGENT_IDS)

    # 3. Disparadores Innegociables
    if any(s in {"auth_security", "data_sql", "monetization"} for s in unique_surfaces):
        active_set.add("10-security-privacy")
    if any(s in {"ui", "frontend"} for s in unique_surfaces):
        active_set.add("04-ux-ui")
    if "media_i18n" in unique_surfaces:
        active_set.add("08-media-i18n")
    if "monetization" in unique_surfaces:
        active_set.add("09-monetization")

    active_ordered = [a for a in EXPECTED_AGENT_IDS if a in active_set]
    benched_ordered = [a for a in EXPECTED_AGENT_IDS if a not in active_set]

    safe_tag = re.sub(r"[^a-zA-Z0-9._-]", "-", milestone_id.lower())
    checkpoint_tag = f"sdd-checkpoint-pre-{safe_tag}"
    requires_approval = size in {"L", "XL"} or spec_contract_change

    return {
        "milestone_id": milestone_id,
        "size": size,
        "surfaces": unique_surfaces,
        "active_agents": active_ordered,
        "benched_agents": benched_ordered,
        "verification_gate": verification_gate,
        "checkpoint_tag": checkpoint_tag,
        "requires_human_approval": requires_approval,
    }


def format_triage_card_from_dict(d: dict[str, Any]) -> str:
    """Devuelve la Tarjeta de Triaje canónica de 6 líneas exactas."""
    surfaces_str = ", ".join(d["surfaces"])
    active_str = ", ".join(d["active_agents"])
    benched_str = ", ".join(d["benched_agents"]) if d["benched_agents"] else "Ninguno (escuadrón completo)"
    approval_str = "SÍ" if d["requires_human_approval"] else "NO"
    lines = [
        f"TRIAGE HELIX · Hito {d['milestone_id']} · Talla: {d['size']}",
        f"Superficies afectadas: {surfaces_str}",
        f"Roles activados ({len(d['active_agents'])} de 12): {active_str}",
        f"Roles en banquillo: {benched_str}",
        f"Verification Gate: {d['verification_gate']}",
        f"Presupuesto y Gobernanza: Máx. 2 intentos por gate · Checkpoint {d['checkpoint_tag']} · Aprobación humana previa: {approval_str}",
    ]
    return "\n".join(lines)


# ============================================================================
# 3. Funciones Auxiliares Git y Sistema de Archivos
# ============================================================================

def _run_cmd(cmd: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return res.returncode, res.stdout.strip(), res.stderr.strip()


def _find_repo_root(start_dir: Path | None = None) -> Path:
    curr = (start_dir or Path.cwd()).resolve()
    for p in [curr, *curr.parents]:
        if (p / "specs").is_dir() or (p / ".git").is_dir():
            return p
    return curr


def _check_anti_bloat(squad_dir: Path) -> list[str]:
    violations: list[str] = []
    if not squad_dir.exists():
        return violations
    for fp in squad_dir.glob("*.md"):
        if fp.name in {"README.md", "triage-rubric.md", "OPPORTUNITY_BACKLOG.md"}:
            continue
        text = fp.read_text(encoding="utf-8")
        lines = text.splitlines()
        if len(lines) > MAX_AGENT_SPEC_LINES:
            violations.append(f"{fp.name}: {len(lines)} líneas (máximo {MAX_AGENT_SPEC_LINES})")
        match = re.search(r"## 6\. Reglas de Fricción Real[^\n]*\n([\s\S]*?)(?=\n## |\Z)", text)
        if match:
            rules = [l for l in match.group(1).splitlines() if l.strip().startswith(("-", "*"))]
            if len(rules) > MAX_FRICTION_RULES:
                violations.append(f"{fp.name}: {len(rules)} reglas en Sección 6 (máximo {MAX_FRICTION_RULES})")
    return violations


def _check_static_firewall(static_dir: Path) -> list[str]:
    violations: list[str] = []
    if not static_dir.exists():
        return violations
    for p in static_dir.rglob("*"):
        if p.is_file() and p.suffix.lower() in FORBIDDEN_STATIC_SUFFIXES:
            violations.append(p.as_posix())
    return violations


# ============================================================================
# 4. Implementación de los 7 Subcomandos CLI
# ============================================================================

def cmd_status(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else _find_repo_root()
    roadmap_file = root / "specs" / "ROADMAP.md"

    active_phase = "Desconocida"
    last_checkpoint = "Ninguno"
    next_milestone = "Ninguno"

    if roadmap_file.exists():
        text = roadmap_file.read_text(encoding="utf-8")
        m_phase = re.search(r"- \*\*Fase Activa:\*\*\s*(.+)", text)
        if m_phase:
            active_phase = m_phase.group(1).strip()
        m_chk = re.search(r"- \*\*Último Checkpoint Verificado:\*\*\s*(.+)", text)
        if m_chk:
            last_checkpoint = m_chk.group(1).strip()
        m_next = re.search(r"- \*\*Próximo Hito:\*\*\s*(.+)", text)
        if m_next:
            next_milestone = m_next.group(1).strip()

    # Inspeccionar Specs
    specs_list = []
    specs_dir = root / "specs" / "apps"
    if specs_dir.exists():
        for sp in specs_dir.glob("*/spec.md"):
            scr = score_spec_markdown(sp.read_text(encoding="utf-8"))
            specs_list.append({
                "app": sp.parent.name,
                "path": sp.relative_to(root).as_posix(),
                "score": scr["total_score"],
                "passed": scr["passed"],
            })

    # Inspeccionar Squad
    squad_dir = root / "specs" / "squad"
    anti_bloat_errors = _check_anti_bloat(squad_dir)
    static_leaks = _check_static_firewall(root / "static")

    # Tags Git
    code, out, _ = _run_cmd(["git", "tag", "-l", "sdd-checkpoint-*"], cwd=root)
    git_tags = out.splitlines() if code == 0 and out else []

    status_data = {
        "root": root.as_posix(),
        "phase": active_phase,
        "last_checkpoint": last_checkpoint,
        "next_milestone": next_milestone,
        "specs": specs_list,
        "anti_bloat_violations": anti_bloat_errors,
        "static_firewall_leaks": static_leaks,
        "git_checkpoints": git_tags[-5:],
    }

    if args.json:
        print(json.dumps(status_data, indent=2, ensure_ascii=False))
        return 0

    print("================================================================================")
    print("                    DATALARIA HELIX · ESTADO DEL SISTEMA SDD                    ")
    print("================================================================================")
    print(f"Raíz del Repositorio: {root}")
    print(f"Fase Activa:         {active_phase}")
    print(f"Último Checkpoint:   {last_checkpoint}")
    print(f"Próximo Hito:        {next_milestone}")
    print("--------------------------------------------------------------------------------")
    print(f"Especificaciones Auditadas ({len(specs_list)}):")
    for s in specs_list:
        badge = "✅" if s["passed"] else "⚠️"
        print(f"  {badge} {s['app']:<20} Score: {s['score']:>3}/100  ({s['path']})")
    print("--------------------------------------------------------------------------------")
    print(f"Salud Anti-Bloat (INV-HELIX-8): {'OK ✅' if not anti_bloat_errors else 'ERRORES ❌'}")
    for err in anti_bloat_errors:
        print(f"  - Violación: {err}")
    print(f"Firewall static/ (INV-HELIX-6): {'OK ✅' if not static_leaks else 'LEAKS ❌'}")
    for leak in static_leaks:
        print(f"  - Leak: {leak}")
    print("--------------------------------------------------------------------------------")
    print(f"Checkpoints Recientes: {', '.join(git_tags[-3:]) if git_tags else 'Ninguno'}")
    print("================================================================================")
    return 0


def cmd_triage(args: argparse.Namespace) -> int:
    surfaces = [s.strip() for s in args.surfaces.split(",") if s.strip()]
    triage_dict = std_calculate_triage(
        milestone_id=args.milestone,
        estimated_files=args.files,
        surfaces=surfaces,
        spec_contract_change=args.spec_change,
        is_new_app=args.new_app,
        verification_gate=args.gate,
    )
    if args.json:
        print(json.dumps(triage_dict, indent=2, ensure_ascii=False))
    else:
        print(format_triage_card_from_dict(triage_dict))
    return 0


def cmd_new_spec(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else _find_repo_root()
    slug = args.slug.lower().strip()
    target_dir = root / "specs" / "apps" / slug
    target_dir.mkdir(parents=True, exist_ok=True)
    spec_path = target_dir / "spec.md"

    if spec_path.exists() and not args.force:
        print(f"[HELIX ERROR] La especificación ya existe: {spec_path}. Usa --force para sobrescribir.", file=sys.stderr)
        return 1

    title = args.title or slug.replace("-", " ").title()
    tier = args.tier or "pro"
    today = datetime.date.today().isoformat()

    content = f"""# SPEC-APP-{slug.upper()}: {title}

> **Identificador:** `SPEC-APP-{slug.upper()}`  
> **Versión:** `v0.1.0`  
> **Fecha:** `{today}`  
> **Clasificación:** Tier `{tier}`  
> **Ruta Canónica:** `/apps/{slug}/`  
> **Estado:** `DRAFT`

---

## 1. Propósito Ejecutivo y Problema que Resuelve
{title} proporciona una solución determinista para usuarios profesionales que requieren automatizar flujos de trabajo sin fricción.
- **Audiencia y Contexto de Negocio:** Consultores y equipos técnicos que gestionan operaciones digitales.

## 2. Límites y Prohibiciones (Non-Goals)
- **Non-Goals:**
  - Cero dependencias de servicios externos no tipados.
  - No almacenar datos sensibles en almacenamiento no cifrado.

## 3. Arquitectura y Contratos de Datos
### 3.1 Modelo de Datos Principal
```json
{{
  "id": "uuid",
  "name": "string",
  "created_at": "ISO8601"
}}
```

## 4. Invariantes Innegociables
- `INV-{slug.upper()}-1`: Cero llamadas a APIs externas en modo desconectado.
- `INV-{slug.upper()}-2`: Validación estricta de esquemas antes de persistencia.
- `INV-{slug.upper()}-3`: Cero fuga de variables de entorno o credenciales.

## 5. Criterios de Aceptación y Verification Gates
- **Verification Gate:**
  ```powershell
  python -m pytest tests/ -v
  ```
- Cobertura de tests unitarios >= 90%.

---

## 6. Historial Evolutivo (Changelog SemVer)
| Versión | Fecha | Tipo | Cambios |
| :--- | :--- | :--- | :--- |
| `v0.1.0` | `{today}` | 📐 Spec | Inicialización de especificación bajo estándar Datalaria Helix SDD. |
"""
    spec_path.write_text(content, encoding="utf-8")
    print(f"[HELIX] Especificación creada con éxito: {spec_path}")

    if args.with_design:
        design_path = target_dir / "design.md"
        design_content = f"""# Especificación de Diseño UX/UI: {title} (`design.md`)

## 1. Sistema de Diseño y Tokens
- Paleta: Slate `#0f172a`, Teal `#0d9488`, Indigo `#6366f1`.
- Tipografía: Outfit (títulos), Inter (cuerpo), JetBrains Mono (código/números).
- Accesibilidad: Cumplimiento estricto WCAG 2.2 AA (contraste >= 4.5:1).

## 2. Signature Wow Moment
- Feedback visual instantáneo con micro-interacción en < 100ms.
"""
        design_path.write_text(design_content, encoding="utf-8")
        print(f"[HELIX] Especificación de diseño creada: {design_path}")

    score = score_spec_markdown(content)
    print(f"[HELIX] SpecQualityScore: {score['total_score']}/100 (Passed: {score['passed']})")
    return 0


def cmd_checkpoint(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else _find_repo_root()
    prefix = "sdd-checkpoint-post" if args.post else "sdd-checkpoint-pre"
    safe_id = re.sub(r"[^a-zA-Z0-9._-]", "-", args.id.lower().strip())
    tag_name = f"{prefix}-{safe_id}"

    if not args.allow_dirty:
        code, out, _ = _run_cmd(["git", "status", "--porcelain"], cwd=root)
        if code == 0 and out.strip():
            print(f"[HELIX ERROR] El árbol de trabajo tiene cambios sin commitear.\nUsa --allow-dirty para forzar el tag sobre el commit HEAD actual.", file=sys.stderr)
            return 1

    code, out, err = _run_cmd(["git", "tag", "-f", tag_name], cwd=root)
    if code != 0:
        print(f"[HELIX ERROR] Error al crear tag Git '{tag_name}': {err}", file=sys.stderr)
        return 1

    print(f"[HELIX CHECKPOINT] Tag creado exitosamente: {tag_name}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else _find_repo_root()
    min_score = args.min_score
    failures: list[str] = []

    # 1. Auditoría de Specs
    specs_to_audit = [Path(args.spec).resolve()] if args.spec else list((root / "specs" / "apps").glob("*/spec.md"))
    results = []

    for sp in specs_to_audit:
        if not sp.exists():
            failures.append(f"No existe el archivo de spec: {sp}")
            continue
        content = sp.read_text(encoding="utf-8")
        is_frozen = bool(re.search(r"(?:frozen|legacy|cuarentena|congelad|reverse-spec)", content, re.IGNORECASE))
        scr = score_spec_markdown(content)
        passed = scr["total_score"] >= min_score or (is_frozen and not args.spec)
        results.append({
            "path": sp.as_posix(),
            "score": scr["total_score"],
            "passed": passed,
            "is_frozen": is_frozen,
        })
        if scr["total_score"] < min_score and not (is_frozen and not args.spec):
            failures.append(f"Spec '{sp.parent.name}/spec.md' insuficiente: {scr['total_score']}/{min_score} pts.")

    # 2. Firewall static/
    leaks = _check_static_firewall(root / "static")
    if leaks:
        failures.extend([f"Firewall static/ violado: {l}" for l in leaks])

    # 3. Anti-Bloat
    bloat = _check_anti_bloat(root / "specs" / "squad")
    if bloat:
        failures.extend([f"Anti-Bloat violado: {b}" for b in bloat])

    # 4. Gate ejecutable opcional
    gate_success = True
    if args.run_gate:
        print(f"[HELIX VERIFY] Ejecutando gate: {args.run_gate}")
        gcode = subprocess.run(args.run_gate, shell=True, cwd=root).returncode
        if gcode != 0:
            gate_success = False
            failures.append(f"Verification gate falló con código {gcode}: '{args.run_gate}'")

    if args.json:
        print(json.dumps({"passed": len(failures) == 0, "failures": failures, "specs": results}, indent=2))
        return 0 if not failures else 1

    print("================================================================================")
    print(f"VERIFICACIÓN HELIX SDD (Min Score: {min_score})")
    print("================================================================================")
    for r in results:
        if r["passed"]:
            b = "✅"
        elif r.get("is_frozen"):
            b = "⏸️ [FROZEN]"
        else:
            b = "❌"
        print(f"  {b} {r['path']} -> {r['score']}/100")
    if failures:
        print("\nFALLOS DETECTADOS:")
        for f in failures:
            print(f"  ❌ {f}")
        return 1
    print("\nTODOS LOS CHECKS SUPERADOS CON ÉXITO ✅")
    return 0


def cmd_rollback(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else _find_repo_root()
    tag = args.tag_or_id.strip()
    if not tag.startswith("sdd-checkpoint-"):
        tag = f"sdd-checkpoint-pre-{tag}"

    # Comprobar si el tag existe
    code, out, _ = _run_cmd(["git", "tag", "-l", tag], cwd=root)
    if code != 0 or not out.strip():
        print(f"[HELIX ERROR] El tag Git '{tag}' no existe.", file=sys.stderr)
        return 1

    if not args.confirm:
        print(f"[HELIX ROLLBACK — DRY RUN] Tag objetivo: {tag}")
        print("Comando que se ejecutará con --confirm:")
        print(f"  git checkout {tag} -- .")
        print("\nArchivos modificados actualmente:")
        _, s_out, _ = _run_cmd(["git", "status", "--short"], cwd=root)
        print(s_out if s_out else "  (árbol de trabajo limpio)")
        print("\nPara ejecutar la restauración definitiva, añade el flag --confirm.")
        return 0

    code, out, err = _run_cmd(["git", "checkout", tag, "--", "."], cwd=root)
    if code != 0:
        print(f"[HELIX ERROR] Falló el rollback al tag '{tag}': {err}", file=sys.stderr)
        return 1

    print(f"[HELIX ROLLBACK] Árbol restaurado exitosamente al checkpoint: {tag}")

    # Registrar en ROADMAP.md si se indicó motivo
    if args.log_reason:
        roadmap = root / "specs" / "ROADMAP.md"
        if roadmap.exists():
            today = datetime.date.today().isoformat()
            row = f"| {today} | Rollback | {args.log_reason} | Restauración de archivos al tag {tag} | ✅ Rollback Ejecutado |"
            old_txt = roadmap.read_text(encoding="utf-8")
            roadmap.write_text(old_txt.strip() + "\n" + row + "\n", encoding="utf-8")
            print(f"[HELIX ROLLBACK] Incidencia documentada en ROADMAP.md.")

    return 0


def cmd_init(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve() if args.target else Path.cwd().resolve()
    target.mkdir(parents=True, exist_ok=True)
    root = _find_repo_root()

    # Intentar usar build_core_kit si está disponible
    try:
        from ops.helix.build_core_kit import init_project_from_core_kit
        init_project_from_core_kit(target_dir=target, blueprint_id=args.blueprint)
        # Asegurar copia de helix.py en target
        shutil.copy2(__file__, target / "helix.py")
        print(f"[HELIX INIT] Repositorio inicializado exitosamente en: {target}")
        return 0
    except Exception:
        pass

    # Fallback determinista autónomo en caso de ejecución standalone fuera del repo
    (target / "specs").mkdir(parents=True, exist_ok=True)
    (target / "specs" / "squad").mkdir(parents=True, exist_ok=True)
    (target / "specs" / "_templates").mkdir(parents=True, exist_ok=True)
    (target / "specs" / "apps").mkdir(parents=True, exist_ok=True)

    if (root / "AGENTS.md").exists():
        shutil.copy2(root / "AGENTS.md", target / "AGENTS.md")
    if (root / "CLAUDE.md").exists():
        shutil.copy2(root / "CLAUDE.md", target / "CLAUDE.md")
    if (root / "specs" / "_constitution.md").exists():
        shutil.copy2(root / "specs" / "_constitution.md", target / "specs" / "_constitution.md")
    if (root / "specs" / "ROADMAP.md").exists():
        shutil.copy2(root / "specs" / "ROADMAP.md", target / "specs" / "ROADMAP.md")

    shutil.copy2(__file__, target / "helix.py")
    print(f"[HELIX INIT] Repositorio base inicializado con éxito en: {target}")
    return 0


# ============================================================================
# 5. Punto de Entrada Principal CLI
# ============================================================================

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="helix",
        description="Datalaria Helix CLI — Sistema Operativo de Ingeniería para Desarrollo Asistido por IA (SDD)",
    )
    sub = parser.add_subparsers(dest="subcommand", required=True)

    # 1. status
    p_status = sub.add_parser("status", help="Muestra el estado de la hoja de ruta, specs y salud de Helix.")
    p_status.add_argument("--root", type=str, help="Directorio raíz del proyecto.")
    p_status.add_argument("--json", action="store_true", help="Salida en JSON estructurado.")

    # 2. triage
    p_triage = sub.add_parser("triage", help="Calcula el dimensionamiento determinista y emite la Tarjeta de Triaje.")
    p_triage.add_argument("--milestone", required=True, help="Identificador del hito (ej. 6.5).")
    p_triage.add_argument("--files", type=int, required=True, help="Número de archivos estimados.")
    p_triage.add_argument("--surfaces", required=True, help="Superficies separadas por coma (docs,ui,frontend,backend,...).")
    p_triage.add_argument("--spec-change", action="store_true", help="Si modifica contratos de especificación.")
    p_triage.add_argument("--new-app", action="store_true", help="Si representa una nueva aplicación.")
    p_triage.add_argument("--gate", default="python -m pytest && hugo --renderToMemory", help="Comando del Verification Gate.")
    p_triage.add_argument("--json", action="store_true", help="Salida en JSON.")

    # 3. new-spec
    p_new = sub.add_parser("new-spec", help="Crea el andamiaje de una nueva especificación de módulo.")
    p_new.add_argument("slug", help="Slug único de la aplicación o módulo.")
    p_new.add_argument("--title", help="Título legible del módulo.")
    p_new.add_argument("--tier", default="pro", choices=["lab", "pro", "flagship"], help="Tier de la app.")
    p_new.add_argument("--with-design", action="store_true", help="Genera también design.md.")
    p_new.add_argument("--force", action="store_true", help="Sobrescribe si ya existe.")
    p_new.add_argument("--root", type=str, help="Directorio raíz del proyecto.")

    # 4. checkpoint
    p_chk = sub.add_parser("checkpoint", help="Crea un tag Git de seguridad sdd-checkpoint-*.")
    p_chk.add_argument("id", help="Identificador del hito (ej. 6.5).")
    p_chk.add_argument("--post", action="store_true", help="Crea tag post-hito en lugar de pre-hito.")
    p_chk.add_argument("--allow-dirty", action="store_true", help="Permite crear tag aunque haya cambios sin commitear.")
    p_chk.add_argument("--root", type=str, help="Directorio raíz del proyecto.")

    # 5. verify
    p_ver = sub.add_parser("verify", help="Audita specs, invariantes y ejecuta gates deterministas.")
    p_ver.add_argument("--spec", help="Ruta de una spec concreta a evaluar.")
    p_ver.add_argument("--min-score", type=int, default=70, help="Puntuación mínima de SpecQualityScore requerida (0..100).")
    p_ver.add_argument("--run-gate", help="Comando shell a ejecutar y verificar código de salida 0.")
    p_ver.add_argument("--json", action="store_true", help="Salida en JSON.")
    p_ver.add_argument("--root", type=str, help="Directorio raíz del proyecto.")

    # 6. rollback
    p_rb = sub.add_parser("rollback", help="Restaura de forma segura el árbol de trabajo al checkpoint previo.")
    p_rb.add_argument("tag_or_id", help="Tag completo o identificador del hito.")
    p_rb.add_argument("--confirm", action="store_true", help="Aplica la restauración en Git de forma efectiva.")
    p_rb.add_argument("--log-reason", help="Registra el motivo del rollback en specs/ROADMAP.md.")
    p_rb.add_argument("--root", type=str, help="Directorio raíz del proyecto.")

    # 7. init
    p_init = sub.add_parser("init", help="Inicializa un nuevo repositorio con el estándar Helix SDD.")
    p_init.add_argument("--target", default=".", help="Directorio destino para inicializar.")
    p_init.add_argument("--blueprint", choices=AVAILABLE_BLUEPRINTS, help="Blueprint opcional a clonar.")

    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    parser = build_parser()
    args = parser.parse_args(argv)

    handler_map = {
        "status": cmd_status,
        "triage": cmd_triage,
        "new-spec": cmd_new_spec,
        "checkpoint": cmd_checkpoint,
        "verify": cmd_verify,
        "rollback": cmd_rollback,
        "init": cmd_init,
    }

    handler = handler_map.get(args.subcommand)
    if not handler:
        parser.print_help()
        return 1

    try:
        return handler(args)
    except Exception as exc:
        print(f"[HELIX CLI ERROR] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    sys.exit(main())
