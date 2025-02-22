import time
import json
from playwright.sync_api import sync_playwright

# ✅ Load Instagram credentials
with open("instagram/credentials.json", "r") as f:
    credentials = json.load(f)
INSTAGRAM_USERNAME = credentials["username"]
INSTAGRAM_PASSWORD = credentials["password"]

def post_to_instagram(image_path):
    """Automates Instagram login and posting an image with Playwright."""
    print("\n🚀 Starting Instagram Automation...\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True when running on a server
        context = browser.new_context()
        page = context.new_page()

        try:
            # ✅ Go to Instagram login page
            page.goto("https://www.instagram.com/accounts/login/")
            print("🌍 Navigating to Instagram login page...")
            page.fill("input[name='username']", INSTAGRAM_USERNAME)
            page.fill("input[name='password']", INSTAGRAM_PASSWORD)
            page.click("button[type='submit']")
            print("✅ Logged into Instagram")

            # ✅ Wait for profile picture (ensures homepage is fully loaded)
            profile_pic_selector = "img[alt=\"dailyverse_bot_proj's profile picture\"]"
            page.wait_for_selector(profile_pic_selector, timeout=15000)
            print("✅ Instagram homepage loaded successfully!")

            time.sleep(3)  # Additional buffer time

            # ✅ Click "New Post" button (SVG icon with `aria-label="New post"`)
            page.click("svg[aria-label='New post']")
            print("📤 Opened 'Create New Post' popup...")
            
            # ✅ Wait for post creation popup (ensures input field is loaded)
            time.sleep(3)  # Allows Instagram to initialize input field

            # ✅ Insert image file directly (force input interaction)
            file_input_selector = "form[role='presentation'] input[type='file']"
            page.set_input_files(file_input_selector, image_path, force=True)
            print(f"📸 Uploaded image: {image_path}")

            # ✅ Wait for 'Next' button to appear and click
            page.click("text=Next")
            time.sleep(5)  # Allow time for Instagram to process the image

            # ✅ Add caption (Verse reference as caption)
            verse_reference = image_path.split("_VOTD_")[-1].replace(".png", "")
            caption = f"{verse_reference} #VerseOfTheDay #Bible"
            page.fill("textarea[aria-label='Write a caption...']", caption)
            print(f"📝 Added caption: {caption}")

            time.sleep(3)  # Buffer time for UI to catch up

            # ✅ Click 'Share' button
            page.click("text=Share")
            print("✅ Post shared successfully!")

            # ✅ Close browser after posting
            time.sleep(5)
            browser.close()

        except Exception as e:
            print(f"❌ Error during Instagram automation: {e}")
            browser.close()