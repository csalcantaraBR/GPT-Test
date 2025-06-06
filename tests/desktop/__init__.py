import sys, pytest
if sys.platform != "win32":
    pytest.skip("Desktop tests require Windows", allow_module_level=True)
