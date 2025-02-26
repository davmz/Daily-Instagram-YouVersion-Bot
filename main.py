import time

from file_storage import manage_storage
from data_scrape.scraper import capture_verse_image
from google_drive.google_drive import process_google_drive_uploads

def main():
    """Runs the Verse of the Day bot and tracks total execution time."""
    # Start timer
    start_time = time.time()

    print("🚀 Starting the Verse Automation...")

    # Step #1: Capture the Verse of the Day and save the image
    verse_image, verse_reference, verse_text = capture_verse_image()

    print(f"📸 Captured Verse Image: {verse_image}")
    print(f"📖 Verse Reference: {verse_reference}")
    print(f"📜 Verse Text: {verse_text}")

    # Step #2: Organize images in monthly folders and deletes old ones (new month)
    stored_image_path =  manage_storage()
    print(f"✅ Image successfully stored: {stored_image_path}")

    # Step #3: Upload Image to Google Drive
    if stored_image_path:
        print("📤 Uploading Image to Google Drive...")
        process_google_drive_uploads(stored_image_path)
        print("✅ Image successfully uploaded to Google Drive!")

    # Step #4: Upload Image to Instagram
    ## Issues setting up API -> will not continue

    print("🎉 Daily Verse Automation Completed!")

    # Calculate total execution time 
    total_time = time.time() - start_time
    print(f"⏱️ Total execution time: {total_time:.2f} seconds")

if __name__ == "__main__":
    main()