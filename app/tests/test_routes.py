from fastapi.testclient import TestClient
from app.main import app
from app.routes import create_job
from uuid import uuid4
import httpx
import app.services as services

client = TestClient(app)


def test_create_job():
    response = client.post(
        "/job-submission", json={"id": "14 chemin de la bezou 6540 romagnat"}
    )
    assert response.status_code == 200
    data = response.json()
    assert response.json() == {
        "jobsUUID": data["jobsUUID"],
        "jobs": {
            "id": {
                "Orange": {"2G": True, "3G": True, "4G": True},
                "SFR": {"2G": True, "3G": True, "4G": True},
                "Bouygues": {"2G": True, "3G": True, "4G": True},
            }
        },
    }


def test_create_job_network(monkeypatch):

    async def raise_request_error_async(self, *args, **kwargs):
        raise httpx.RequestError("error")

    monkeypatch.setattr(
        services, "fetch_geocode", raise_request_error_async, raising=True
    )

    response = client.post(
        "/job-submission",
        json={"id": "14 chemin de la bezou 6540 romagnat"},
    )

    assert response.status_code == 500
    detail = response.json()["detail"]
    assert detail.startswith("Error network: ")
