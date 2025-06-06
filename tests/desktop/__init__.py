import os, sys, pytest

# Skip the entire desktop test suite when running on hosted CI runners
# or on any non-Windows platform.
if os.getenv("CI") or sys.platform != "win32":
    pytest.skip(
        "Desktop tests require an interactive Windows session",
        allow_module_level=True
    )
