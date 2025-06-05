"""Configuration for the Playwright-based automation framework."""

import os
from dotenv import load_dotenv


load_dotenv()

# Base URL for the application under test
BASE_URL = os.getenv("BASE_URL", "https://example.com")
