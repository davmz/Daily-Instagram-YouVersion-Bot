import os
import time
import shutil
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 🔥 Define paths
SERVICE_ACCOUNT_FILE = "google_drive/service_account.json"
VERSE_IMAGES_DIR = "verse_images"  # ✅ Root directory for images
FAILED_UPLOADS_DIR = os.path.join(VERSE_IMAGES_DIR, "failed_uploads")  # ✅ Failed images stored here
LOGS_DIR = "logs"
FAILED_LOG_FILE = os.path.join(LOGS_DIR, "failed_log.txt")

# ✅ Ensure `logs/` directory exists
os.makedirs(LOGS_DIR, exist_ok=True)

# ✅ Authenticate **once** and reuse
def authenticate_drive():
    """Authenticates and returns a Google Drive API service instance."""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=credentials)

# ✅ Create a single instance of the Drive service
drive_service = authenticate_drive()

def get_or_create_folder(folder_name, parent_id=None):
    """Finds or creates a folder in Google Drive and returns its ID. Prints folder details for debugging."""
    
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"

    results = drive_service.files().list(q=query, fields="files(id, name)").execute().get("files", [])

    if results:
        folder_id = results[0]["id"]
        print(f"📁 Found existing folder: {folder_name} (ID: {folder_id})")
        return folder_id
    else:
        folder_metadata = {"name": folder_name, "mimeType": "application/vnd.google-apps.folder"}
        if parent_id:
            folder_metadata["parents"] = [parent_id]

        folder = drive_service.files().create(body=folder_metadata, fields="id, name").execute()
        print(f"📂 Created folder: {folder_name} (ID: {folder['id']})")
        return folder["id"]

def get_drive_folders():
    """Returns the Google Drive folder structure for the current date."""
    votd_folder_id = get_or_create_folder("VOTD")
    current_year = datetime.now().strftime("%Y")
    year_folder_id = get_or_create_folder(current_year, votd_folder_id)
    current_month = datetime.now().strftime("%m_%B")  # Example: "02_February"
    month_folder_id = get_or_create_folder(current_month, year_folder_id)
    return month_folder_id  # ✅ Returns folder ID for uploads

def file_exists_in_drive(filename, parent_folder_id):
    """Checks if the file already exists in Google Drive to prevent duplicate uploads."""
    query = f"name='{filename}' and '{parent_folder_id}' in parents and trashed=false"
    results = drive_service.files().list(q=query, fields="files(id)").execute().get("files", [])
    return len(results) > 0  # ✅ Returns True if file exists, False otherwise

def upload_to_google_drive(file_path):
    """
    Uploads the given file to Google Drive inside `VOTD/{YEAR}/{MM_Month}/`.
    Now prints detailed API response to verify if the file is actually uploaded.
    """
    start_time = time.time()

    if not os.path.exists(file_path):
        print(f"❌ ERROR: File not found - {file_path}")
        log_failed_upload(file_path)
        return False  # Upload failed

    try:
        print("\n🚀 Starting Google Drive upload process...\n")
        month_folder_id = get_drive_folders()  # Get correct upload location

        if not month_folder_id:
            print("❌ ERROR: Could not retrieve or create the destination folder in Google Drive.")
            log_failed_upload(file_path)
            return False  # Upload failed

        filename = os.path.basename(file_path)
        print(f"📂 Checking for file: {file_path}...")

        # Skip upload if file already exists in Google Drive
        if file_exists_in_drive(filename, month_folder_id):
            print(f"⚠️ Skipping upload: {filename} already exists in Google Drive.")
            return False

        if os.path.exists(file_path):
            print(f"✅ Found '{filename}'. Uploading...")

            file_metadata = {"name": filename, "parents": [month_folder_id]}
            media = MediaFileUpload(file_path, mimetype="image/png", resumable=True)

            uploaded_file = drive_service.files().create(
                body=file_metadata, media_body=media, fields="id, name, mimeType, parents"
            ).execute()

            # Print the full API response for debugging
            print(f"🔍 Google Drive API Response: {uploaded_file}")

            if uploaded_file and "id" in uploaded_file:
                print(f"✅ Uploaded '{filename}' to Google Drive (ID: {uploaded_file['id']})")
                print(f"🔗 File Link: https://drive.google.com/file/d/{uploaded_file['id']}/view")
                
                # Remove from failed log if it was a retry
                remove_from_failed_log([filename])

                total_time = time.time() - start_time
                print(f"\n⏱️ Total execution time: {total_time:.2f} seconds\n")
                return True  # Upload successful
            else:
                print(f"❌ ERROR: Upload API did not return a valid response.")
                log_failed_upload(file_path)
                return False  # Upload failed

        else:
            print(f"❌ ERROR: File not found - {file_path}")
            log_failed_upload(file_path)  # ✅ Log failed upload
            return False  # Upload failed

    except Exception as e:
        print(f"❌ ERROR: {e}")
        log_failed_upload(file_path)  # ✅ Log failed upload
        return False  # Upload failed

def log_failed_upload(file_path):
    """Moves failed upload to `verse_images/failed_uploads/YYYY/MM_Month/` and logs failure."""
    filename = os.path.basename(file_path)
    current_year = datetime.now().strftime("%Y")
    current_month = datetime.now().strftime("%m_%B")
    failed_folder = os.path.join(FAILED_UPLOADS_DIR, current_year, current_month)

    # Create failed_uploads directory if it doesn't exist
    os.makedirs(failed_folder, exist_ok=True)
    failed_image_path = os.path.join(failed_folder, filename)

    try:
        shutil.move(file_path, failed_image_path)
        print(f"⚠️ Upload failed. Moved file to: {failed_image_path}")

        # Log failure in `logs/failed_log.txt`
        with open(FAILED_LOG_FILE, "a") as log_file:
            log_file.write(f"{datetime.now()} - FAILED: {filename}\n")

    except Exception as e:
        print(f"❌ Error moving failed file: {e}")

def retry_failed_uploads():
    """Retries uploads for files in `failed_uploads/`, then removes them from `failed_log.txt`."""
    
    # Ensure failed_uploads directory exists before accessing it
    if not os.path.exists(FAILED_UPLOADS_DIR):
        print("⚠️ No failed uploads directory found. Skipping retry process.")
        return  # Exit if the directory does not exist

    files_to_remove = []

    for year in os.listdir(FAILED_UPLOADS_DIR):
        year_path = os.path.join(FAILED_UPLOADS_DIR, year)
        if os.path.isdir(year_path):
            for month in os.listdir(year_path):
                month_path = os.path.join(year_path, month)
                if os.path.isdir(month_path):
                    for filename in os.listdir(month_path):
                        file_path = os.path.join(month_path, filename)
                        print(f"🔄 Retrying upload for: {file_path}")
                        if upload_to_google_drive(file_path):  # Only remove if upload is successful
                            files_to_remove.append(filename)

    # Remove successfully uploaded files from `failed_log.txt`
    if files_to_remove:
        remove_from_failed_log(files_to_remove)


def remove_from_failed_log(files_to_remove):
    """Removes successfully uploaded files from `logs/failed_log.txt`."""
    if not files_to_remove:
        return  # No files to remove, skip

    if os.path.exists(FAILED_LOG_FILE):
        with open(FAILED_LOG_FILE, "r") as log_file:
            lines = log_file.readlines()

        with open(FAILED_LOG_FILE, "w") as log_file:
            for line in lines:
                if not any(filename in line for filename in files_to_remove):
                    log_file.write(line)

        print("🗑️ Updated failed_log.txt after successful uploads.")