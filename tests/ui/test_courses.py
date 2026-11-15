import pytest
from pages.courses_page import CoursesPage

#search course
@pytest.mark.ui
@pytest.mark.smoke
def test_search_course(page, base_url):
    courses = CoursesPage(page)
    courses.open(base_url)
    courses.search("Python")
    assert page.locator("#c1").is_visible()

#Filter course 
@pytest.mark.ui
@pytest.mark.regression
def test_filter_courses(page, base_url):
    courses = CoursesPage(page)
    courses.open(base_url)
    courses.filter_by("QA")
    assert page.locator("#c2").is_visible()

#open first course 
@pytest.mark.ui
@pytest.mark.regression
def test_open_course_details(page, base_url):
    courses = CoursesPage(page)
    courses.open(base_url)
    courses.open_first_course()
    assert "Course Details" in page.locator(".details").inner_text()
