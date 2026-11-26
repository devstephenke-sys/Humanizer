import pytest

from app.services.detection import DetectionService
from app.services.text_utils import missing_markers, word_count


def test_word_count_ignores_extra_space():
    assert word_count("  one   two\nthree ") == 3


def test_missing_citation_is_reported():
    warnings = missing_markers("Memory improves with sleep [1].", "Memory improves with sleep.")
    assert any("[1]" in item for item in warnings)


def test_detector_flags_stock_phrasing_more_than_a_casual_note():
    detector = DetectionService()
    stiff = detector.analyze(
        "Furthermore, it is important to note that regular exercise significantly improves cognitive function. "
        "Moreover, physical activity plays a crucial role in enhancing memory retention and neuroplasticity. "
        "In addition, it is essential to leverage a comprehensive routine in order to foster robust health. "
        "In conclusion, exercise remains a pivotal and multifaceted tool in today's wellness landscape.",
        "deep",
    )
    casual = detector.analyze(
        "I don't have a neat routine. Some weeks I walk the dog before dawn, and other weeks I skip it "
        "because the baby was up all night. My knee's been weird since March — stairs are fine, hills aren't. "
        "We still try. If it rains I just pace the hallway and call that enough.",
        "deep",
    )
    assert stiff.ai_likelihood > casual.ai_likelihood
    assert stiff.ai_likelihood >= 55
    assert casual.ai_likelihood <= 50
    assert stiff.sentences
    assert casual.short_text_warning
    assert "probabilistic" in stiff.disclaimer.lower() or "estimate" in stiff.disclaimer.lower()


@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["payments_enabled"] is False
    assert body["provider_configured"] is False


@pytest.mark.asyncio
async def test_write_requires_a_configured_model(client):
    response = await client.post("/api/write", json={"text": "Hello from a draft that is long enough.", "tool": "humanize"})
    assert response.status_code == 503
    assert "OPENAI_API_KEY" in response.json()["detail"]


@pytest.mark.asyncio
async def test_write_and_alternatives(client, mock_model):
    response = await client.post(
        "/api/write",
        json={"text": "Exercise helps memory according to one review [1].", "tool": "humanize", "intensity": 8, "profile": "plain"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "[1]" in body["text"]
    assert body["warnings"] == []
    assert "guarantee" in body["disclaimer"].lower()

    dropped = await client.post(
        "/api/write",
        json={"text": "See the review [1] for the claim.", "tool": "paraphrase", "preserve_citations": True},
    )
    assert dropped.status_code == 200
    assert dropped.json()["warnings"]

    alts = await client.post("/api/write/alternatives", json={"sentence": "Exercise helps memory."})
    assert alts.status_code == 200
    assert len(alts.json()["alternatives"]) == 2


@pytest.mark.asyncio
async def test_detect_endpoint(client):
    response = await client.post(
        "/api/detect",
        json={"text": "Short note.", "mode": "quick"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["sentences"] == []
    assert body["short_text_warning"]
    assert 0 <= body["ai_likelihood"] <= 100
    assert body["human_like"] == 100 - body["ai_likelihood"]


@pytest.mark.asyncio
async def test_validation_and_accounts_and_documents(client, mock_model):
    empty = await client.post("/api/write", json={"text": "   ", "tool": "grammar"})
    assert empty.status_code == 422

    register = await client.post(
        "/api/auth/register",
        json={"email": "ada@example.com", "password": "correct-horse", "display_name": "Ada"},
    )
    assert register.status_code == 200
    token = register.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    other = await client.post(
        "/api/auth/register",
        json={"email": "grace@example.com", "password": "correct-horse", "display_name": "Grace"},
    )
    other_headers = {"Authorization": f"Bearer {other.json()['token']}"}

    created = await client.post(
        "/api/documents",
        headers=headers,
        json={
            "title": "Memory note",
            "tool": "humanize",
            "input_text": "Exercise helps.",
            "output_text": "A walk helps.",
            "settings_json": "{\"intensity\": 5}",
        },
    )
    assert created.status_code == 200
    document_id = created.json()["id"]

    listing = await client.get("/api/documents", headers=headers)
    assert len(listing.json()) == 1

    hidden = await client.get(f"/api/documents/{document_id}", headers=other_headers)
    assert hidden.status_code == 404

    deleted = await client.delete(f"/api/documents/{document_id}", headers=headers)
    assert deleted.status_code == 204
    assert (await client.get("/api/documents", headers=headers)).json() == []

    bad_login = await client.post("/api/auth/login", json={"email": "ada@example.com", "password": "nope"})
    assert bad_login.status_code == 401


@pytest.mark.asyncio
async def test_docx_export(client):
    response = await client.post("/api/export/docx", json={"title": "Note", "text": "Hello draft."})
    assert response.status_code == 200
    assert "wordprocessingml" in response.headers["content-type"]
    assert response.content[:2] == b"PK"
