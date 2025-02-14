from data_scrape import capture_verse_image

def main():
    print("🚀 Starting the Verse Automation...")

    # Step #1: Capture the Verse of the Day and save the image
    verse_image, verse_reference, verse_text = capture_verse_image()

    # Step #2: Organize images in monthly folders and deletes old ones (new month)
    # manage_images()

    # Step #3: Post the latest image to Instagram with music, caption, and hashtags
    # post_to_instagram()

    print("🎉 Daily Verse Automation Completed!")

if __name__ == "__main__":
    main()