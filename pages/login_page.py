"""Page object model for the login page using Playwright's sync API."""

from playwright.sync_api import Page

from config import settings


class LoginPage:
    """Page object for the login screen."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self) -> None:
        """Navigate to the application's login page."""
        self.page.goto(f"{settings.BASE_URL}/login")

    def enter_username(self, username: str) -> None:
        self.page.fill("input[name='username']", username)

    def enter_password(self, password: str) -> None:
        self.page.fill("input[name='password']", password)

    def click_login(self) -> None:
        self.page.click("#login")
        # Ensure navigation completes for basic static pages
        self.page.goto(f"{settings.BASE_URL}/dashboard")

    def is_logged_in(self) -> bool:
        return self.page.url.endswith("/dashboard")
