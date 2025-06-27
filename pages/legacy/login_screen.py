"""Page object for the legacy terminal login screen."""


class LoginScreen:
    """Interact with the legacy login screen over a session."""

    def __init__(self, session):
        """Store the session used to communicate with the terminal."""
        self.session = session

    def login(self, user: str, pwd: str) -> None:
        """Send credentials and advance to the next screen."""
        # Type username, move to the password field and submit
        self.session.send(user)
        # Navigate to password input if required
        self.session.send("\t")
        self.session.send(pwd)
        # Press Enter to submit the form
        self.session.send("\r")

    def assert_logged_in(self) -> None:
        """Verify that the main menu is displayed."""
        self.session.expect("MAIN MENU")
