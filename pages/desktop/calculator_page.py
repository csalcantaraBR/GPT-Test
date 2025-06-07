"""Page object for Windows Calculator using pywinauto."""

from __future__ import annotations

from pywinauto.application import Application
from pywinauto import Desktop
import re


class CalculatorPage:
    """Simple model of the Windows Calculator app."""

    def __init__(self) -> None:
        self.app: Application | None = None
        self.window = None

    def open(self) -> "CalculatorPage":
        """Launch or connect to the Calculator application."""
        backend = "uia"

        # First attempt to connect to an already running instance. If that
        # fails, start a new one and connect to its process.
        try:
            self.app = Application(backend=backend).connect(path="Calculator.exe")
        except Exception:
            started = Application(backend=backend).start("calc.exe")
            self.app = Application(backend=backend).connect(process=started.process)

        # Support both English and Portuguese titles and allow suffixes ("Calculator - 1").
        title_re = re.compile(r"(Calculator|Calculadora).*", re.I)

        # Locate the main window and dive into the child window if needed.
        window = self.app.window(title_re=title_re)
        if window.element_info.class_name == "ApplicationFrameWindow":
            window = window.child_window(title_re=title_re, control_type="Window")

        # Wait for the window to appear.
        try:
            window.wait("visible", timeout=15)
        except Exception as e:
            raise RuntimeError("Calculator window not found") from e

        window.set_focus()
        window = window.wrapper_object()

        # Store the window for later interactions
        self.dlg = window
        self.window = window
        return self

    def close(self) -> None:
        """Close the Calculator application if it's running."""
        if self.app is not None:
            try:
                self.app.kill()
            finally:
                self.app = None
                self.window = None
                self.dlg = None

    # ---- helpers -----------------------------------------------------
    def press_number(self, number: int) -> None:
        button_name = f"Num{number}Button"
        getattr(self.window, button_name).click()

    def press_operator(self, operator: str) -> None:
        mapping = {
            "+": "PlusButton",
            "-": "MinusButton",
            "*": "MultiplyByButton",
            "/": "DivideByButton",
        }
        button_name = mapping.get(operator)
        if not button_name:
            raise ValueError(f"Unsupported operator: {operator}")
        getattr(self.window, button_name).click()

    def press(self, key):
        """Press a digit, operator or equals button based on ``key``."""
        if isinstance(key, int):
            self.press_number(key)
        elif key in {"+", "-", "*", "/"}:
            self.press_operator(key)
        elif key == "=":
            self.press_equals()
        else:
            raise ValueError(f"Unsupported key: {key}")

    def press_equals(self) -> None:
        self.window.EqualsButton.click()

    # ---- result ------------------------------------------------------
    def read_result(self) -> float:
        result_text = self.window.CalculatorResults.window_text()
        result_text = result_text.replace("Display is", "").strip()
        result_text = result_text.replace(",", "")
        return float(result_text)
