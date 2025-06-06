import os
import sys
import pytest

# hosted Windows runners (windows-latest) não têm desktop interativo
if os.getenv("CI"):
    pytest.xfail("Skipping GUI test: no interactive desktop on hosted runner")

if sys.platform != "win32":
    pytest.skip("Desktop tests require Windows", allow_module_level=True)
