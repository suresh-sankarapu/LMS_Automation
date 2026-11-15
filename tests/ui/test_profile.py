import pytest
from pages.profile_page import ProfilePage
from pages.dashboard_page import DashboardPage


@pytest.mark.ui
@pytest.mark.regression
#update profile with data 
def test_update_profile(page, base_url):
    profile = ProfilePage(page)
    page.goto(f"{base_url}/profile")
    profile.update("Alex", "alex@test.com", "NewPass123!")
    assert "Updated" in profile.get_success()

#navigate to dashboard 
@pytest.mark.ui
@pytest.mark.regression
def test_page_navigation(page, base_url):
    page.goto(f"{base_url}/dashboard")
    page.click("#profile-link")
    assert "/profile" in page.url

#validate course count as 2 
@pytest.mark.ui
@pytest.mark.regression
def test_dashboard_courses(page, base_url):
    dashboard = DashboardPage(page)
    page.goto(f"{base_url}/dashboard")
    assert dashboard.get_course_count() == 2

#Validate the progress as 75 percent 
@pytest.mark.ui
@pytest.mark.smoke
def test_dashboard_progress(page, base_url):
    dashboard = DashboardPage(page)
    page.goto(f"{base_url}/dashboard")
    assert dashboard.get_progress() == "75"
