import time
from playwright.sync_api import sync_playwright

def capture_verse_image():
    url = "https://www.bible.com/verse-of-the-day"
    output_filename = "daily_verse.png"

    # Start timing
    start_time = time.time()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Run in headless mode
        page = browser.new_page()

        # Go to the Verse of the Day page
        page.goto(url, wait_until="networkidle")  # Ensures full page load

        # Locate the first Verse Image element
        verse_element = page.locator("div.cursor-pointer.relative.w-full img").first

        # Click the image to remove overlay (force click ensures it registers)
        verse_element.click(force=True)

        # Wait 2 seconds to ensure UI updates (adjust if needed)
        page.wait_for_timeout(2000)

        # Take a high-quality screenshot of just the verse image
        verse_element.screenshot(path=output_filename, scale="css")

        browser.close()

    # Stop timing
    end_time = time.time()
    execution_time = end_time - start_time

    print(f"✅ Screenshot saved as {output_filename}")
    print(f"⏱️ Total execution time: {execution_time:.2f} seconds")

# Run the function
capture_verse_image()