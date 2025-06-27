import os, pytest
if not (os.getenv('MF_HOST') and os.getenv('MF_PORT')):
    pytest.skip('Legacy tests require MF_HOST and MF_PORT to be set', allow_module_level=True)
