import os
import time
import logging
from datetime import datetime

from file_storage import manage_storage
from data_scrape.scraper import capture_verse_image
from google_drive.google_drive import process_google_drive_uploads

# Ensure `logs/` directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Generate a log file for each day (YYYY-MM-DD.log)
log_filename = os.path.join(LOG_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.log")

# Configure logging format
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def main():
    """Runs the Verse of the Day bot and logs execution details."""
    start_time = time.time()
    logging.info("🚀 Starting the Verse Automation...\n")

    try:
        # Step #1: Capture the Verse of the Day
        verse_image, verse_reference, verse_text = capture_verse_image()
        if not verse_image:
            logging.error("❌ Failed to capture the verse image.")
            return

        logging.info(f"📸 Captured Verse Image: {verse_image}")
        logging.info(f"📖 Verse Reference: {verse_reference}")
        logging.info(f"📜 Verse Text: {verse_text}")

        # Step #2: Organize images in monthly folders
        stored_image_path = manage_storage()
        if not stored_image_path:
            logging.error("❌ Storage process failed.")
            return

        logging.info(f"✅ Image successfully stored: {stored_image_path}")

        # Step #3: Upload Image to Google Drive
        process_google_drive_uploads(stored_image_path)

    except Exception as e:
        logging.error(f"❌ Error in main execution: {e}")

    # Log execution time
    total_time = time.time() - start_time
    logging.info(f"⏱️ Total execution time: {total_time:.2f} seconds")
    logging.info("🎉 Daily Verse Automation Completed!")

if __name__ == "__main__":
    main()