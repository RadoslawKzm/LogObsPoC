import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from backend.proj_exc import add_exception_handlers
from backend.proj_exc import api_exceptions
from backend.proj_exc import db_exceptions
from backend.proj_exc.base import BaseCustomError

@pytest.fixture
def test_app():
    app = FastAPI()
    add_exception_handlers(app)

    # Routes that raise specific exceptions
    @app.get("/raise-api-error")
    async def raise_api():
        raise api_exceptions.ApiError(
            internal_message="Validation failed",
        )

    @app.get("/raise-db-error")
    async def raise_db():
        raise db_exceptions.DbError(
            internal_message="DB timeout",
        )

    @app.get("/raise-custom-error")
    async def raise_custom():
        raise BaseCustomError(
            internal_message="Invalid custom rule",
        )

    @app.get("/raise-generic-error")
    async def raise_generic():
        raise RuntimeError("Unexpected error")

    return app


def test_api_error_handler(test_app):
    client = TestClient(test_app)
    response = client.get("/raise-api-error")
    assert response.status_code == 400
    assert response.json() == {"message": "Invalid request data"}


def test_db_error_handler(test_app):
    client = TestClient(test_app)
    response = client.get("/raise-db-error")
    assert response.status_code == 503
    assert response.json() == {"message": "Database unavailable"}


def test_custom_error_handler(test_app):
    client = TestClient(test_app)
    response = client.get("/raise-custom-error")
    assert response.status_code == 422
    assert response.json() == {"message": "Custom logic failed"}


def test_generic_error_handler(test_app):
    client = TestClient(test_app)
    response = client.get("/raise-generic-error")
    assert response.status_code == 500
    assert response.json() == {
        "message": "Team got notified and working on solution."
    }
