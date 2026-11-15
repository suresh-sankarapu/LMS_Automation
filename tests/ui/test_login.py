import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.test_data import TestData

#markeres smoke and regression for the Scenario 
@pytest.mark.ui
@pytest.mark.smoke
#for the Valid login testcase
def test_valid_login(page, base_url):
    login = LoginPage(page)
    dashboard = DashboardPage(page)
    login.open(base_url)
    login.login(*TestData.VALID_USER)
    page.goto(f"{base_url}/dashboard")
    assert "Welcome" in dashboard.get_welcome()

#2.	Verify login with invalid credentials from testdata
#2.	Verify login with empty credentials from testdata
@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize("username, password", TestData.INVALID_USERS)
def test_invalid_login(page, base_url, username, password):
    login = LoginPage(page)
    login.open(base_url)
    #login.login(TestData.INVALID_USERS)
    login.login(username, password)
    assert "Invalid" in login.get_error()

#Verify the logout 
@pytest.mark.ui
@pytest.mark.regression
def test_logout(page, base_url):
    dashboard = DashboardPage(page)
    page.goto(f"{base_url}/dashboard")
    dashboard.logout()
    assert page.locator("#login-btn").is_visible()
    #assert False