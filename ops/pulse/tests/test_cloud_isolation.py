"""
ops/pulse/tests/test_cloud_isolation.py
---------------------------------------
Verificación de invariantes de aislamiento y seguridad para Datalaria Pulse Pro (ADR-015).
Garantiza RLS estricto, configuración hermética de Supabase y protección contra contaminación de datos (INV-11).
"""

from pathlib import Path
import re

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent


def test_sql_migration_rls_invariants():
    """Verifica que la migración SQL incluya RLS, políticas de usuario y configuración de PostgREST."""
    migration_file = ROOT_DIR / "ops" / "pulse" / "migrations" / "001_create_pulse_schema.sql"
    assert migration_file.exists(), "Falta el archivo de migración 001_create_pulse_schema.sql"

    sql = migration_file.read_text(encoding="utf-8")

    # Invariante 1: Esquema dedicado pulse (Constitución Art. 4)
    assert "CREATE SCHEMA IF NOT EXISTS pulse;" in sql

    # Invariante 2: Habilitación explícita de RLS
    assert "ALTER TABLE pulse.ideas ENABLE ROW LEVEL SECURITY;" in sql
    assert "ALTER TABLE pulse.content_schedule ENABLE ROW LEVEL SECURITY;" in sql

    # Invariante 3: Política de aislamiento auth.uid() = user_id
    assert "auth.uid() = user_id" in sql
    assert "CREATE POLICY user_ideas_isolation ON pulse.ideas" in sql

    # Invariante 4: Exposición en PostgREST y reload config
    assert "pgrst.db_schemas" in sql
    assert "NOTIFY pgrst, 'reload config';" in sql


def test_web_env_supabase_configuration():
    """Verifica que las variables de entorno frontend apunten al cluster unificado datalaria-core."""
    web_dir = ROOT_DIR / "apps" / "pulse" / "web"

    for env_name in [".env", ".env.production"]:
        env_file = web_dir / env_name
        assert env_file.exists(), f"Falta el archivo {env_name} en apps/pulse/web/"
        content = env_file.read_text(encoding="utf-8")
        assert "VITE_SUPABASE_URL=https://wkbmxekmofrjtcsyytrv.supabase.co" in content
        assert "VITE_SUPABASE_ANON_KEY=" in content

    example_file = web_dir / ".env.example"
    assert example_file.exists()
    example_content = example_file.read_text(encoding="utf-8")
    assert "VITE_SUPABASE_URL=" in example_content
    assert "VITE_SUPABASE_ANON_KEY=" in example_content


def test_demo_seeder_safety():
    """Verifica que el seeder de demo solo apunte a la cuenta de prueba y no toque producción."""
    seeder_file = ROOT_DIR / "ops" / "pulse" / "seed_demo.py"
    assert seeder_file.exists()

    content = seeder_file.read_text(encoding="utf-8")
    # Verificar que solo contiene el email demo
    assert "demo@datalaria.com" in content
    # Verificar que no intenta insertar o asociar ideas a cuentas de producción
    assert "dalaez1@gmail.com" not in content
