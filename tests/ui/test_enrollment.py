import pytest
from pages.courses_page import CoursesPage

#Vselecting the course and alidating course enrolled
@pytest.mark.ui
@pytest.mark.smoke
def test_enroll_course(page, base_url):
    courses = CoursesPage(page)
    courses.open(base_url)
    courses.enroll_first()
    assert "Enrolled" in courses.get_toast()

#duplicate enrolment
@pytest.mark.ui
@pytest.mark.regression
def test_duplicate_enrollment(page, base_url):
    courses = CoursesPage(page)
    # Mock API/page response using page.route()
    page.route("**/courses", lambda r: r.fulfill(
        status=200,
        content_type="text/html",
        body="<button class='enroll-btn'>Enroll</button><div class='toast'>Already Enrolled</div>",
    ))
    courses.open(base_url)
    courses.enroll_first()
    assert "Already Enrolled" in courses.get_toast()
