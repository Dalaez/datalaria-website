"""Planificador declarativo de olas en 24h para Autopilot 2.0 (INV-AUTO-10)."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from autopilot.src.models import DispatchQueue, WaveQueueEntry

DEFAULT_QUEUE_PATH = REPO_ROOT / "data" / "editorial" / "dispatch_queue.yaml"


def _configure_utf8_console() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def parse_utc_timestamp(ts: str) -> datetime:
    """Convierte un timestamp ISO-8601 con zona horaria en datetime UTC consciente."""
    parsed = datetime.fromisoformat(ts.strip().replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError(f"Timestamp sin zona horaria UTC: {ts}")
    return parsed.astimezone(timezone.utc)


def format_utc_timestamp(dt: datetime) -> str:
    """Formatea un datetime como ISO-8601 UTC acabado en 'Z'."""
    aware = dt if dt.tzinfo is not None else dt.replace(tzinfo=timezone.utc)
    return aware.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_dispatch_queue(queue_path: Path = DEFAULT_QUEUE_PATH) -> DispatchQueue:
    """Carga y valida con Pydantic v2 el archivo YAML de cola declarativa."""
    path = Path(queue_path)
    if not path.is_file():
        return DispatchQueue()
    with open(path, "r", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh) or {}
    return DispatchQueue(**raw)


def save_dispatch_queue(
    queue: DispatchQueue,
    queue_path: Path = DEFAULT_QUEUE_PATH,
) -> Path:
    """Persiste la cola declarativa en UTF-8 con formato YAML legible."""
    path = Path(queue_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = queue.model_dump(mode="json")
    with open(path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(payload, fh, allow_unicode=True, sort_keys=False)
    return path


def enqueue_post_waves(
    es_file_path: str,
    en_file_path: str,
    slug_prefix: str,
    start_utc: Optional[datetime] = None,
    queue_path: Path = DEFAULT_QUEUE_PATH,
    include_newsletter: bool = False,
    include_wave1: bool = False,
) -> DispatchQueue:
    """Encola de forma idempotente las olas escalonadas (T+0h, T+7h, T+12h, T+22h) de un post."""
    base_dt = (start_utc or datetime.now(timezone.utc)).astimezone(timezone.utc)
    date_tag = base_dt.strftime("%Y-%m-%d")
    native_channels: List[str] = ["linkedin", "x"] + (["newsletter"] if include_newsletter else [])

    new_entries: List[WaveQueueEntry] = []
    if include_wave1:
        new_entries.append(
            WaveQueueEntry(
                id=f"{slug_prefix}-{date_tag}-wave1-es-native",
                file_path=es_file_path.replace("\\", "/"),
                lang="es",
                wave="1_es_native",
                channels=native_channels,  # type: ignore[arg-type]
                scheduled_at_utc=format_utc_timestamp(base_dt),
                notes="Ola 1 (T+0h): ES Native Social",
            )
        )

    new_entries.extend(
        [
            WaveQueueEntry(
                id=f"{slug_prefix}-{date_tag}-wave2-en-native",
                file_path=en_file_path.replace("\\", "/"),
                lang="en",
                wave="2_en_native",
                channels=native_channels,  # type: ignore[arg-type]
                scheduled_at_utc=format_utc_timestamp(base_dt + timedelta(hours=7)),
                notes="Ola 2 (T+7h · Apertura USA): EN Native Social",
            ),
            WaveQueueEntry(
                id=f"{slug_prefix}-{date_tag}-wave3a-es-devto",
                file_path=es_file_path.replace("\\", "/"),
                lang="es",
                wave="3a_es_syndication",
                channels=["devto"],
                scheduled_at_utc=format_utc_timestamp(base_dt + timedelta(hours=12)),
                notes="Ola 3A (T+12h): Dev.to ES con ventaja de indexación canónica",
            ),
            WaveQueueEntry(
                id=f"{slug_prefix}-{date_tag}-wave3b-en-syndication",
                file_path=en_file_path.replace("\\", "/"),
                lang="en",
                wave="3b_en_syndication",
                channels=["devto", "coderlegion"],
                scheduled_at_utc=format_utc_timestamp(base_dt + timedelta(hours=22)),
                notes="Ola 3B (T+22h Día +1): Dev.to EN + CoderLegion EN",
            ),
        ]
    )

    queue = load_dispatch_queue(queue_path)
    existing_ids = {item.id: idx for idx, item in enumerate(queue.entries)}
    for entry in new_entries:
        if entry.id in existing_ids:
            idx = existing_ids[entry.id]
            if queue.entries[idx].status == "pending":
                queue.entries[idx] = entry
        else:
            queue.entries.append(entry)
    save_dispatch_queue(queue, queue_path)
    return queue


def process_due_waves(
    queue_path: Path = DEFAULT_QUEUE_PATH,
    now_utc: Optional[datetime] = None,
    dry_run: bool = False,
    runner: Optional[Callable[..., Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Ejecuta todas las olas pendientes vencidas (scheduled_at_utc <= now_utc)."""
    current = (now_utc or datetime.now(timezone.utc)).astimezone(timezone.utc)
    queue = load_dispatch_queue(queue_path)
    if runner is None:
        from autopilot.src.orchestrator import run_orchestration

        runner = run_orchestration

    processed: List[Dict[str, Any]] = []
    skipped_future: List[str] = []
    failed: List[Dict[str, Any]] = []

    for entry in queue.entries:
        if entry.status != "pending":
            continue
        due_dt = parse_utc_timestamp(entry.scheduled_at_utc)
        if due_dt > current:
            skipped_future.append(entry.id)
            continue

        print(
            f"⏰ Procesando ola vencida '{entry.id}' ({entry.wave}) -> "
            f"{entry.file_path} | channels={entry.channels}"
        )
        try:
            target_path = Path(entry.file_path)
            resolved_path = target_path if target_path.is_absolute() else (REPO_ROOT / target_path)
            runner(
                str(resolved_path),
                dry_run=dry_run,
                wave=entry.wave,
                channels=entry.channels,
            )
            if not dry_run:
                entry.status = "completed"
                entry.executed_at_utc = format_utc_timestamp(current)
                entry.last_error = None
            processed.append({"id": entry.id, "wave": entry.wave, "channels": list(entry.channels)})
        except Exception as exc:
            if not dry_run:
                entry.status = "failed"
                entry.last_error = str(exc)[:300]
            failed.append({"id": entry.id, "error": str(exc)})
            print(f"❌ Error procesando ola '{entry.id}': {exc}")

    if not dry_run and (processed or failed):
        save_dispatch_queue(queue, queue_path)

    return {
        "now_utc": format_utc_timestamp(current),
        "processed_count": len(processed),
        "failed_count": len(failed),
        "pending_future_count": len(skipped_future),
        "processed": processed,
        "failed": failed,
        "skipped_future": skipped_future,
    }


