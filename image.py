import time
from playwright.sync_api import sync_playwright

def capture_verse_image():
    url = "https://www.bible.com/verse-of-the-day"
    output_filename = "daily_verse.png"

    # Start timing
    start_time = time.time()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True in production
        page = browser.new_page()

        # Go to the Verse of the Day page
        page.goto(url, wait_until="networkidle")

        # ✅ Dismiss Cookie Popup if it appears
        try:
            cookie_button = page.locator("[data-testid='close-cookie-banner']")  # More precise selector
            if cookie_button.is_visible():
                cookie_button.click()
                print("✅ Cookie popup dismissed!")
                page.wait_for_timeout(1000)  # Allow time for popup to disappear
        except:
            print("⚠️ No cookie popup found, continuing...")

        # Locate and click the first Verse Image to remove overlay
        initial_verse_element = page.locator("div.cursor-pointer.relative.w-full img").first
        initial_verse_element.click(force=True)
        print("✅ Clicked on the image to remove overlay.")

        # Wait for the new div that appears after clicking
        page.wait_for_selector("div.overflow-hidden.rounded-1", timeout=8000)
        print("✅ Image container updated after click.")

        # Locate the final image inside the updated div
        final_verse_element = page.locator("div.overflow-hidden.rounded-1 img").first

        # Wait until the final image is fully visible
        final_verse_element.wait_for(state="visible", timeout=8000)

        # Take a high-quality screenshot of just the final verse image
        final_verse_element.screenshot(path=output_filename, scale="css")

        browser.close()

    # Stop timing
    end_time = time.time()
    execution_time = end_time - start_time

    print(f"✅ Screenshot saved as {output_filename}")
    print(f"⏱️ Total execution time: {execution_time:.2f} seconds")

# Run the function
capture_verse_image()