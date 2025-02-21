import time
from .monthly_storage import check_for_new_month, store_image, find_todays_image

def manage_storage():
    """
    Main storage function that:
    1️⃣ Checks if a new month has started (uploads & deletes old images).
    2️⃣ Finds today's image and moves it into the correct monthly folder.
    3️⃣ Prints the execution time.
    """
    print("🗂️ Managing Storage Process...")

    # Start execution timer
    start_time = time.time()

    # Step 1: Detect if a new month started & handle cleanup
    check_for_new_month()

    # Step 2: Find today's image automatically
    image_path = find_todays_image()
    if not image_path:
        print("❌ No image found for today. Skipping storage process.")
        return None

    # Step 3: Move the image to the correct folder
    stored_image_path = store_image(image_path)

    # Calculate execution time
    execution_time = time.time() - start_time
    print(f"✅ Image successfully stored: {stored_image_path}")
    print(f"⏱️ Execution time: {execution_time:.2f} seconds")

    return stored_image_path  # Return the final stored path

# # Example Usage (Called from `main.py`)
# if __name__ == "__main__":
#     manage_storage()