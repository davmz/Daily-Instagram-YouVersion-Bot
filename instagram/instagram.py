from insta_bot import post_to_instagram

IMAGE_PATH = "C:\Projects\Daily-Instagram-YouVersion-Bot\verse_images\02-February\2025-02-20_VOTD_Philippians4.7(NIV).png"

def process_instagram_upload(file_path):
    """"Main function to handle Instagram automation."""
    if file_path:
        post_to_instagram(file_path)

# Example Usage (Called from `main.py`)
if __name__ == "__main__":
    process_instagram_upload(IMAGE_PATH)