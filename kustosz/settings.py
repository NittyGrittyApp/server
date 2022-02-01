"""
Django settings are managed by dynaconf - see settings.yaml in parent directory
"""
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

import dynaconf  # noqa

settings = dynaconf.DjangoDynaconf(
    __name__, settings_files=[BASE_DIR / "settings.yaml", BASE_DIR / ".secrets.yaml"]
)  # noqa