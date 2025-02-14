
import requests
from bs4 import BeautifulSoup

def get_verse_of_the_day(VERSE_URL):
    """Fetches the verse text, reference, and Bible version using BeautifulSoup."""
    try:
        # Fetch the Verse of the Day page
        response = requests.get(VERSE_URL)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the <a> tag where href starts with "/bible/compare/"
        verse_text_tag = soup.find("a", href=lambda x: x and x.startswith("/bible/compare/"))
        verse_text = verse_text_tag.get_text(strip=True) if verse_text_tag else "Unknown Verse"

        # Find the <a> tag where href starts with "/bible/" but NOT "/bible/compare/"
        verse_reference_tag = soup.find("a", href=lambda x: x and x.startswith("/bible/") and "/bible/compare/" not in x)

        # Extract the text inside <p> within this <a> tag
        verse_reference = verse_reference_tag.find("p").get_text(strip=True) if verse_reference_tag else "Unknown Reference"

        return verse_reference, verse_text
    except Exception as e:
        print(f"❌ Error in get_verse_of_the_day: {e}")
        return "Unknown Reference", "Unknown Verse"

def get_verse_image_data(page):
    """Finds the Verse of the Day image, verse reference, and verse text."""

    ### Find the Verse of the Day image
    # Handle cookie banner/popup if present
    cookie_button = page.locator("[data-testid='close-cookie-banner']")
    if cookie_button.is_visible():
        cookie_button.click()
        print("Cookie popup dismissed!")
        page.wait_for_timeout(1000)

    # Locate and click the first Verse Image to remove overlay
    image_element = page.locator("div.cursor-pointer.relative.w-full img").first
    image_element.click(force=True)
    print("✅ Clicked on the image to remove overlay.")

    # Wait for the new div that appears after clicking
    page.wait_for_selector("div.overflow-hidden.rounded-1", timeout=8000)
    print("✅ Image container updated after click.")

    # ✅ Get final image element
    final_image_element = page.locator("div.overflow-hidden.rounded-1 img").first

    ### Find the Verse Reference and Verse Text

    return final_image_element