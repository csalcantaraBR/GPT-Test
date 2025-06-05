"""Configuration settings for automation framework."""
import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Base URL for the application under test
BASE_URL = os.getenv("BASE_URL", "https://example.com")

# Browser to use for Selenium tests
BROWSER = os.getenv("BROWSER", "chrome")
