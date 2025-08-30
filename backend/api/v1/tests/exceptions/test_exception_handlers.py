import pytest
from backend.api.v1.exceptions import (
    BaseCustomError,
    add_exception_handlers,
    api_exceptions,
    auth_exceptions,
    cloud_exceptions,
    core_exceptions,
    db_exceptions,
)
from backend.loguru_logger import logger_setup
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

logger_setup()

error_msg: str = "Internal Server Error. Our team is notified."


@pytest.fixture
def test_app():
    app = FastAPI()
    add_exception_handlers(app)

    # Routes that raise specific exceptions
    @app.get("/raise-http-error")
    async def raise_http():
        raise HTTPException(status_code=500, detail=error_msg)

    @app.get("/raise-api-error")
    async def raise_api():
        raise api_exceptions.ApiError(
            internal_message="Validation failed",
        )

    @app.get("/raise-auth-error")
    async def raise_auth():
        raise auth_exceptions.AuthError(
            internal_message="Validation failed",
        )

    @app.get("/raise-core-error")
    async def raise_core():
        raise core_exceptions.CoreError(
            internal_message="Validation failed",
        )

    @app.get("/raise-cloud-error")
    async def raise_cloud():
        raise cloud_exceptions.CloudError(
            internal_message="Validation failed",
        )

    @app.get("/raise-db-error")
    async def raise_db():
        raise db_exceptions.DbError(
            internal_message="DB timeout",
        )

    @app.get("/raise-base-error")
    async def raise_base():
        raise BaseCustomError(
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
    assert response.json() == {"message": error_msg}


def test_api_error_handler(test_client):
    response = test_client.get("/raise-api-error")
    assert response.status_code == 500
    assert response.json() == {"message": error_msg}


def test_auth_error_handler(test_client):
    response = test_client.get("/raise-auth-error")
    assert response.status_code == 401
    assert response.json() == {"message": "You are not authorized."}


def test_core_error_handler(test_client):
    response = test_client.get("/raise-core-error")
    assert response.status_code == 500
    assert response.json() == {"message": error_msg}


def test_cloud_error_handler(test_client):
    response = test_client.get("/raise-cloud-error")
    assert response.status_code == 500
    assert response.json() == {"message": error_msg}


def test_db_error_handler(test_client):
    response = test_client.get("/raise-db-error")
    assert response.status_code == 500
    assert response.json() == {"message": error_msg}


def test_base_error_handler(test_client):
    response = test_client.get("/raise-base-error")
    assert response.status_code == 500
    assert response.json() == {"message": error_msg}


def test_generic_error_handler(test_client):
    response = test_client.get("/raise-generic-error")
    assert response.status_code == 500
    assert response.json() == {"message": error_msg}
