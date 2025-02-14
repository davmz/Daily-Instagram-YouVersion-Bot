from data_scrape.browser import get_browser
from playwright.sync_api import sync_playwright

def test_get_browser():
    """Tests if the browser instance is created successfully."""
    with sync_playwright() as p:
        browser, page = get_browser(p)

        # ✅ Ensure browser instance is created
        assert browser is not None, "❌ Browser instance was not created!"
        assert page is not None, "❌ Page instance was not created!"

        browser.close()  # ✅ Cleanup