from pathlib import Path
from functools import partial
import threading
import socketserver
from http.server import SimpleHTTPRequestHandler

from pages.login_page import LoginPage
from config import settings


def test_login(page):
    """Verify a user can log in using the sample HTML page."""
    html_dir = Path(__file__).parent / "static"

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, directory=None, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)

        def do_GET(self):
            if self.path == "/login":
                self.path = "/login.html"
            elif self.path == "/dashboard":
                self.path = "/dashboard.html"
            return super().do_GET()

    with socketserver.TCPServer(("127.0.0.1", 0), partial(Handler, directory=html_dir)) as httpd:
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        settings.BASE_URL = f"http://127.0.0.1:{httpd.server_address[1]}"
        login_page = LoginPage(page)
        login_page.goto()
        login_page.enter_username("user")
        login_page.enter_password("pass")
        login_page.click_login()
        assert login_page.is_logged_in()
        httpd.shutdown()
        thread.join()
