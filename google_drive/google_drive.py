import os
from google_drive.drive_helper import upload_to_google_drive, retry_failed_uploads, file_exists_in_drive, get_drive_folders

def process_google_drive_uploads(file_path):
    """Main function to handle both new uploads and retry failed uploads."""
    if file_path:
        filename = os.path.basename(file_path)
        month_folder_id = get_drive_folders()  # Get correct upload location

        # Check if the file exists in Google Drive before uploading
        if file_exists_in_drive(filename, month_folder_id):
            print(f"⚠️ Skipping upload: {file_path} already exists in Google Drive.")
            return
        
        upload_to_google_drive(file_path)  # Upload new image

    retry_failed_uploads()  # Always check for failed uploads after new ones

# # Example Usage (Called from `main.py`)
# if __name__ == "__main__":
#     process_google_drive_uploads()