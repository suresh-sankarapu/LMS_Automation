import pytest


@pytest.mark.ui
@pytest.mark.regression
#Registernew user 
def test_new_registration(page, base_url):
    page.goto(f"{base_url}/register")
    page.fill("#user", "newstudent")
    page.fill("#email", "student@test.com")
    page.fill("#pass1", "Pass123!")
    page.fill("#pass2", "Pass123!")
    page.click("#reg-btn")
    assert page.locator(".success").is_visible()

#validate mandatory fields with error 
@pytest.mark.ui
@pytest.mark.regression
def test_mandatory_fields(page, base_url):
    page.goto(f"{base_url}/register")
    page.click("#reg-btn")
    assert "required" in page.locator(".error").inner_text()

#validate the password mismatch 
@pytest.mark.ui
@pytest.mark.regression
def test_password_mismatch(page, base_url):
    page.goto(f"{base_url}/register")
    page.fill("#user", "newstudent")
    page.fill("#pass1", "Pass1")
    page.fill("#pass2", "Pass2")
    page.click("#reg-btn")
    assert "do not match" in page.locator(".error").inner_text()
