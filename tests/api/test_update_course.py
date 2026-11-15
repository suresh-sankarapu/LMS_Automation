import pytest
from conftest import log_api


@pytest.mark.api
def test_put_course(api_context):
    payload = {"title": "Updated Python Course"}
    res = api_context.put("/api/courses/101", data=payload)
    log_api("PUT", "/api/courses/101", res, payload)
    assert res.status == 200
    assert res.json()["title"] == "Updated Python Course"


@pytest.mark.api
def test_patch_course(api_context):
    payload = {"status": "Archived"}
    res = api_context.patch("/api/courses/101", data=payload)
    log_api("PATCH", "/api/courses/101", res, payload)
    assert res.status == 200
    assert res.json()["status"] == "Archived"
