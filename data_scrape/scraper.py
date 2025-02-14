import time
from playwright.sync_api import sync_playwright
from browser import get_browser
from verse_fetcher import get_verse_of_the_day, get_verse_image_data
from utils.image_utils import crop_image

VERSE_URL = "https://www.bible.com/verse-of-the-day"

def capture_verse_image():
    """Scrapes the Verse of the Day image, verse text, and Bible version."""
    start_time = time.time()
    browser = None

    try:
        with sync_playwright() as p:
            browser, page = get_browser(p) # Get the browser and page
            page.goto(VERSE_URL, wait_until="networkidle") # Go to the Verse of the Day page

            # Fetch image element
            verse_image = get_verse_image_data(page)

            if not verse_image:
                raise ValueError("❌ Could not locate the verse image.")

            # Fetch verse text, and verse reference using BeautifulSoup
            verse_reference, verse_text = get_verse_of_the_day(VERSE_URL)

            ### Take high-quality screenshot of the verse image
            # Wait until final image is fully visible
            verse_image.wait_for(state="visible", timeout=10000)

            # Take a high-quality screenshot
            raw_image_path = "../verse_images/daily_verse_raw.png"
            cropped_image_path = "../verse_images/daily_verse.png" # Final cropped version
            verse_image.screenshot(path=raw_image_path, type="png", scale="device")
            print(f"✅ Screenshot saved as {raw_image_path} (High Quality)")

            browser.close() # Close the browser

        # Auto-crop the screenshot to remove white edges
        final_image_path = crop_image(raw_image_path, cropped_image_path, margin_percent=0.02)

        execution_time = time.time() - start_time
        print(f"⏱️ Total execution time: {execution_time:.2f} seconds")

        return final_image_path, verse_reference, verse_text
    except Exception as e:
        print(f"❌ Error in capture_verse_image: {e}")
        return None, None, None
    finally:
        # Prevent double-closing errors by handling exceptions
        try:
            if browser:  
                browser.close()
        except Exception:
            pass  # Ignore errors if the browser is already closed

if __name__ == "__main__":
    capture_verse_image() # Run the main function