def main(argv: Optional[List[str]] = None) -> None:
    _configure_utf8_console()
    parser = argparse.ArgumentParser(description="Planificador de olas 24h de Autopilot 2.0.")
    parser.add_argument(
        "--queue-path",
        default=str(DEFAULT_QUEUE_PATH),
        help="Ruta al archivo YAML de cola declarativa.",
    )
    parser.add_argument("--process-due", action="store_true", help="Ejecuta las olas vencidas.")
    parser.add_argument("--dry-run", action="store_true", help="Simula sin persistir ni publicar.")
    parser.add_argument("--status", action="store_true", help="Muestra el estado actual de la cola.")
    args = parser.parse_args(argv)

    q_path = Path(args.queue_path)
    if args.status or not args.process_due:
        queue = load_dispatch_queue(q_path)
        print(f"📋 Cola declarativa ({q_path}): {len(queue.entries)} entradas")
        for entry in queue.entries:
            print(
                f"  - [{entry.status.upper()}] {entry.id} | {entry.wave} | "
                f"channels={entry.channels} | at={entry.scheduled_at_utc}"
            )
        if not args.process_due:
            return

    if args.process_due:
        summary = process_due_waves(queue_path=q_path, dry_run=args.dry_run)
        print(
            f"✅ Resumen olas: ejecutadas={summary['processed_count']} · "
            f"fallidas={summary['failed_count']} · futuras={summary['pending_future_count']}"
        )


if __name__ == "__main__":
    main()
