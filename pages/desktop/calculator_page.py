"""Page object for Windows Calculator using pywinauto."""

from __future__ import annotations

from pywinauto import Application, Desktop, timings
import time
import re


class CalculatorPage:
    """Simple model of the Windows Calculator app."""

    def __init__(self) -> None:
        self.app: Application | None = None
        self.window = None

    # ------------------------------------------------------------------
    def _start_or_attach(self) -> None:
        """Start Calculator or attach to an existing instance."""
        try:
            # Try connecting to a running calculator first.
            self.app = Application(backend="uia").connect(
                title_re=r"(Calculadora|Calculator).*", timeout=5
            )
        except Exception:
            # If not running, launch a new instance.
            self.app = Application(backend="uia").start("calc.exe")
            # Allow the UWP frame some time to initialize.
            time.sleep(1)

    def _find_main_window(self, timeout: int = 45):
        """Return the Calculator window, waiting until it exists."""
        regex = re.compile(r"(Calculadora|Calculator).*", re.I)
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                win = Desktop(backend="uia").window(
                    title_re=regex, control_type="Window", top_level_only=True
                )
                if win.exists(timeout=1):
                    win.wait("visible", timeout=10)
                    win.wait_cpu_usage_lower(threshold=5, timeout=10)
                    return win.wrapper_object()
            except Exception:
                pass
            time.sleep(0.5)
        raise RuntimeError(f"Calculator window not found after {timeout} s")

    # ------------------------------------------------------------------
    def open(self) -> "CalculatorPage":
        """Launch or connect to the Calculator application."""
        self._start_or_attach()
        self.window = self._find_main_window()
        self.window.set_focus()
        return self

    def close(self) -> None:
        """Close the Calculator window if it's open."""
        if self.window:
            try:
                self.window.close()
            except Exception:
                pass
        self.app = None
        self.window = None

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
