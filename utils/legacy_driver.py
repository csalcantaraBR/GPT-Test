"""Legacy mainframe driver wrapper around py3270."""

import os
import re
import time
from typing import Optional

from py3270 import Emulator


class MainframeSession:
    """Context manager for interacting with a 3270 mainframe."""

    def __init__(self) -> None:
        self.host = os.getenv("MF_HOST")
        self.port = os.getenv("MF_PORT")
        if not self.host or not self.port:
            raise ValueError("MF_HOST and MF_PORT environment variables must be set")
        self._emulator: Optional[Emulator] = None

    def __enter__(self) -> "MainframeSession":
        self._emulator = Emulator()
        self._emulator.connect(f"{self.host}:{self.port}")
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self._emulator:
            self._emulator.terminate()

    @property
    def emulator(self) -> Emulator:
        if not self._emulator:
            raise RuntimeError("Session not started")
        return self._emulator

    def send(self, data: str) -> None:
        """Send a string to the mainframe and press Enter."""
        self.emulator.send_string(data)
        self.emulator.send_enter()

    def expect(self, pattern: str, timeout: int = 30) -> bool:
        """Return True if regex pattern is found on screen within timeout."""
        regex = re.compile(pattern)
        end = time.time() + timeout
        while time.time() < end:
            cmd = self.emulator.exec_command(b"ReadBuffer(Ascii)")
            screen = b"\n".join(cmd.data).decode("ascii", errors="ignore")
            if regex.search(screen):
                return True
            time.sleep(0.5)
        return False

    def screenshot(self, file_path: str) -> None:
        """Write the current screen buffer to *file_path* as plain text."""
        cmd = self.emulator.exec_command(b"ReadBuffer(Ascii)")
        screen = b"\n".join(cmd.data).decode("ascii", errors="ignore")
        with open(file_path, "w", encoding="utf-8") as fh:
            fh.write(screen)
