import os
import time
from playwright.sync_api import sync_playwright

from data_scrape import get_browser, get_verse_of_the_day, get_verse_image_data
from data_scrape.utils import crop_image, generate_filename

# 🔥 Get absolute project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
verse_images_dir = os.path.join(project_root, "verse_images")

# 🔥 Ensure verse_images directory exists
os.makedirs(verse_images_dir, exist_ok=True)

VERSE_URL = "https://www.bible.com/verse-of-the-day"

# def format_verse_reference(verse_reference):
#     """Formats the verse reference by removing spaces and replacing `:` with `.`."""
#     return verse_reference.replace(" ", "").replace(":", ".")

# def generate_filename(verse_reference):
#     """Generates a filename in the format YYYY-MM-DD_VOTD_versereference.png"""
#     now = datetime.datetime.now()
#     formatted_reference = format_verse_reference(verse_reference)  # 🛠 Apply formatting fix
#     return f"{now.strftime('%Y-%m-%d')}_VOTD_{formatted_reference}.png"

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

            # Generate final filename and path
            final_filename = generate_filename(verse_reference)
            final_image_path = os.path.join(verse_images_dir, final_filename)

            # Ensure Directory exists
            os.makedirs(verse_images_dir, exist_ok=True)

            final_image_abs_path = os.path.abspath(final_image_path)  # Get full path
            print(f"📁 Absolute image path: {final_image_abs_path}")

            # Take a high-quality screenshot directly to the final image path
            verse_image.screenshot(path=final_image_path, type="png", scale="css")
            print(f"✅ Screenshot saved as {final_image_path} (High Quality)")

            browser.close() # Close the browser

        # Auto-crop the screenshot to remove white edges
        crop_image(final_image_path, final_image_path, margin_percent=0.02)

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

# if __name__ == "__main__":
#     capture_verse_image() # Run the main function