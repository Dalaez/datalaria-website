"""
Agentic PMO Sandbox - EVM Engine (The Muscle)
==============================================
Pure mathematical calculations. Zero opinions.
Earned Value Management (EVM) and Monte Carlo simulation
using Pandas and NumPy exclusively.
"""
import numpy as np
import pandas as pd
from datetime import date, timedelta
from typing import List, Dict, Any, Optional

import db_tools
from models import EVMSnapshot, MonteCarloResult


def calculate_evm_snapshot(
    project_id: str,
    snapshot_date: Optional[date] = None,
) -> EVMSnapshot:
    """
    Calculates EVM metrics for a project at a given date.

    Planned Value (PV): Sum of planned_cost for tasks that should be
                        completed by snapshot_date (based on schedule).
    Earned Value (EV): Sum of (planned_cost * percent_complete) for all tasks.
    Actual Cost (AC):  Sum of actual_cost from fact_task_execution.

    CPI = EV / AC  (Cost efficiency. < 1.0 = over budget)
    SPI = EV / PV  (Schedule efficiency. < 1.0 = behind schedule)
    """
    if snapshot_date is None:
        snapshot_date = date.today()

    # Fetch project metadata
    project = db_tools.get_project_by_id(project_id)
    if not project:
        raise ValueError(f"Project '{project_id}' not found in dim_project.")

    # Fetch all tasks
    tasks = db_tools.get_tasks_by_project(project_id)
    if not tasks:
        raise ValueError(f"No tasks found for project '{project_id}'.")

    df_tasks = pd.DataFrame(tasks)

    # Fetch all execution records
    executions = db_tools.get_executions_by_project(project_id)
    df_exec = pd.DataFrame(executions) if executions else pd.DataFrame()

    # --- Planned Value (PV) ---
    # Simplified linear model: tasks are assumed to be scheduled proportionally
    # across the project timeline based on their order.
    total_planned_cost = df_tasks["planned_cost"].astype(float).sum()
    project_start = pd.to_datetime(project["start_date"]).date()
    project_end = (
        pd.to_datetime(project["end_date"]).date()
        if project.get("end_date")
        else project_start + timedelta(days=365)
    )
    total_days = max((project_end - project_start).days, 1)
    elapsed_days = max(min((snapshot_date - project_start).days, total_days), 0)
    pv = total_planned_cost * (elapsed_days / total_days)

    # --- Earned Value (EV) ---
    # EV = sum of (planned_cost × percent_complete) for each task
    if not df_exec.empty:
        # Get latest percent_complete per task
        df_exec["execution_date"] = pd.to_datetime(df_exec["execution_date"])
        latest_progress = df_exec.sort_values("execution_date").groupby(
            "task_id"
        ).last().reset_index()[["task_id", "percent_complete"]]

        df_merged = df_tasks.merge(
            latest_progress, on="task_id", how="left"
        )
        df_merged["percent_complete"] = df_merged["percent_complete"].fillna(0).astype(float)
    else:
        df_merged = df_tasks.copy()
        df_merged["percent_complete"] = 0.0

    df_merged["planned_cost"] = df_merged["planned_cost"].astype(float)
    ev = (df_merged["planned_cost"] * df_merged["percent_complete"]).sum()

    # --- Actual Cost (AC) ---
    ac = df_exec["actual_cost"].astype(float).sum() if not df_exec.empty else 0.0

    # --- Performance Indices ---
    cpi = ev / ac if ac > 0 else 1.0  # No cost yet → perfect efficiency
    spi = ev / pv if pv > 0 else 1.0  # No plan elapsed → on schedule

    snapshot = EVMSnapshot(
        project_id=project_id,
        snapshot_date=snapshot_date,
        planned_value=round(pv, 2),
        earned_value=round(ev, 2),
        actual_cost=round(ac, 2),
        cpi=round(cpi, 4),
        spi=round(spi, 4),
    )

    # Persist the snapshot to fact_evm_snapshot
    db_tools.insert_evm_snapshot({
        "project_id": project_id,
        "snapshot_date": snapshot_date.isoformat(),
        "planned_value": snapshot.planned_value,
        "earned_value": snapshot.earned_value,
        "actual_cost": snapshot.actual_cost,
        "cost_performance_index": snapshot.cpi,
        "schedule_performance_index": snapshot.spi,
    })

    return snapshot


def run_monte_carlo(
    project_id: str,
    iterations: int = 10000,
) -> MonteCarloResult:
    """
    Monte Carlo Schedule Simulation.

    For each task, models duration as a PERT distribution:
      - Optimistic: 0.7 × planned_duration
      - Most Likely: 1.0 × planned_duration
      - Pessimistic: 1.8 × planned_duration

    Simulates N iterations of the full critical path and returns
    P50, P85, P95 completion estimates and probability of on-time delivery.
    """
    project = db_tools.get_project_by_id(project_id)
    if not project:
        raise ValueError(f"Project '{project_id}' not found.")

    tasks = db_tools.get_tasks_by_project(project_id)
    if not tasks:
        raise ValueError(f"No tasks for project '{project_id}'.")

    df_tasks = pd.DataFrame(tasks)
    df_tasks["planned_duration_hours"] = df_tasks["planned_duration_hours"].astype(float)
    df_tasks["planned_cost"] = df_tasks["planned_cost"].astype(float)

    # PERT parameters per task
    optimistic = df_tasks["planned_duration_hours"].values * 0.7
    most_likely = df_tasks["planned_duration_hours"].values * 1.0
    pessimistic = df_tasks["planned_duration_hours"].values * 1.8

    # PERT mean and std for triangular approximation
    pert_mean = (optimistic + 4 * most_likely + pessimistic) / 6
    pert_std = (pessimistic - optimistic) / 6

    # Simulate
    rng = np.random.default_rng(seed=42)
    total_durations = np.zeros(iterations)

    for i in range(len(df_tasks)):
        samples = rng.normal(loc=pert_mean[i], scale=max(pert_std[i], 0.1), size=iterations)
        samples = np.maximum(samples, optimistic[i])  # Floor at optimistic
        total_durations += samples

    # Convert hours to working days (8h/day)
    total_days = total_durations / 8.0

    p50 = float(np.percentile(total_days, 50))
    p85 = float(np.percentile(total_days, 85))
    p95 = float(np.percentile(total_days, 95))

    # Planned duration
    project_start = pd.to_datetime(project["start_date"]).date()
    project_end = (
        pd.to_datetime(project["end_date"]).date()
        if project.get("end_date")
        else project_start + timedelta(days=365)
    )
    planned_working_days = max((project_end - project_start).days * 5 / 7, 1)

    prob_on_time = float(np.mean(total_days <= planned_working_days))

    # Expected cost overrun: if median duration exceeds plan
    total_budget = float(project["budget_allocated"])
    cost_rate_per_day = total_budget / planned_working_days if planned_working_days > 0 else 0
    cost_overrun = max(0, (p50 - planned_working_days) * cost_rate_per_day)

    return MonteCarloResult(
        project_id=project_id,
        iterations=iterations,
        p50_completion_days=round(p50, 1),
        p85_completion_days=round(p85, 1),
        p95_completion_days=round(p95, 1),
        probability_on_time=round(prob_on_time, 4),
        cost_overrun_expected=round(cost_overrun, 2),
    )
