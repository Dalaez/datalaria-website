"""
Agentic PMO Sandbox - Sample Excel Generator
=============================================
Generates a sample .xlsx payload for testing the ingestion pipeline.
Run this script directly: python generate_sample_excel.py
"""
import pandas as pd
from datetime import date


def generate():
    """Creates sample_project.xlsx with 3 sheets: Project, Resources, Tasks."""

    # --- Project Sheet (single row) ---
    df_project = pd.DataFrame([{
        "project_code": "PROJ-TITAN-001",
        "project_name": "Titanium Chassis Assembly Line v2",
        "description": "Redesign of the primary structural chassis for the X-500 platform. Mil-Spec compliance required.",
        "budget_allocated": 2500000.00,
        "start_date": date(2026, 4, 1),
        "end_date": date(2026, 12, 31),
    }])

    # --- Resources Sheet ---
    df_resources = pd.DataFrame([
        {"resource_code": "ENG-SR-001", "resource_name": "Lead Structural Engineer", "resource_type": "ENGINEER", "standard_cost_rate": 95.00},
        {"resource_code": "ENG-SR-002", "resource_name": "Senior FEA Analyst", "resource_type": "ENGINEER", "standard_cost_rate": 88.00},
        {"resource_code": "ENG-JR-003", "resource_name": "Junior Test Engineer", "resource_type": "ENGINEER", "standard_cost_rate": 55.00},
        {"resource_code": "MCH-CNC-001", "resource_name": "5-Axis CNC Mill (Haas UMC-750)", "resource_type": "MACHINE", "standard_cost_rate": 150.00},
        {"resource_code": "VND-TI-001", "resource_name": "VSMPO-AVISMA (Titanium Supplier)", "resource_type": "VENDOR", "standard_cost_rate": 0.00},
    ])

    # --- Tasks Sheet (WBS) ---
    df_tasks = pd.DataFrame([
        {"project_code": "PROJ-TITAN-001", "task_code": "WBS-1.0", "task_name": "Requirements Freeze & Kick-Off", "planned_duration_hours": 80, "planned_cost": 15000.00, "dependency_task_code": None},
        {"project_code": "PROJ-TITAN-001", "task_code": "WBS-2.0", "task_name": "Preliminary Design Review (PDR)", "planned_duration_hours": 320, "planned_cost": 65000.00, "dependency_task_code": "WBS-1.0"},
        {"project_code": "PROJ-TITAN-001", "task_code": "WBS-3.0", "task_name": "Critical Design Review (CDR)", "planned_duration_hours": 480, "planned_cost": 120000.00, "dependency_task_code": "WBS-2.0"},
        {"project_code": "PROJ-TITAN-001", "task_code": "WBS-4.0", "task_name": "FEA Simulation & Fatigue Analysis", "planned_duration_hours": 600, "planned_cost": 180000.00, "dependency_task_code": "WBS-3.0"},
        {"project_code": "PROJ-TITAN-001", "task_code": "WBS-5.0", "task_name": "Titanium Billet Procurement", "planned_duration_hours": 200, "planned_cost": 750000.00, "dependency_task_code": "WBS-3.0"},
        {"project_code": "PROJ-TITAN-001", "task_code": "WBS-6.0", "task_name": "CNC Machining (Prototype)", "planned_duration_hours": 400, "planned_cost": 350000.00, "dependency_task_code": "WBS-5.0"},
        {"project_code": "PROJ-TITAN-001", "task_code": "WBS-7.0", "task_name": "NDT Inspection & Quality Gate", "planned_duration_hours": 160, "planned_cost": 95000.00, "dependency_task_code": "WBS-6.0"},
        {"project_code": "PROJ-TITAN-001", "task_code": "WBS-8.0", "task_name": "Environmental Stress Screening (ESS)", "planned_duration_hours": 240, "planned_cost": 130000.00, "dependency_task_code": "WBS-7.0"},
        {"project_code": "PROJ-TITAN-001", "task_code": "WBS-9.0", "task_name": "Mil-Spec Certification Package", "planned_duration_hours": 320, "planned_cost": 200000.00, "dependency_task_code": "WBS-8.0"},
        {"project_code": "PROJ-TITAN-001", "task_code": "WBS-10.0", "task_name": "Production Readiness Review (PRR)", "planned_duration_hours": 120, "planned_cost": 85000.00, "dependency_task_code": "WBS-9.0"},
    ])

    output_path = "sample_project.xlsx"
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df_project.to_excel(writer, sheet_name="Project", index=False)
        df_resources.to_excel(writer, sheet_name="Resources", index=False)
        df_tasks.to_excel(writer, sheet_name="Tasks", index=False)

    print(f"Sample Excel generated: {output_path}")
    print(f"  - Project: {df_project['project_code'].iloc[0]}")
    print(f"  - Resources: {len(df_resources)} rows")
    print(f"  - WBS Tasks: {len(df_tasks)} rows")
    print(f"  - Total Budget: €{df_project['budget_allocated'].iloc[0]:,.2f}")


if __name__ == "__main__":
    generate()
