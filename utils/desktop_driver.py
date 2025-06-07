"""Helpers for interacting with desktop applications using pywinauto."""

from __future__ import annotations

from typing import Optional

from pywinauto import Application
from pywinauto.application import WindowSpecification
from pywinauto import timings

timings.Timings.window_find_timeout = 30
timings.Timings.app_start_timeout = 30


_app: Optional[Application] = None


def get_app(app_path: str) -> Application:
    """Return a connected ``Application`` instance, starting it if needed."""
    global _app
    if _app is None:
        app = Application(backend="uia")
        try:
            app.connect(path=app_path)
        except Exception:
            app = Application(backend="uia").start(app_path)
        _app = app
    return _app


def find_window(title_regex: str, class_name: str | None = None) -> WindowSpecification:
    """Return a window matching ``title_regex`` from the initialized app."""
    if _app is None:
        raise RuntimeError("Application not initialized. Call get_app() first.")
    return _app.window(title_re=title_regex, class_name=class_name)


def close_app() -> None:
    """Terminate the application if it is running."""
    global _app
    if _app is not None:
        try:
            _app.kill()
        finally:
            _app = None

