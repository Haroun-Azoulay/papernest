from fastapi.testclient import TestClient
from app.main import app
from app.services import parsing_coords_gouv, read_csv, fetch_geocode
import pandas
import requests
import httpx


client = TestClient(app)


def test_parsing_coords_gouv():
    fakeData = {"features": [{"properties": {"x": 2.3522, "y": 48.8566}}]}
    result = parsing_coords_gouv(fakeData)
    assert isinstance(result, tuple)
    assert result == (2.3522, 48.8566)


def test_read_csv(tmp_path):
    x1 = 1000
    y1 = 1000
    csvFile = tmp_path / "mobil_coverage.csv"
    csvFile.write_text(
        "Operateur,2G,3G,4G,x,y\n" "Orange,1,0,0,1000,1000\n" "SFR,0,0,0,2000,2000\n"
    )
    radii = {"2G": 30000, "3G": 5000, "4G": 10000}
    operators = ("Orange", "SFR", "Bouygues")

    dataFrame = pandas.read_csv(csvFile)
    deltaX = dataFrame["x"] - x1
    deltaY = dataFrame["y"] - y1
    distanceSquared = deltaX * deltaX + deltaY * deltaY
    coverageResult = {
        operator: {tech: False for tech in radii} for operator in operators
    }

    for operator in operators:
        operatorMask = dataFrame["Operateur"].str.contains(
            operator, case=False, na=False
        )
        for tech, radius in radii.items():
            antennaMask = (
                (dataFrame[tech].eq(1))
                & operatorMask
                & (distanceSquared <= radius * radius)
            )
            coverageResult[operator][tech] = bool(antennaMask.any())

    assert isinstance(coverageResult, dict)
    assert coverageResult == {
        "Orange": {"2G": True, "3G": False, "4G": False},
        "SFR": {"2G": False, "3G": False, "4G": False},
        "Bouygues": {"2G": False, "3G": False, "4G": False},
    }


def test_fetchgeo_code():
    address = "12 chemin de la bezou 6540 Romagnat"

    response = requests.get(
        "https://data.geopf.fr/geocodage/search", params={"q": address}
    )

    assert response.status_code == 200


def test_fetchgeo_short_search():
    address = "ab"

    response = requests.get(
        "https://data.geopf.fr/geocodage/search", params={"q": address}
    )
    assert response.status_code == 400


def test_fetchgeo_json_invalid(monkeypatch):

    async def fake_get(self, *args, **kwargs):
        return httpx.Response(
            status_code=200,
            content=b"<<<not-json>>>",
            headers={"content-type": "application/json"},
        )

    monkeypatch.setattr(httpx.AsyncClient, "get", fake_get, raising=True)

    response = client.post(
        "/job-submission", json={"id": "14 chemin de la bezou 6540 romagnat"}
    )

    assert response.status_code == 502
    assert response.json()["detail"] == "API gouv returned an invalid JSON response."


def test_fetchgeo_no_data(monkeypatch):
    async def fake_get(self, *args, **kwargs):
        return httpx.Response(
            status_code=200,
            text="""{
    "type": "FeatureCollection",
    "features": [],
    "query": "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"}""",
            headers={"content-type": "application/json"},
        )

    monkeypatch.setattr(httpx.AsyncClient, "get", fake_get, raising=True)

    response = client.post(
        "/job-submission", json={"id": "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "No data for this address."


def test_fetchgeo_network(monkeypatch):
    async def fake_get(self, *args, **kwargs):
        raise httpx.RequestError("error")

    monkeypatch.setattr(httpx.AsyncClient, "get", fake_get, raising=True)

    response = client.post(
        "/job-submission", json={"id": "14 chemin de la bezou 6540 romagnat"}
    )
    assert response.status_code == 500
    assert response.json()["detail"].startswith("Error network:")


def test_fetchgeo_timeout_504(monkeypatch):
    async def fake_get(self, *args, **kwargs):
        raise httpx.ReadTimeout("timeout")

    monkeypatch.setattr(httpx.AsyncClient, "get", fake_get, raising=True)

    response = client.post(
        "/job-submission", json={"id": "14 chemin de la bezou 6540 romagnat"}
    )
    assert response.status_code == 504
    assert "timeout" in response.json()["detail"]
