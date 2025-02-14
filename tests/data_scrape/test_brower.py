import os
import sys
from playwright.sync_api import sync_playwright

# ✅ Add the project root to sys.path so Python can find `data_scrape`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from data_scrape.browser import get_browser

def test_get_browser():
    """Tests if the browser instance is created successfully."""
    with sync_playwright() as p:
        browser, page = get_browser(p)

        # ✅ Ensure browser instance is created
        assert browser is not None, "❌ Browser instance was not created!"
        assert page is not None, "❌ Page instance was not created!"

        browser.close()  # ✅ Cleanup