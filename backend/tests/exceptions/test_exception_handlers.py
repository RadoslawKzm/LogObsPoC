import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from backend import exceptions
from backend.api.config import settings
from backend.loguru_logger import logger_setup

logger_setup(settings)

error_msg: str = "Internal server error. Our team has been notified."


@pytest.fixture
def test_app():
    app = FastAPI()
    exceptions.add_handlers(app)

    # Routes that raise specific exceptions
    @app.get("/raise-http-error")
    async def raise_http():
        raise HTTPException(status_code=500, detail=error_msg)

    @app.get("/raise-api-error")
    async def raise_api():
        raise exceptions.api.ApiError(
            internal_message="Validation failed",
        )

    @app.get("/raise-auth-error")
    async def raise_auth():
        raise exceptions.auth.AuthError(
            internal_message="Validation failed",
        )

    @app.get("/raise-core-error")
    async def raise_core():
        raise exceptions.core.CoreError(
            internal_message="Validation failed",
        )

    @app.get("/raise-cloud-error")
    async def raise_cloud():
        raise exceptions.cloud.CloudError(
            internal_message="Validation failed",
        )

    @app.get("/raise-db-error")
    async def raise_db():
        raise exceptions.db.DbError(
            internal_message="DB timeout",
        )

    @app.get("/raise-base-error")
    async def raise_base():
        raise exceptions.BaseCustomError(
            internal_message="Invalid custom rule",
        )

    @app.get("/raise-generic-error")
    async def raise_generic():
        raise RuntimeError("Unexpected error")

    return app


@pytest.fixture
def test_client(test_app):
    return TestClient(test_app, raise_server_exceptions=False)


def test_http_error_handler(test_client):
    response = test_client.get("/raise-http-error")
    assert response.status_code == 500
    response = response.json()
    assert response["message"] == error_msg
    assert (
        response["internal_code"] == exceptions.BaseCustomError.internal_code
    )


def test_api_error_handler(test_client):
    response = test_client.get("/raise-api-error")
    assert response.status_code == 500
    response = response.json()
    assert response["message"] == error_msg
    assert response["internal_code"] == exceptions.api.ApiError.internal_code


def test_auth_error_handler(test_client):
    response = test_client.get("/raise-auth-error")
    assert response.status_code == 401
    response = response.json()
    assert response["message"] == "Authentication or authorization required."
    assert response["internal_code"] == exceptions.auth.AuthError.internal_code


def test_core_error_handler(test_client):
    response = test_client.get("/raise-core-error")
    assert response.status_code == 500
    response = response.json()
    assert response["message"] == error_msg
    assert response["internal_code"] == exceptions.core.CoreError.internal_code


def test_cloud_error_handler(test_client):
    response = test_client.get("/raise-cloud-error")
    assert response.status_code == 500
    response = response.json()
    assert response["message"] == error_msg
    assert (
        response["internal_code"] == exceptions.cloud.CloudError.internal_code
    )


def test_db_error_handler(test_client):
    response = test_client.get("/raise-db-error")
    assert response.status_code == 500
    response = response.json()
    assert response["message"] == error_msg
    assert response["internal_code"] == exceptions.db.DbError.internal_code


def test_base_error_handler(test_client):
    response = test_client.get("/raise-base-error")
    assert response.status_code == 500
    response = response.json()
    assert response["message"] == error_msg
    assert (
        response["internal_code"] == exceptions.BaseCustomError.internal_code
    )


def test_generic_error_handler(test_client):
    response = test_client.get("/raise-generic-error")
    assert response.status_code == 500
    response = response.json()
    assert response["message"] == error_msg
    assert (
        response["internal_code"] == exceptions.BaseCustomError.internal_code
    )
