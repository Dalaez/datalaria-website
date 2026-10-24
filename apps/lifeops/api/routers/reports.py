"""
LifeOps API — Reports Router
=============================
Generates and downloads customized Word (.docx) reports.
All endpoints require authentication.
"""
import datetime as dt
from typing import Optional, List, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address

from middleware.auth import AuthenticatedUser, get_current_user
from services.supabase_client import db
from services.report_generator import generate_docx_report

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])


# ── Schemas ───────────────────────────────────────

class ReportTemplateInfo(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    category: str


class GenerateReportRequest(BaseModel):
    template_type: str = "monthly_summary"  # 'monthly_summary', 'sport_performance', 'project_status'
    date_from: Optional[dt.date] = None
    date_to: Optional[dt.date] = None


TEMPLATES: List[ReportTemplateInfo] = [
    ReportTemplateInfo(
        id="monthly_summary",
        name="Informe Mensual Integral",
        description="Resumen ejecutivo completo 360° con Deporte, Libros, Cine y Portafolio de Proyectos/Tareas.",
        icon="📊",
        category="General",
    ),
    ReportTemplateInfo(
        id="sport_performance",
        name="Dossier de Rendimiento Deportivo",
        description="Desglose detallado de entrenamientos, volumen por disciplina, marcas personales y calorías.",
        icon="🏃",
        category="Personal",
    ),
    ReportTemplateInfo(
        id="project_status",
        name="Estado de Portafolio de Proyectos",
        description="Informe ejecutivo de control presupuestario, horas estimadas vs. reales y avance de tareas.",
        icon="📋",
        category="Profesional",
    ),
]


# ── Endpoints ─────────────────────────────────────

@router.get(
    "/templates",
    response_model=List[ReportTemplateInfo],
    summary="List available report templates",
)
def list_templates(user: AuthenticatedUser = Depends(get_current_user)):
    return TEMPLATES


@router.post(
    "/generate",
    summary="Generate and download a Word (.docx) report",
    response_description="Binary .docx file stream",
)
@limiter.limit("10/minute")
def generate_report(
    request: Request,
    req: GenerateReportRequest,
    user: AuthenticatedUser = Depends(get_current_user),
):
    today = dt.date.today()
    date_from = req.date_from or (today.replace(day=1))
    date_to = req.date_to or today

    # 1. Fetch activities with embedded child details in a single query
    activities = []
    if req.template_type != "project_status":
        activities_query = (
            db("activities")
            .select("*, workouts(*), books(*), films(*)")
            .eq("user_id", user.id)
            .gte("date", date_from.isoformat())
            .lte("date", date_to.isoformat())
            .order("date", desc=True)
        )
        if req.template_type == "sport_performance":
            activities_query = activities_query.eq("activity_type", "sport")

        raw_activities = activities_query.execute().data or []
        for a in raw_activities:
            # Flatten 1-to-1 relations from arrays
            if a.get("workouts"):
                a["workout"] = a["workouts"][0] if isinstance(a["workouts"], list) else a["workouts"]
            if a.get("books"):
                a["book"] = a["books"][0] if isinstance(a["books"], list) else a["books"]
            if a.get("films"):
                a["film"] = a["films"][0] if isinstance(a["films"], list) else a["films"]
            activities.append(a)

    # 2. Fetch projects and tasks
    projects = []
    tasks = []
    if req.template_type in ("monthly_summary", "project_status"):
        projects = db("projects").select("*").eq("user_id", user.id).execute().data or []
        tasks = db("tasks").select("*").eq("user_id", user.id).order("due_date", desc=False).execute().data or []

    data = {
        "activities": activities,
        "projects": projects,
        "tasks": tasks,
    }

    # 3. Generate Word document in memory
    buffer = generate_docx_report(
        template_type=req.template_type,
        user_email=user.email or "usuario@datalaria.com",
        date_from=date_from,
        date_to=date_to,
        data=data,
    )

    # 4. Log generation in generated_reports table
    filename = f"LifeOps_{req.template_type}_{date_from.strftime('%Y%m%d')}_{date_to.strftime('%Y%m%d')}.docx"
    try:
        db("generated_reports").insert({
            "user_id": user.id,
            "report_name": filename,
            "period_start": date_from.isoformat(),
            "period_end": date_to.isoformat(),
            "metadata": {
                "template_type": req.template_type,
                "activities_count": len(activities),
                "tasks_count": len(tasks),
            },
        }).execute()
    except Exception as e:
        print(f"Warning: could not log report in history: {e}")

    # 5. Return downloadable binary stream
    return Response(
        content=buffer.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@router.get(
    "/history",
    summary="List previously generated reports history",
)
def get_report_history(
    limit: int = Query(20, ge=1, le=100),
    user: AuthenticatedUser = Depends(get_current_user),
):
    result = (
        db("generated_reports")
        .select("*")
        .eq("user_id", user.id)
        .order("generated_at", desc=True)
        .limit(limit)
        .execute()
    )
    return result.data or []


# ── Data Export Endpoints (CSV & Excel) ───────────

@router.get(
    "/export/csv",
    summary="Export module data as UTF-8 BOM CSV",
    response_description="CSV attachment download",
)
@limiter.limit("20/minute")
def export_csv(
    request: Request,
    entity: str = Query(..., description="Entity to export: 'sport', 'books', 'films', 'tasks', 'projects'"),
    user: AuthenticatedUser = Depends(get_current_user),
):
    try:
        from services.data_exporter import export_entity_csv
        csv_bytes = export_entity_csv(entity, user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    today_str = dt.date.today().strftime('%Y%m%d')
    filename = f"lifeops_{entity}_{today_str}.csv"

    return Response(
        content=csv_bytes,
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@router.get(
    "/export/excel",
    summary="Export all data into a multi-sheet Excel (.xlsx) workbook",
    response_description="Excel spreadsheet download",
)
@limiter.limit("10/minute")
def export_excel(
    request: Request,
    user: AuthenticatedUser = Depends(get_current_user),
):
    from services.data_exporter import export_full_excel
    buffer = export_full_excel(user.id)

    today_str = dt.date.today().strftime('%Y%m%d')
    filename = f"LifeOps_Backup_Completo_{today_str}.xlsx"

    return Response(
        content=buffer.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )
