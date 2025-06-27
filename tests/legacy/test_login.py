from utils.legacy_driver import MainframeSession
from pages.legacy.login_screen import LoginScreen


def test_mainframe_login():
    with MainframeSession() as sess:
        login = LoginScreen(sess)
        login.login("USER1", "SECRET")
        assert login.assert_logged_in()
