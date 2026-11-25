"""Tests for Hito 9.3 — Primer Sprint Comercial de Datalaria Mercator (M02/M03/M04)."""
from __future__ import annotations

import pathlib
import re

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]


def test_mercator_sprint1_spec_exists_and_complete() -> None:
    spec_path = REPO_ROOT / "specs" / "growth" / "mercator-sprint-1" / "spec.md"
    assert spec_path.exists(), "Missing SDD spec for Hito 9.3"
    text = spec_path.read_text(encoding="utf-8")
    for token in (
        "INV-AUTO-6",
        "OPP-MON-01",
        "DATALARIA-UPGRADE20",
        "UPGRADE20",
        "lemonsqueezy-webhook",
        "99 €",
        "149 €",
        "data/growth/lifecycle_flows.yaml",
        "data/growth/launch_pack_obs_helix.yaml",
    ):
        assert token in text, f"Missing expected token '{token}' in sprint 1 spec"


def test_lifecycle_flows_yaml_valid_bilingual_and_zero_mailto() -> None:
    path = REPO_ROOT / "data" / "growth" / "lifecycle_flows.yaml"
    assert path.exists(), "Missing data/growth/lifecycle_flows.yaml"
    raw = path.read_text(encoding="utf-8")
    assert "mailto:" not in raw.lower(), "mailto: links are forbidden (INV-HELIX-WL-4)"

    data = yaml.safe_load(raw)
    assert data["brevo_constraints"]["monthly_cost_eur"] == 0
    assert data["brevo_constraints"]["min_text_to_image_ratio_pct"] >= 80
    assert data["cross_sell_coupon_spec"]["name"] == "DATALARIA-UPGRADE20"
    assert data["cross_sell_coupon_spec"]["code"] == "UPGRADE20"

    flows = {f["id"]: f for f in data["flows"]}
    assert set(flows.keys()) == {
        "welcome_segmented",
        "helix_waitlist_nurture",
        "post_purchase_lemonsqueezy",
    }
    assert len(flows["welcome_segmented"]["emails"]) == 4
    assert len(flows["helix_waitlist_nurture"]["emails"]) == 3
    assert len(flows["post_purchase_lemonsqueezy"]["emails"]) == 3
    assert flows["helix_waitlist_nurture"]["embargo_until"] == "2027-01-19"

    for flow in data["flows"]:
        for email in flow["emails"]:
            assert "es" in email and "en" in email, f"Missing ES/EN parity in {flow['id']} step {email['step']}"
            for lang in ("es", "en"):
                assert email[lang]["subject"]
                assert email[lang]["cta_url"].startswith("https://datalaria.com/")
                assert "utm_source=brevo_auto" in email[lang]["cta_url"]


def test_launch_pack_obs_helix_yaml_en_first_embargo_and_linkedin_plan() -> None:
    path = REPO_ROOT / "data" / "growth" / "launch_pack_obs_helix.yaml"
    assert path.exists(), "Missing data/growth/launch_pack_obs_helix.yaml"
    raw = path.read_text(encoding="utf-8")
    assert "mailto:" not in raw.lower(), "mailto: links are forbidden"

    data = yaml.safe_load(raw)
    assert data["governance_rules"]["cost_eur"] == 0
    assert data["governance_rules"]["priority_language"] == "en"
    assert data["governance_rules"]["allow_scraping_or_li_at_cookie"] is False
    assert data["governance_rules"]["embargo_dates"]["pack_obs"] == "2026-12-09"
    assert data["governance_rules"]["embargo_dates"]["helix_pack_sdd"] == "2027-01-19"

    ph_ids = {item["product_id"] for item in data["product_hunt"]}
    assert {"pack-obs", "pack-sdd"} <= ph_ids

    hn_ids = {item["product_id"] for item in data["hacker_news_show_hn"]}
    assert {"pack-obs", "pack-sdd"} <= hn_ids

    subreddits = {item["subreddit"] for item in data["reddit_niche_playbooks"]}
    assert {"r/supplychain", "r/projectmanagement", "r/ClaudeAI", "r/Excel"} <= subreddits

    li_plan = data["linkedin_company_4week_plan"]
    assert len(li_plan["weeks"]) == 4
    total_posts = sum(len(w["posts"]) for w in li_plan["weeks"])
    assert total_posts >= 12
    for w in li_plan["weeks"]:
        for post in w["posts"]:
            assert "utm_source=linkedin" in post["cta_url"]
            assert "utm_medium=social" in post["cta_url"]


def test_recursos_cro_b2b_faq_beacon_and_zero_mailto() -> None:
    catalog_path = REPO_ROOT / "layouts" / "partials" / "recursos_catalog.html"
    es_index = REPO_ROOT / "content" / "es" / "recursos" / "_index.md"
    en_index = REPO_ROOT / "content" / "en" / "resources" / "_index.md"
    app_single = REPO_ROOT / "layouts" / "apps" / "single.html"

    for p in (catalog_path, es_index, en_index, app_single):
        text = p.read_text(encoding="utf-8")
        assert "mailto:" not in text.lower(), f"Forbidden mailto: found in {p}"

    for p in (es_index, en_index):
        text = p.read_text(encoding="utf-8")
        assert 'id="pricing-comparison"' in text
        assert 'id="b2b-team-license"' in text
        assert 'id="catalog-faq"' in text
        assert "transport_type: 'beacon'" in text
        assert "99" in text and "149" in text
        # MWG accordion invariant: no heading inside <summary>
        summaries = re.findall(r"<summary[^>]*>(.*?)</summary>", text, flags=re.S | re.I)
        assert len(summaries) == 5, f"Expected 5 FAQ <summary> items in {p}, got {len(summaries)}"
        for s in summaries:
            assert not re.search(r"<h[1-6]\b", s, flags=re.I), f"Heading inside <summary> violates MWG accordion in {p}"


