   #Intilaize page through constructor 
class LoginPage:
    def __init__(self, page):
        self.page = page
    # trigger to go to the url
    def open(self, url):
        self.page.goto(f"{url}/login")
    # login method for the username and password ,button
    def login(self, username, password):
        self.page.fill("#username", username)
        self.page.fill("#password", password)
        self.page.click("#login-btn")
     #Error call for the error text
    def get_error(self):
        return self.page.locator(".error").inner_text()
