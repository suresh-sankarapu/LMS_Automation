class DashboardPage:
    def __init__(self, page):
        self.page = page
     #Describes welcome 
    def get_welcome(self):
        return self.page.locator(".welcome").inner_text()
    #Course card count for the courses defined 
    def get_course_count(self):
        return self.page.locator(".course-card").count()
     #progress bar for the course selected 
    def get_progress(self):
        return self.page.locator(".progress").first.get_attribute("value")
     #logout 
    def logout(self):
        self.page.click("#logout-btn")
