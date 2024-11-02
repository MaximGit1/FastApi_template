import pytest
from fastapi.testclient import TestClient
from src.web import create_app

app = create_app()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
