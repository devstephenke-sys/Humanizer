import os

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret"
os.environ["AI_PROVIDER"] = "openai"
os.environ["OPENAI_API_KEY"] = ""
os.environ["CORS_ORIGINS"] = "http://localhost:5173"

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as http:
        yield http


@pytest.fixture
def mock_model(monkeypatch):
    async def fake_complete(self, system: str, user: str, temperature: float, max_tokens: int) -> str:
        if "three different" in system:
            return '{"alternatives": ["Walking most days helps.", "A regular walk makes the difference."]}'
        if user.startswith("See the review"):
            return '{"text": "The review makes the claim."}'
        if "[1]" in user:
            return '{"text": "Walking most days supports memory [1]."}'
        return '{"text": "Walking most days supports memory more than people expect."}'

    monkeypatch.setattr("app.services.ai_provider.AIProviderService.complete", fake_complete)
