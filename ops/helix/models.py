"""Contratos Pydantic v2 y Motor Determinista de Triaje para Datalaria Helix (SPEC-APP-HELIX)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, field_validator, model_validator

SquadCell = Literal["direction", "construction", "assurance", "delivery"]
TaskSize = Literal["XS", "S", "M", "L", "XL"]
SurfaceType = Literal[
    "docs",
    "ui",
    "frontend",
    "backend",
    "data_sql",
    "apis",
    "media_i18n",
    "monetization",
    "auth_security",
]

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


class AgentSpecFrontmatter(BaseModel):
    """Esquema estricto del bloque YAML de cada ficha AGENT_SPEC en specs/squad/."""

    id: str = Field(..., pattern=r"^\d{2}-[a-z0-9-]+$")
    name_es: str = Field(..., min_length=3)
    name_en: str = Field(..., min_length=3)
    cell: SquadCell
    icon: str = Field(..., min_length=1)
    activates_on_sizes: list[TaskSize] = Field(..., min_length=1)
    mandatory_triggers: list[str] = Field(..., min_length=1)
    can_write_production_code: bool
    has_veto_power: bool
    inputs: list[str] = Field(..., min_length=1)
    outputs: list[str] = Field(..., min_length=1)

    @model_validator(mode="after")
    def validate_helix_invariants(self) -> "AgentSpecFrontmatter":
        # INV-HELIX-1: Ningún agente constructor puede tener derecho a veto,
        # y ningún agente con veto puede escribir código de producción.
        if self.cell == "construction" and self.has_veto_power:
            raise ValueError(
                f"Violación INV-HELIX-1 en {self.id}: un agente de 'construction' no puede tener has_veto_power=True."
            )
        if self.has_veto_power and self.can_write_production_code:
            raise ValueError(
                f"Violación INV-HELIX-1 en {self.id}: un agente con derecho a veto no puede escribir código de producción."
            )
        if self.has_veto_power and self.id not in {"10-security-privacy", "11-qa-verifier"}:
            raise ValueError(
                f"Violación INV-HELIX-1 en {self.id}: solo '10-security-privacy' y '11-qa-verifier' poseen derecho a veto."
            )
        return self


class AgentSpecDocument(BaseModel):
    """Representación completa en memoria de una ficha AGENT_SPEC."""

    frontmatter: AgentSpecFrontmatter
    body_markdown: str = Field(..., min_length=100)
    source_path: str

    @field_validator("body_markdown")
    @classmethod
    def validate_required_sections(cls, v: str) -> str:
        required_headings = [
            "## 1. Misión y Propósito",
            "## 2. Cuándo se Activa",
            "## 3. Responsabilidades",
            "## 4. Entregables y Contrato de Salida",
            "## 5. Límites y Prohibiciones",
        ]
        for heading in required_headings:
            if heading not in v:
                raise ValueError(f"Falta la sección obligatoria '{heading}' en el cuerpo del AGENT_SPEC.")
        return v


class TriageDecision(BaseModel):
    """Resultado determinista del algoritmo de triaje del Orquestador (SPEC-APP-HELIX §3.2 y §4.1)."""

    milestone_id: str
    size: TaskSize
    surfaces: list[SurfaceType]
    active_agents: list[str]
    benched_agents: list[str]
    verification_gate: str
    checkpoint_tag: str
    requires_human_approval: bool

    def format_triage_card(self) -> str:
        """Devuelve la Tarjeta de Triaje canónica de exactamente 6 líneas."""
        surfaces_str = ", ".join(self.surfaces)
        active_str = ", ".join(self.active_agents)
        benched_str = ", ".join(self.benched_agents) if self.benched_agents else "Ninguno (escuadrón completo)"
        approval_str = "SÍ" if self.requires_human_approval else "NO"
        lines = [
            f"TRIAGE HELIX · Hito {self.milestone_id} · Talla: {self.size}",
            f"Superficies afectadas: {surfaces_str}",
            f"Roles activados ({len(self.active_agents)} de 12): {active_str}",
            f"Roles en banquillo: {benched_str}",
            f"Verification Gate: {self.verification_gate}",
            f"Presupuesto y Gobernanza: Máx. 2 intentos por gate · Checkpoint {self.checkpoint_tag} · Aprobación humana previa: {approval_str}",
        ]
        return "\n".join(lines)


def load_squad_specs(squad_dir: Path | str = Path("specs/squad")) -> list[AgentSpecDocument]:
    """Carga, parsea y valida determinísticamente las 12 fichas AGENT_SPEC desde specs/squad/."""
    base = Path(squad_dir)
    docs: list[AgentSpecDocument] = []
    for agent_id in EXPECTED_AGENT_IDS:
        fp = base / f"{agent_id}.md"
        if not fp.exists():
            raise FileNotFoundError(f"Falta la ficha canónica AGENT_SPEC: {fp}")
        raw = fp.read_text(encoding="utf-8")
        if not raw.startswith("---"):
            raise ValueError(f"El archivo {fp} no comienza con frontmatter YAML ('---').")
        parts = raw.split("---", 2)
        if len(parts) < 3:
            raise ValueError(f"Frontmatter YAML mal cerrado en {fp}.")
        meta_dict = yaml.safe_load(parts[1])
        frontmatter = AgentSpecFrontmatter(**meta_dict)
        if frontmatter.id != agent_id:
            raise ValueError(f"El id '{frontmatter.id}' no coincide con el nombre de archivo '{agent_id}.md'.")
        docs.append(
            AgentSpecDocument(
                frontmatter=frontmatter,
                body_markdown=parts[2].strip(),
                source_path=fp.as_posix(),
            )
        )
    return docs


def calculate_triage(
    milestone_id: str,
    estimated_files: int,
    surfaces: list[SurfaceType],
    spec_contract_change: bool = False,
    is_new_app: bool = False,
    verification_gate: str = "python -m pytest && hugo --renderToMemory",
) -> TriageDecision:
    """Ejecuta el algoritmo determinista de triaje (SPEC-APP-HELIX §4.1 e INV-HELIX-2/3)."""
    if estimated_files < 1:
        raise ValueError("estimated_files debe ser >= 1")
    if not surfaces:
        raise ValueError("Debe especificarse al menos una superficie afectada.")

    unique_surfaces = list(dict.fromkeys(surfaces))

    # 1. Asignación de Talla Base
    if is_new_app:
        size: TaskSize = "XL"
    elif spec_contract_change or len(unique_surfaces) >= 3:
        size = "L"
    elif len(unique_surfaces) == 2 or estimated_files > 3:
        size = "M"
    elif estimated_files <= 3 and len(unique_surfaces) == 1 and estimated_files > 1:
        size = "S"
    else:
        size = "XS"

    # 2. Selección base de agentes según talla y superficie
    active_set: set[str] = {"01-orchestrator", "11-qa-verifier"}  # Siempre activos (TRG-QA)

    # Constructores por superficie
    surface_to_builder: dict[SurfaceType, str] = {
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
    for s in unique_surfaces:
        active_set.add(surface_to_builder[s])

    # Roles de dirección y entrega según talla
    if size in {"M", "L", "XL"}:
        active_set.add("03-architect")
        active_set.add("12-release-devops")
    if size in {"L", "XL"}:
        active_set.add("02-product-analyst")
        active_set.add("04-ux-ui")
    if size == "XL":
        active_set.update(EXPECTED_AGENT_IDS)

    # 3. Inyección de Disparadores Automáticos Innegociables (INV-HELIX-3)
    if any(s in {"auth_security", "data_sql", "monetization"} for s in unique_surfaces):
        active_set.add("10-security-privacy")  # TRG-SEC
    if any(s in {"ui", "frontend"} for s in unique_surfaces):
        active_set.add("04-ux-ui")  # TRG-UX
    if "media_i18n" in unique_surfaces:
        active_set.add("08-media-i18n")  # TRG-I18N
    if "monetization" in unique_surfaces:
        active_set.add("09-monetization")  # TRG-MON

    # Ordenar según orden canónico 01..12
    active_ordered = [a for a in EXPECTED_AGENT_IDS if a in active_set]
    benched_ordered = [a for a in EXPECTED_AGENT_IDS if a not in active_set]

    safe_tag = re.sub(r"[^a-zA-Z0-9._-]", "-", milestone_id.lower())
    return TriageDecision(
        milestone_id=milestone_id,
        size=size,
        surfaces=unique_surfaces,
        active_agents=active_ordered,
        benched_agents=benched_ordered,
        verification_gate=verification_gate,
        checkpoint_tag=f"sdd-checkpoint-pre-{safe_tag}",
        requires_human_approval=(size in {"L", "XL"} or spec_contract_change),
    )
