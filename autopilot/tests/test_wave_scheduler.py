"""Tests deterministas del planificador de olas 24h y filtro por canal/ola (INV-AUTO-9/10)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from autopilot.src import orchestrator
from autopilot.src.models import WaveQueueEntry, resolve_allowed_channels
from autopilot.src.wave_scheduler import (
    enqueue_post_waves,
    load_dispatch_queue,
    process_due_waves,
)


def test_resolve_allowed_channels_waves_and_overrides() -> None:
    assert resolve_allowed_channels() == {"x", "linkedin", "newsletter", "devto", "coderlegion"}
    assert resolve_allowed_channels(wave="1_es_native") == {"linkedin", "x", "newsletter"}
    assert resolve_allowed_channels(wave="3a_es_syndication") == {"devto"}
    assert resolve_allowed_channels(wave="3b_en_syndication") == {"devto", "coderlegion"}
    assert resolve_allowed_channels(wave="3b_en_syndication", channels="linkedin") == {"linkedin"}
    assert resolve_allowed_channels(channels=["devto", "coderlegion"]) == {"devto", "coderlegion"}

    with pytest.raises(ValueError):
        resolve_allowed_channels(wave="unknown_wave")
    with pytest.raises(ValueError):
        resolve_allowed_channels(channels="mastodon")


def test_wave_queue_entry_normalizes_utc_and_rejects_naive_dates() -> None:
    entry = WaveQueueEntry(
        id="test-wave-utc",
        file_path="content/en/posts/sample/index.md",
        lang="en",
        wave="2_en_native",
        channels=["linkedin", "x"],
        scheduled_at_utc="2026-11-16T15:30:00+01:00",
    )
    assert entry.scheduled_at_utc == "2026-11-16T14:30:00Z"

    with pytest.raises(ValueError):
        WaveQueueEntry(
            id="test-wave-naive",
            file_path="content/en/posts/sample/index.md",
            lang="en",
            wave="2_en_native",
            channels=["linkedin"],
            scheduled_at_utc="2026-11-16T15:30:00",
        )


def test_orchestrator_filters_live_channels_and_preserves_full_dry_run_audit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    post_dir = tmp_path / "content" / "es" / "posts" / "demo-amfe"
    post_dir.mkdir(parents=True)
    post_file = post_dir / "index.md"
    post_file.write_text(
        "---\ntitle: \"Matriz AMFE Demo\"\ndate: 2026-11-16\ndraft: false\n---\n\nContenido técnico demo.\n",
        encoding="utf-8",
    )
    social_pack = post_dir / "social_pack.yaml"
    social_pack.write_text(
        """es:
  x:
    hook: "Cómo transformar matrices de riesgo subjetivas en decisiones cuantitativas auditables con AMFE."
    thread:
      - "1/4 Las matrices 5x5 tradicionales agrupan demasiados riesgos en zona amarilla."
      - "2/4 AMFE añade la dimensión de Detección inversa para penalizar fallos ciegos."
      - "3/4 Prioridad de Acción AIAG-VDA evita ocultar eventos críticos de severidad alta."
      - "4/4 Lee el modelo completo: https://datalaria.com/es/posts/demo-amfe/"
    hashtags: ["AMFE", "ISO31000"]
  linkedin:
    text: |-
      Las matrices 5x5 cualitativas fallan al justificar presupuestos de mitigación.

      ⚠️ Sin cuantificar la pérdida esperada ni la detección en tiempo real, el CFO no tiene criterio objetivo.

      ¿Cómo evalúas la criticidad operativa en tu equipo?
    hashtags: ["AMFE"]
  devto:
    enabled: true
    title: "AMFE Cuantitativo"
    description: "Cómo pasar de matrices subjetivas al cálculo de NPR y Prioridad de Acción."
    tags: ["operations", "fmea"]
    canonical_url: "https://datalaria.com/es/posts/demo-amfe/"
    published: true
