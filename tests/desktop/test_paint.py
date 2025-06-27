import time
from pywinauto.application import Application
from pywinauto.findwindows import ElementNotFoundError


def test_open_paint():
    """Verify that Microsoft Paint launches correctly."""
    app = Application(backend="uia").start("mspaint.exe")
    time.sleep(2)
    try:
        win = app.window(title_re=".*Paint.*", control_type="Window", top_level_only=True)
        win.wait("visible", timeout=10)
    except ElementNotFoundError:
        raise AssertionError("Paint window not found")
    finally:
        try:
            win.close()
            app.window(title_re=".*Paint.*").window(auto_id="CommandButton_7").click()
        except Exception:
            pass

