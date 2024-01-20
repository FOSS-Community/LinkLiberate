from unittest.mock import Mock

from fastapi.testclient import TestClient

from src.link_liberate.main import app


def test_index_page():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "request" in response.context


def test_web():
    client = TestClient(app)
    response = client.get("/liberate")
    assert response.status_code == 200
    assert "request" in response.context


def test_web_post(mocker):
    # Patch the get_db function to return the db mock
    mocker.patch('src.link_liberate.database.Session_Local', return_value=Mock())
    client_mock = TestClient(app)
    response = client_mock.post("/liberate", data={"content": "valid_content"})
    assert response.status_code == 200



def test_get_link(mocker):
    # Patch the get_db function to return the db mock
    mocker.patch('src.link_liberate.database.Session_Local', return_value=Mock())
    client_mock = TestClient(app)
    response = client_mock.get("/valid_uuid", follow_redirects=False)
    assert response.status_code == 301
