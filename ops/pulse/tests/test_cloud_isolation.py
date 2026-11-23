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


def test_admin_snapshot_rls_and_graceful_sync(monkeypatch):
    """Verifica el RLS estricto de pulse.private_snapshot y degradación limpia sin clave."""
    admin_sql_file = ROOT_DIR / "ops" / "pulse" / "migrations" / "002_admin_snapshot_rls.sql"
    assert admin_sql_file.exists(), "Falta ops/pulse/migrations/002_admin_snapshot_rls.sql"

    sql = admin_sql_file.read_text(encoding="utf-8")
    assert "CREATE TABLE IF NOT EXISTS pulse.private_snapshot" in sql
    assert "ALTER TABLE pulse.private_snapshot ENABLE ROW LEVEL SECURITY;" in sql
    assert "auth.jwt() ->> 'email'" in sql
    assert "dalaez1@gmail.com" in sql
    assert "REVOKE ALL ON pulse.private_snapshot FROM anon;" in sql
    assert "GRANT ALL ON pulse.private_snapshot TO service_role;" in sql
    assert "NOTIFY pgrst, 'reload config';" in sql

    import ops.pulse.sync_admin_snapshot as sync_mod

    monkeypatch.delenv("SUPABASE_SERVICE_ROLE_KEY", raising=False)
    monkeypatch.setattr(sync_mod, "_load_env_fallback", lambda: {})
    ok, msg = sync_mod.sync_admin_snapshot(service_role_key="")
    assert ok is False
    assert "SKIP" in msg

    opaque_hdrs = sync_mod.build_supabase_headers("sb_secret_dummy_test_key")
    assert opaque_hdrs["apikey"] == "sb_secret_dummy_test_key"
    assert "Authorization" not in opaque_hdrs

    jwt_hdrs = sync_mod.build_supabase_headers("aaa.bbb.ccc")
    assert jwt_hdrs["Authorization"] == "Bearer aaa.bbb.ccc"


def test_inv_pulse_10_no_hardcoded_demo_password_in_source_or_static():
    """INV-PULSE-10: Ninguna contraseña literal puede vivir en código cliente, bundle estático ni seed_demo.py."""
    forbidden_patterns = [
        re.compile("Demo" + "User2026!?"),
        re.compile(r"""['"]password['"]?\s*[:=]\s*['"][^'"]+['"]""", re.I),
        re.compile(r"""\bpassword\s*[:=]\s*['"][^'"]{4,}['"]""", re.I),
    ]

    targets = [
        ROOT_DIR / "apps" / "pulse" / "web" / "src" / "lib" / "supabase.ts",
        ROOT_DIR / "apps" / "pulse" / "web" / "src" / "App.tsx",
        ROOT_DIR / "ops" / "pulse" / "seed_demo.py",
    ]
    static_assets_dir = ROOT_DIR / "static" / "apps" / "pulse" / "assets"
    if static_assets_dir.is_dir():
        targets.extend(static_assets_dir.glob("*.js"))

    for file_path in targets:
        assert file_path.exists(), f"Archivo esperado ausente: {file_path}"
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        for pat in forbidden_patterns:
            match = pat.search(content)
            assert match is None, (
                f"Credencial hardcoded prohibida por INV-PULSE-10 en {file_path}: {match.group(0)}"
            )


def test_admin_omnichannel_snapshot_and_public_json_firewall_inv_pulse_2_9_12():
    """Hito 7.14: Verifica payload privado RLS omnicanal, cero fuga en public.json y paridad i18n ES/EN."""
    import json
    from ops.pulse.sync_admin_snapshot import build_omnichannel_intelligence_payload

    omni = build_omnichannel_intelligence_payload()
    assert omni["is_synthetic"] is False
    assert omni["roi_formula_version"] == "v2"
    assert omni["x_standby_zero_cost"] is True
    assert "funnel_4_layers" in omni
    assert "social_funnel" in omni
    assert "channel_category_matrix" in omni
    assert "top_recommendations" in omni

    public_json = ROOT_DIR / "static" / "apps" / "pulse" / "data" / "public.json"
    if public_json.is_file():
        raw = public_json.read_text(encoding="utf-8")
        for forbidden in (
            "omnichannel_intelligence",
            "channel_metrics",
            "social_metrics",
            "distribution_ledger",
        ):
            assert forbidden not in raw, f"Fuga prohibida '{forbidden}' detectada en public.json"

        parsed = json.loads(raw)
        assert "omnichannel_intelligence" not in parsed

    # Paridad estricta de claves ES/EN en apps/pulse/web/src/lib/i18n.ts
    i18n_ts = (ROOT_DIR / "apps" / "pulse" / "web" / "src" / "lib" / "i18n.ts").read_text(encoding="utf-8")
    es_section = i18n_ts.split("es: {", 1)[1].split("en: {", 1)[0]
    en_section = i18n_ts.split("en: {", 1)[1]
    es_keys = set(re.findall(r"^\s*([a-zA-Z0-9_]+):", es_section, flags=re.M))
    en_keys = set(re.findall(r"^\s*([a-zA-Z0-9_]+):", en_section, flags=re.M))
    assert es_keys == en_keys, f"Asimetría i18n ES vs EN: diff={es_keys ^ en_keys}"

