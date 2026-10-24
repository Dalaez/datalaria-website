"""
LifeOps API — Smart Alerts Evaluator Service
=============================================
Evaluates business rules over user activities, tasks, and projects
to generate actionable real-time notifications.
"""
import datetime as dt
from typing import List, Dict, Any
from services.supabase_client import db

def evaluate_user_alerts(user_id: str) -> List[Dict[str, Any]]:
    """
    Evaluates business rules for the user and returns a list of active alerts.
    """
    today = dt.date.today()
    today_str = today.isoformat()
    two_days_ahead = (today + dt.timedelta(days=2)).isoformat()
    three_days_ago = (today - dt.timedelta(days=3)).isoformat()
    fourteen_days_ago = (today - dt.timedelta(days=14)).isoformat()

    alerts: List[Dict[str, Any]] = []

    # ── 1. Tasks Rules (Overdue & Upcoming Deadlines) ──
    tasks_res = (
        db("tasks")
        .select("id, title, due_date, status, priority")
        .eq("user_id", user_id)
        .neq("status", "done")
        .neq("status", "cancelled")
        .execute()
    )
    tasks = tasks_res.data or []

    for t in tasks:
        due = t.get("due_date")
        if not due:
            continue
        if due < today_str:
            alerts.append({
                "id": f"task-overdue-{t['id']}",
                "type": "task_overdue",
                "severity": "critical",
                "title": f"Tarea Vencida: {t['title']}",
                "message": f"La fecha límite era el {due}. Pasa por el tablero Kanban para actualizar su estado.",
                "action_url": "/professional?tab=kanban",
                "action_label": "Ver en Kanban",
                "entity_id": t["id"],
                "created_at": dt.datetime.now().isoformat(),
            })
        elif due <= two_days_ahead:
            alerts.append({
                "id": f"task-upcoming-{t['id']}",
                "type": "task_upcoming",
                "severity": "warning",
                "title": f"Fecha Límite Próxima: {t['title']}",
                "message": f"Vence el {due}. ¡Planifícala para hoy!",
                "action_url": "/professional?tab=kanban",
                "action_label": "Ver Tarea",
                "entity_id": t["id"],
                "created_at": dt.datetime.now().isoformat(),
            })

    # ── 2. Sport Inactivity Rule (> 3 days without workout) ──
    latest_workout_res = (
        db("activities")
        .select("id, date, title")
        .eq("user_id", user_id)
        .eq("activity_type", "sport")
        .order("date", desc=True)
        .limit(1)
        .execute()
    )
    latest_workout = latest_workout_res.data

    if latest_workout:
        last_date = latest_workout[0]["date"]
        if last_date < three_days_ago:
            alerts.append({
                "id": "sport-inactivity",
                "type": "sport_inactivity",
                "severity": "warning",
                "title": "Mantén tu Racha Deportiva 🏃",
                "message": f"Han pasado más de 3 días desde tu última sesión ({last_date}). ¿Toca entrenar hoy?",
                "action_url": "/personal?tab=sport",
                "action_label": "Registrar Sesión",
                "entity_id": None,
                "created_at": dt.datetime.now().isoformat(),
            })
    else:
        # No workouts recorded yet
        alerts.append({
            "id": "sport-welcome",
            "type": "sport_welcome",
            "severity": "info",
            "title": "Bienvenido al Módulo Deporte",
            "message": "Aún no has registrado tu primer entrenamiento. ¡Comienza hoy!",
            "action_url": "/personal?tab=sport",
            "action_label": "Añadir Primer Entreno",
            "entity_id": None,
            "created_at": dt.datetime.now().isoformat(),
        })

    # ── 3. Stagnant Reading Books (> 14 days in progress) ──
    books_res = (
        db("activities")
        .select("id, title, date, books!inner(status, author, pages_read, pages_total)")
        .eq("user_id", user_id)
        .eq("activity_type", "book")
        .execute()
    )
    # Filter safely
    for b in (books_res.data or []):
        bk = b.get("books", {})
        if isinstance(bk, list) and bk:
            bk = bk[0]
        if bk.get("status") == "reading" and b.get("date") and b["date"] < fourteen_days_ago:
            alerts.append({
                "id": f"book-stagnant-{b['id']}",
                "type": "book_stagnant",
                "severity": "info",
                "title": f"Lectura en Curso: {b['title']}",
                "message": f"Llevas tiempo con este libro de {bk.get('author', 'tu biblioteca')}. ¿Actualizamos las páginas leídas?",
                "action_url": "/personal?tab=books",
                "action_label": "Actualizar Lectura",
                "entity_id": b["id"],
                "created_at": dt.datetime.now().isoformat(),
            })

    return alerts
