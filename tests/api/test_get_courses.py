import pytest
from conftest import log_api


@pytest.mark.api
def test_get_all_courses(api_context):
    res = api_context.get("/api/courses")
    log_api("GET", "/api/courses", res)
    assert res.status == 200
    assert len(res.json()) == 2


@pytest.mark.api
def test_get_invalid_course(api_context):
    res = api_context.get("/api/courses/999")
    log_api("GET", "/api/courses/999", res)
    assert res.status == 404
