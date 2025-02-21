import os
import shutil
import datetime

# 🔥 Ensure paths are correctly referenced from the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VERSE_IMAGE_DIR = os.path.join(project_root, "verse_images")

# 🔹 Ensure last_run_month.txt is stored inside the storage folder
STORAGE_DIR = os.path.dirname(__file__)  # Makes sure it's inside `storage/`
STORAGE_FILE = os.path.join(STORAGE_DIR, "last_run_month.txt")

def get_current_month_folder():
    """Returns the current month folder path in the format `02-February/`"""
    now = datetime.datetime.now()
    month_folder = f"{now.strftime('%m')}-{now.strftime('%B')}"  # ✅ 02-February format
    return os.path.join(VERSE_IMAGE_DIR, month_folder)

def find_todays_image():
    """Finds today's image inside `verse_images/` (not inside month folder yet)."""
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Check in root `verse_images/` for today's image
    for filename in os.listdir(VERSE_IMAGE_DIR):
        if today_date in filename and filename.endswith(".png"):  # ✅ Ensure it's a PNG image
            return os.path.join(VERSE_IMAGE_DIR, filename)

    print(f"❌ No image found for today ({today_date}) in {VERSE_IMAGE_DIR}")
    return None  # Return None if no matching file is found

def check_for_new_month():
    """Detects if a new month has started and prepares for a new storage cycle."""
    now = datetime.datetime.now()
    current_month = now.strftime("%m-%B")  # ✅ 02-February format

    # Read last recorded month
    last_month = None
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r") as f:
            last_month = f.read().strip()

    if last_month != current_month:
        print("🗓️ New month detected. Preparing for new storage cycle...")

        # Identify last month’s folder
        last_month_dt = now.replace(day=1) - datetime.timedelta(days=1)
        last_month_folder = os.path.join(VERSE_IMAGE_DIR, last_month_dt.strftime("%m-%B"))

        if os.path.exists(last_month_folder):
            print(f"📤 Last month's images are in {last_month_folder} and ready for processing.")
            # 🔹 Later, this will call Google Drive upload before deletion.

        # Save the new month as the last recorded month inside storage/
        with open(STORAGE_FILE, "w") as f:
            f.write(current_month)

def store_image(image_path):
    """
    Moves today's image from `verse_images/` to the correct `verse_images/MM-MonthName/` folder.
    Preserves the filename.
    """
    # Get the current month folder (e.g., verse_images/02-February)
    month_folder = get_current_month_folder()
    
    # ✅ Create the month folder if it doesn't exist
    os.makedirs(month_folder, exist_ok=True)  

    # Extract only the filename from the full image path
    filename = os.path.basename(image_path)
    final_image_path = os.path.join(month_folder, filename)

    # Move the image to the correct folder
    try:
        shutil.move(image_path, final_image_path)
        print(f"✅ Image successfully moved to: {final_image_path}")
    except Exception as e:
        print(f"❌ Error moving file: {e}")

    return final_image_path