def get_browser(playwright):
    """Initializes Playwright browser with optimized settings."""
    # Run Playwright in headless mode for GitHub Actions
    browser = playwright.chromium.launch(
        headless=True,  # ✅ Must be True for GitHub Actions
        args=["--window-size=2560,1440"]
    )
    context = browser.new_context(
        viewport={"width": 2560, "height": 1440},
        device_scale_factor=3
    )

    return browser, context.new_page()