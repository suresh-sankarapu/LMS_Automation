import pytest
from conftest import log_api


@pytest.mark.api
def test_create_course(api_context):
    payload = {"title": "API Testing"}
    res = api_context.post("/api/courses", data=payload)
    log_api("POST", "/api/courses", res, payload)
    assert res.status == 201
    assert res.json()["title"] == "API Testing"


@pytest.mark.api
def test_create_invalid_course(api_context):
    payload = {}
    res = api_context.post("/api/courses", data=payload)
    log_api("POST", "/api/courses", res, payload)
    assert res.status == 400