""",
        encoding="utf-8",
    )

    monkeypatch.setenv("ENABLE_TWITTER", "true")
    monkeypatch.setenv("ENABLE_LINKEDIN", "true")
    monkeypatch.setenv("ENABLE_DEVTO", "true")
    monkeypatch.setenv("ENABLE_CODERLEGION", "false")
    monkeypatch.setenv("ENABLE_NEWSLETTER", "false")

    dry_res = orchestrator.run_orchestration(
        str(post_file),
        dry_run=True,
        cache_file=str(tmp_path / "cache.json"),
        dist_dir=tmp_path / "dist",
        wave="1_es_native",
        channels="linkedin",
    )
    assert dry_res["audit_report"]["overall_status"] == "PASS"
    assert set(dry_res["audit_report"]["results"].keys()) == {"x", "linkedin", "devto"}

    calls: list[str] = []

    class FakeSocialManager:
        def post_to_twitter(self, **kwargs):
            calls.append("x")
            return True

        def post_to_linkedin(self, **kwargs):
            calls.append("linkedin")
            return True

        def post_to_devto(self, **kwargs):
            calls.append("devto")
            return True

        def post_to_coderlegion(self, **kwargs):
            calls.append("coderlegion")
            return True

    monkeypatch.setattr(orchestrator, "SocialMediaManager", FakeSocialManager)

    live_res = orchestrator.run_orchestration(
        str(post_file),
        dry_run=False,
        cache_file=str(tmp_path / "cache_live.json"),
        dist_dir=tmp_path / "dist",
        wave="1_es_native",
        channels="linkedin",
    )
    assert calls == ["linkedin"]
    assert live_res["dispatched_channels"] == ["linkedin"]
    assert live_res["allowed_channels"] == ["linkedin"]


def test_wave_scheduler_enqueue_and_process_due_only(tmp_path: Path) -> None:
    q_path = tmp_path / "dispatch_queue.yaml"
    t0 = datetime(2026, 11, 16, 7, 30, tzinfo=timezone.utc)

    q = enqueue_post_waves(
        es_file_path="content/es/posts/demo/index.md",
        en_file_path="content/en/posts/demo/index.md",
        slug_prefix="demo",
        start_utc=t0,
        queue_path=q_path,
        include_wave1=False,
    )
    assert [e.wave for e in q.entries] == [
        "2_en_native",
        "3a_es_syndication",
        "3b_en_syndication",
    ]

    dispatched: list[tuple[str, list[str]]] = []

    def fake_runner(file_path: str, dry_run: bool = False, wave=None, channels=None):
        dispatched.append((str(wave), list(channels or [])))
        return {"ok": True}

    # At T+8h only wave2 (T+7h) should execute; wave3a (T+12h) and wave3b (T+22h) remain pending.
    res1 = process_due_waves(
        queue_path=q_path,
        now_utc=datetime(2026, 11, 16, 15, 0, tzinfo=timezone.utc),
        runner=fake_runner,
    )
    assert res1["processed_count"] == 1
    assert res1["pending_future_count"] == 2
    assert dispatched == [("2_en_native", ["linkedin", "x"])]

    reloaded = load_dispatch_queue(q_path)
    statuses = {e.wave: e.status for e in reloaded.entries}
    assert statuses == {
        "2_en_native": "completed",
        "3a_es_syndication": "pending",
        "3b_en_syndication": "pending",
    }

    # Failing runner marks failed cleanly without affecting untouched entries.
    def failing_runner(*args, **kwargs):
        raise RuntimeError("Simulated API outage")

    res2 = process_due_waves(
        queue_path=q_path,
        now_utc=datetime(2026, 11, 16, 20, 0, tzinfo=timezone.utc),
        runner=failing_runner,
    )
    assert res2["failed_count"] == 1
    statuses_after = {e.wave: e.status for e in load_dispatch_queue(q_path).entries}
    assert statuses_after["3a_es_syndication"] == "failed"
    assert statuses_after["3b_en_syndication"] == "pending"
