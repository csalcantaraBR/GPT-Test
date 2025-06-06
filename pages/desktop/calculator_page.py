"""Page object for Windows Calculator using pywinauto."""

from __future__ import annotations

from pywinauto.application import Application
from pywinauto import Desktop


class CalculatorPage:
    """Simple model of the Windows Calculator app."""

    def __init__(self) -> None:
        self.app: Application | None = None
        self.window = None

    def open(self) -> "CalculatorPage":
        """Attach to a running Calculator or start a new one."""
        try:
            self.app = Application(backend="uia").connect(path="Calculator.exe")
        except Exception:
            self.app = Application(backend="uia").start("calc.exe")

        window = self.app.window(title_re="Calculator")
        window.wait("visible", timeout=15)
        self.dlg = window  # store for later use
        self.window = window
        return self

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

    def press_equals(self) -> None:
        self.window.EqualsButton.click()

    # ---- result ------------------------------------------------------
    def read_result(self) -> float:
        result_text = self.window.CalculatorResults.window_text()
        result_text = result_text.replace("Display is", "").strip()
        result_text = result_text.replace(",", "")
        return float(result_text)
