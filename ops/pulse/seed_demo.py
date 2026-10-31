"""
ops/pulse/seed_demo.py
---------------------
Script de verificación y siembra (seeding) de la cuenta Demo de Datalaria Pulse Pro en Supabase.
Verifica la existencia del usuario demo@datalaria.com, confirma su email y puebla ideas sintéticas en pulse.ideas.
"""

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

# Raíz del proyecto
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Extraer variables de Supabase desde apps/lifeops/api/.env si no están en entorno
def load_supabase_credentials():
    url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    env_file = ROOT_DIR / "apps" / "lifeops" / "api" / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("SUPABASE_URL=") and not url:
                    url = line.split("=", 1)[1].strip()
                elif line.startswith("SUPABASE_SERVICE_ROLE_KEY=") and not service_key:
                    service_key = line.split("=", 1)[1].strip()

    if not url:
        url = "https://wkbmxekmofrjtcsyytrv.supabase.co"
    if not service_key:
        print("[ERROR] No se encontró SUPABASE_SERVICE_ROLE_KEY en el entorno ni en apps/lifeops/api/.env")
        sys.exit(1)

    return url, service_key


def get_or_create_demo_user(url: str, service_key: str) -> str:
    """Asegura que el usuario demo@datalaria.com exista y tenga su email confirmado."""
    headers = {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
    }

    # 1. Buscar si ya existe el usuario
    list_url = f"{url}/auth/v1/admin/users"
    req = urllib.request.Request(list_url, headers=headers, method="GET")
    demo_user_id = None

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            users = data.get("users", [])
            for u in users:
                if u.get("email") == "demo@datalaria.com":
                    demo_user_id = u.get("id")
                    if not u.get("email_confirmed_at"):
                        # Confirmar email
                        confirm_url = f"{url}/auth/v1/admin/users/{demo_user_id}"
                        c_data = json.dumps({"email_confirm": True}).encode("utf-8")
                        c_req = urllib.request.Request(confirm_url, data=c_data, headers=headers, method="PUT")
                        urllib.request.urlopen(c_req)
                        print(f"[DEMO AUTH] Usuario demo@datalaria.com confirmado exitosamente.")
                    else:
                        print(f"[DEMO AUTH] Usuario demo@datalaria.com ya existe y está confirmado (UUID: {demo_user_id}).")
                    break
    except Exception as e:
        print(f"[WARN] Error consultando lista de usuarios admin: {e}")

    # 2. Si no existe, crearlo directamente
    if not demo_user_id:
        create_url = f"{url}/auth/v1/admin/users"
        payload = json.dumps({
            "email": "demo@datalaria.com",
            "password": "DemoUser2026!",
            "email_confirm": True,
            "user_metadata": {"full_name": "Usuario Demo Datalaria Pulse"}
        }).encode("utf-8")
        req = urllib.request.Request(create_url, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            demo_user_id = data.get("id")
            print(f"[DEMO AUTH] Creado nuevo usuario demo@datalaria.com (UUID: {demo_user_id}).")

    return demo_user_id


def seed_demo_ideas(url: str, service_key: str, user_id: str):
    """Siembra ideas sintéticas de prueba en pulse.ideas para la cuenta demo."""
    headers = {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
        "Accept-Profile": "pulse",
        "Content-Profile": "pulse",
        "Prefer": "return=representation"
    }

    # Verificar si pulse.ideas está accesible en la API
    check_url = f"{url}/rest/v1/ideas?user_id=eq.{user_id}"
    req = urllib.request.Request(check_url, headers=headers, method="GET")

    try:
        with urllib.request.urlopen(req) as resp:
            existing = json.loads(resp.read().decode())
            if existing:
                print(f"[DEMO SEED] La cuenta demo ya tiene {len(existing)} ideas sincronizadas en Supabase.")
                for item in existing:
                    print(f"  - [{item.get('status').upper()}] {item.get('title')} ({item.get('target_date') or 'Sin fecha'})")
                return True
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode()
        if e.code == 406 or "Invalid schema" in err_msg:
            print("\n" + "="*80)
            print("[ATENCIÓN] El esquema 'pulse' aún no ha sido expuesto o creado en Supabase.")
            print("Para completar el despliegue del Hito 5.7:")
            print("1. Abre Supabase SQL Editor: https://supabase.com/dashboard/project/wkbmxekmofrjtcsyytrv/sql")
            print("2. Copia y ejecuta el archivo: ops/pulse/migrations/001_create_pulse_schema.sql")
            print("="*80 + "\n")
            return False
        else:
            print(f"[ERROR HTTP {e.code}] {err_msg}")
            return False

    # Insertar ideas sintéticas
    ideas_payload = [
        {
            "user_id": user_id,
            "title": "Modelado Financiero DCF: Descuento de Flujos de Caja para Startups B2B",
            "notes": "Tutorial paso a paso con plantilla Excel descargable y fórmulas dinámicas de WACC.",
            "category": "Finanzas Corporativas",
            "tags": ["finanzas", "dcf", "excel", "b2b"],
            "status": "scheduled",
            "target_date": "2026-11-20"
        },
        {
            "user_id": user_id,
            "title": "Arquitectura Agéntica Multimodelo: Coordinando Claude 3.7 y Gemini 2.5 Argon",
            "notes": "Benchmarking de latencia y costes en pipelines de desarrollo con SDD.",
            "category": "Inteligencia Artificial",
            "tags": ["ia", "agentes", "sdd", "deepmind"],
            "status": "draft",
            "target_date": "2026-11-25"
        },
        {
            "user_id": user_id,
            "title": "Guía S&OP: Del Plan de Demanda a la Capacidad de Planta con Python",
            "notes": "Fórmulas de previsión probabilística y reconciliación de inventarios.",
            "category": "Control Operativo",
            "tags": ["sop", "operaciones", "python", "sc"],
            "status": "idea",
            "target_date": None
        }
    ]

    insert_url = f"{url}/rest/v1/ideas"
    data = json.dumps(ideas_payload).encode("utf-8")
    ins_req = urllib.request.Request(insert_url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(ins_req) as resp:
            created = json.loads(resp.read().decode())
            print(f"[DEMO SEED] Sembradas {len(created)} ideas sintéticas con éxito en pulse.ideas:")
            for item in created:
                print(f"  - [{item.get('status').upper()}] {item.get('title')} ({item.get('target_date') or 'Sin fecha'})")
            return True
    except urllib.error.HTTPError as e:
        print(f"[ERROR SEEDING] {e.code}: {e.read().decode()}")
        return False


def main():
    print("[PULSE PRO] Verificando entorno Supabase Cloud...")
    url, service_key = load_supabase_credentials()
    user_id = get_or_create_demo_user(url, service_key)
    success = seed_demo_ideas(url, service_key, user_id)
    if success:
        print("[PULSE PRO] Inicialización de cuenta Demo completada al 100%.")
    else:
        print("[PULSE PRO] Pendiente de ejecutar la migración SQL en Supabase.")


if __name__ == "__main__":
    main()
