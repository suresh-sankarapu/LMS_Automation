class CoursesPage:
    def __init__(self, page):
        self.page = page
#Open and View 
    def open(self, url):
        self.page.goto(f"{url}/courses")
#Search 
    def search(self, text):
        self.page.fill("#search", text)
        self.page.press("#search", "Enter")
#filter 
    def filter_by(self, category):
        self.page.select_option("#category", label=category)
#select the first course
    def open_first_course(self):
        self.page.locator(".course-link").first.click()
#select and enroll the first course
    def enroll_first(self):
        self.page.locator(".enroll-btn").first.click()
#sucessfull enrolled.
    def get_toast(self):
        return self.page.locator(".toast").inner_text()
