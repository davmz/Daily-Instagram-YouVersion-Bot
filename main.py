import time
from data_scrape import capture_verse_image

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
    # manage_images()

    # Step #3: Post the latest image to Instagram with music, caption, and hashtags
    # post_to_instagram()

    print("🎉 Daily Verse Automation Completed!")

    # Calculate total execution time 
    total_time = time.time() - start_time
    print(f"⏱️ Total execution time: {total_time:.2f} seconds")

if __name__ == "__main__":
    main()