def test_embargo_invariants_preserved_in_kits_yaml() -> None:
    kits_data = yaml.safe_load((REPO_ROOT / "data" / "pulse" / "kits.yaml").read_text(encoding="utf-8"))
    by_id = {k["id"]: k for k in kits_data["kits"]}
    suites_by_id = {s["id"]: s for s in kits_data["suites"]}

    assert by_id["pack-obs"]["status"] == "coming"
    assert by_id["pack-obs"]["checkout_url"] == "#"
    assert by_id["pack-obs"]["publish_date"] == "2026-12-09"

    assert by_id["pack-sdd"]["status"] == "coming"
    assert by_id["pack-sdd"]["checkout_url"] == "#"
    assert by_id["pack-sdd"]["publish_date"] == "2027-01-19"

    assert suites_by_id["suite-sdd"]["status"] == "coming"
    assert suites_by_id["suite-sdd"]["checkout_url"] == "#"
    assert suites_by_id["suite-sdd"]["publish_date"] == "2027-01-19"


def test_hito_9_5_utm_fragment_order_and_activation_kit(tmp_path: pathlib.Path) -> None:
    """INV-MERCATOR-UTM-1 / E07 / INV-AUTO-6: valida UTMs antes de #fragment y compila 20 HTMLs Brevo + LinkedIn + Directorios."""
    from ops.growth.build_activation_kit import build_activation_kit, validate_utm_url

    summary = build_activation_kit(out_dir=tmp_path)
    assert summary["brevo_html_count"] == 20
    assert summary["linkedin_week1_2_count"] == 6
    assert summary["directories_count"] == 4

    brevo_dir = tmp_path / "brevo_html"
    html_files = sorted(brevo_dir.glob("*.html"))
    assert len(html_files) == 20
    for hf in html_files:
        doc = hf.read_text(encoding="utf-8")
        assert "mailto:" not in doc.lower()
        assert "{{ unsubscribe }}" in doc
        assert "utm_source=brevo_auto" in doc

    # LinkedIn Semanas 1-2 cumplen E07 (párrafos separados y pregunta de debate final)
    launch_data = yaml.safe_load((REPO_ROOT / "data" / "growth" / "launch_pack_obs_helix.yaml").read_text(encoding="utf-8"))
    for wk in launch_data["linkedin_company_4week_plan"]["weeks"]:
        if int(wk["week"]) <= 2:
            for post in wk["posts"]:
                full_post = str(post.get("full_post") or "").strip()
                assert "\n\n" in full_post, f"Falta doble salto E07 en LinkedIn W{wk['week']} {post['day']}"
                assert full_post.endswith("?"), f"Falta pregunta de debate final E07 en LinkedIn W{wk['week']} {post['day']}"

    # Directorios Hito 9.5 apuntan exclusivamente a activos LIVE (nunca pack-sdd ni pack-obs)
    dirs = launch_data["directories_and_marketplaces"]["ai_and_devtools_directories"]
    assert len(dirs) == 4
    for d in dirs:
        assert d["hito_9_5_ready"] is True
        assert "pack-sdd" not in d["target_products"]
        assert "pack-obs" not in d["target_products"]
        validate_utm_url(d["tracked_url"], d["name"])

    # Verificar rechazo ante URL malformada (#fragment?utm_...)
    import pytest
    with pytest.raises(ValueError, match="INV-MERCATOR-UTM-1"):
        validate_utm_url("https://datalaria.com/es/recursos/#mega-bundle?utm_source=brevo_auto&utm_medium=email", "bad")

    # Verificar que los HTMLs de post-compra Step 3 usan el código checkout exacto UPGRADE20
    for lang in ("es", "en"):
        step3_html = (brevo_dir / f"post_purchase_lemonsqueezy_step3_{lang}.html").read_text(encoding="utf-8")
        assert "UPGRADE20" in step3_html
        assert "DATALARIA-UPGRADE20" not in step3_html


def test_lemonsqueezy_webhook_node_suite_passes() -> None:
    """INV-MERCATOR-WH-1 / INV-PULSE-13: ejecuta suite Node.js determinista sobre netlify/functions/lemonsqueezy-webhook.js."""
    import subprocess
    res = subprocess.run(
        ["node", "--test", str(REPO_ROOT / "ops" / "growth" / "test_lemonsqueezy_webhook.cjs")],
        capture_output=True,
        text=True,
        check=False,
    )
    assert res.returncode == 0, f"Webhook Node tests failed:\n{res.stdout}\n{res.stderr}"
