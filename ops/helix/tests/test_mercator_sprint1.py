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
    assert data["cross_sell_coupon_spec"]["code"] == "DATALARIA-UPGRADE20"

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
