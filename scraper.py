import time
from playwright.sync_api import sync_playwright
from PIL import Image

## Capture the Verse of the Day image from YouVersion Bible website (Verse of the Day)
def capture_verse_image():
    url = "https://www.bible.com/verse-of-the-day"
    output_filename = "daily_verse.png"
    cropped_output_filename = "daily_verse_cropped.png"

    # Start timing
    start_time = time.time()

    with sync_playwright() as p:
        # ✅ Run Playwright in headless mode for GitHub Actions
        browser = p.chromium.launch(
            headless=True,  # ✅ Must be True for GitHub Actions
            args=["--window-size=2560,1440"]
        )
        context = browser.new_context(
            viewport={"width": 2560, "height": 1440},
            device_scale_factor=4
        )
        page = context.new_page()

        # Go to the Verse of the Day page
        page.goto(url, wait_until="networkidle")

        # ✅ Dismiss Cookie Popup if it appears
        try:
            cookie_button = page.locator("[data-testid='close-cookie-banner']")
            if cookie_button.is_visible():
                cookie_button.click()
                print("✅ Cookie popup dismissed!")
                page.wait_for_timeout(1000)
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
        final_verse_element.wait_for(state="visible", timeout=10000)

        # ✅ Take a high-quality screenshot
        final_verse_element.screenshot(path=output_filename, type="png", scale="device")

        browser.close()

    # ✅ Auto-crop the screenshot to remove white edges
    with Image.open(output_filename) as img:
        width, height = img.size
        crop_margin = int(height * 0.02)  # ✅ Adjusts 2% of the image height as margin
        cropped_img = img.crop((crop_margin, crop_margin, width - crop_margin, height - crop_margin)).copy()
        cropped_img.save(cropped_output_filename, format="PNG", optimize=True)

    # Stop timing
    end_time = time.time()
    execution_time = end_time - start_time

    print(f"✅ Screenshot saved as {output_filename} (High Quality)")
    print(f"✅ Cropped image saved as {cropped_output_filename} (No white edges, HD!)")
    print(f"⏱️ Total execution time: {execution_time:.2f} seconds")