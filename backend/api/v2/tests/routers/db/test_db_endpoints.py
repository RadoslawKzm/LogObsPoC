from unittest.mock import AsyncMock, patch

import pytest
from backend.api.v2.routers.db.endpoints import db_router
from fastapi import FastAPI
from fastapi.testclient import TestClient

pytest_plugins = ["pytest_asyncio"]


# --- Fixtures ---
@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(db_router)
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


# --- Tests ---
@patch(
    "backend.database.PostgresImplementation.get_record",
    new_callable=AsyncMock,
)
@pytest.mark.asyncio
async def test_postgres_endpoint(mock_get_record, client, app):
    mock_get_record.return_value = {"id": 1, "value": "test"}
    response = client.get("/database/postgres")
    assert response.status_code == 200
    mock_get_record.assert_awaited_once()
    assert response.json() == {"id": 1, "value": "test"}


@patch(
    "backend.database.MongoImplementation.get_many_records",
    new_callable=AsyncMock,
)
@pytest.mark.asyncio
async def test_mongo_endpoint(mock_get_many_records, client, app):
    mock_get_many_records.return_value = [{"id": 1}, {"id": 2}]
    response = client.get("/database/mongo")
    assert response.status_code == 200
    mock_get_many_records.assert_awaited_once()
    assert response.json() == [{"id": 1}, {"id": 2}]


@pytest.mark.asyncio
async def test_mock_endpoint(client, app):
    response = client.get("/database/mock")
    assert response.status_code == 200
    assert response.json() == 1
