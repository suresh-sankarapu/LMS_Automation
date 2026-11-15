class ProfilePage:
    def __init__(self, page):
        self.page = page
     #update the details of name,email,password for the profile
    def update(self, name, email, password):
        self.page.fill("#name", name)
        self.page.fill("#email", email)
        self.page.fill("#password", password)
        self.page.click("#save-btn")
     # success on profile update 
    def get_success(self):
        return self.page.locator(".success").inner_text()
