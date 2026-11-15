import pytest
from conftest import log_api


@pytest.mark.api
def test_delete_course(api_context):
    res = api_context.delete("/api/courses/101")
    log_api("DELETE", "/api/courses/101", res)
    assert res.status in (200, 204)


@pytest.mark.api
def test_get_course_by_id(api_context):
    res = api_context.get("/api/courses/101")
    log_api("GET", "/api/courses/101", res)
    assert res.status == 200
    assert res.json()["id"] == 101
