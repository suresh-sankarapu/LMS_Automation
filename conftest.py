import os
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

# QA and Staging environment URLs
ENV = os.getenv("TEST_ENV", "qa").lower()
SLACK_URL = os.getenv("SLACK_WEBHOOK_URL", "")
ENV_URLS = {
    "qa": "http://localhost:8001",
    "staging": "http://localhost:8002",
}
#course data 
COURSES = [
    {"id": 101, "title": "Python Automation", "category": "Development", "status": "Active"},
    {"id": 102, "title": "Playwright Testing", "category": "QA", "status": "Active"},
]

#creating mock server for the URL
class SimpleMockServer(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def send_json(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def send_html(self, code, html):
        self.send_response(code)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def do_GET(self):
        # API Endpoints
        if self.path == "/api/courses":
            self.send_json(200, COURSES)
        elif self.path == "/api/courses/101":
            self.send_json(200, COURSES[0])
        elif self.path.startswith("/api/courses/"):
            self.send_json(404, {"error": "Course not found"})

        # UI HTML Pages
        elif self.path == "/login":
            self.send_html(200, """
                <input id="username" />
                <input id="password" />
                <button id="login-btn" onclick="document.body.innerHTML+='<div class=error>Invalid credentials</div>'">Login</button>
            """)
        elif self.path == "/register":
            self.send_html(200, """
                <input id="user" />
                <input id="email" />
                <input id="pass1" />
                <input id="pass2" />
                <button id="reg-btn" onclick="
                    let u = document.getElementById('user').value;
                    let p1 = document.getElementById('pass1').value;
                    let p2 = document.getElementById('pass2').value;
                    if (!u) document.body.innerHTML += '<div class=error>All fields required</div>';
                    else if (p1 !== p2) document.body.innerHTML += '<div class=error>Passwords do not match</div>';
                    else document.body.innerHTML += '<div class=success>Registered successfully</div>';
                ">Register</button>
            """)
        elif self.path == "/dashboard":
            self.send_html(200, """
                <h1 class="welcome">Welcome Student</h1>
                <div class="course-card">Python Automation <progress class="progress" value="75" max="100"></progress></div>
                <div class="course-card">Playwright Testing <progress class="progress" value="40" max="100"></progress></div>
                <a id="profile-link" href="/profile">Profile</a>
                <button id="logout-btn" onclick="window.location.href='/login'">Logout</button>
            """)
        elif self.path == "/courses":
            self.send_html(200, """
                <input id="search" onkeydown="if(event.key==='Enter') document.getElementById('c2').style.display='none'" />
                <select id="category" onchange="document.getElementById('c1').style.display='none'">
                    <option value="all">All</option>
                    <option value="qa">QA</option>
                </select>
                <div id="c1"><a class="course-link" href="/course/101">Python Automation</a></div>
                <div id="c2"><a class="course-link" href="/course/102">Playwright Testing</a></div>
                <button class="enroll-btn" onclick="document.body.innerHTML+='<div class=toast>Enrolled</div>'">Enroll</button>
            """)
        elif self.path == "/course/101":
            self.send_html(200, "<h1 class='details'>Course Details: Python Automation</h1>")
        elif self.path == "/profile":
            self.send_html(200, """
                <input id="name" />
                <input id="email" />
                <input id="password" />
                <button id="save-btn" onclick="document.body.innerHTML+='<div class=success>Profile Updated</div>'">Save</button>
            """)

    def do_POST(self):
        size = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(size) or "{}")
        if self.path == "/api/courses":
            if not body.get("title"):
                self.send_json(400, {"error": "Title is required"})
            else:
                self.send_json(201, {"id": 103, "title": body["title"]})

    def do_PUT(self):
        size = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(size) or "{}")
        if self.path == "/api/courses/101":
            self.send_json(200, {"id": 101, "title": body.get("title", "")})

    def do_PATCH(self):
        size = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(size) or "{}")
        if self.path == "/api/courses/101":
            self.send_json(200, {"id": 101, "status": body.get("status", "")})

    def do_DELETE(self):
        if self.path == "/api/courses/101":
            self.send_response(204)
            self.end_headers()


@pytest.fixture(scope="session")
def server_url():
    server = HTTPServer(("127.0.0.1", 0), SimpleMockServer)
    port = server.server_address[1]
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{port}"
    server.shutdown()


@pytest.fixture(scope="session")
def base_url(server_url):
    if os.getenv("USE_LIVE_ENV", "false").lower() == "true":
        return ENV_URLS.get(ENV, ENV_URLS["qa"])
    return server_url


@pytest.fixture
def page(context, request):
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    pg = context.new_page()
    yield pg

    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    if failed:
        os.makedirs("screenshots", exist_ok=True)
        os.makedirs("traces", exist_ok=True)
        name = "".join(c if c.isalnum() else "_" for c in request.node.name)

        # Save screenshot ONLY to the separate screenshots/ folder
        pg.screenshot(path=f"screenshots/{name}.png", full_page=True)

        # Save Playwright trace ONLY to the separate traces/ folder
        context.tracing.stop(path=f"traces/{name}_trace.zip")

        if SLACK_URL:
            try:
                requests.post(
                    SLACK_URL,
                    json={"text": f"Test Failed [{ENV}]: {request.node.name}"},
                    timeout=5,
                )
            except Exception:
                pass
    else:
        context.tracing.stop()


@pytest.fixture(scope="session")
def api_context(playwright, server_url):
    ctx = playwright.request.new_context(
        base_url=server_url,
        extra_http_headers={"Authorization": "Bearer secret-token-123"},
    )
    yield ctx
    ctx.dispose()


def log_api(method, url, res, payload=None):
    print(f"\n[{ENV.upper()}] {method} {url} -> Status: {res.status}")
    if payload:
        print(f"Request Body: {json.dumps(payload)}")
    print(f"Response Headers: {dict(res.headers)}")
    print(f"Response Body: {res.text()}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
