import os
import time
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 🔥 Define the service account JSON path
SERVICE_ACCOUNT_FILE = "google_drive/service_account.json"

def upload_to_google_drive(file_path):
    """
    Uploads the given file to Google Drive inside `VOTD/{YEAR}/{MM_Month}/`
    """

    # ✅ Start execution timer
    start_time = time.time()
    
    try:
        print("\n🚀 Starting Google Drive upload process...\n")

        # ✅ Step 1: Authenticate with Google Drive
        print("🔑 Authenticating with Google Drive...")
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/drive"]
        )
        drive_service = build("drive", "v3", credentials=credentials)
        print("✅ Authentication successful.\n")

        # ✅ Step 2: Create or find the `VOTD` main folder
        def get_or_create_folder(folder_name, parent_id=None):
            """Finds or creates a folder in Google Drive and returns its ID."""
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            if parent_id:
                query += f" and '{parent_id}' in parents"

            results = drive_service.files().list(q=query, fields="files(id)").execute().get("files", [])
            if results:
                return results[0]["id"]  # ✅ Folder already exists
            else:
                folder_metadata = {
                    "name": folder_name,
                    "mimeType": "application/vnd.google-apps.folder",
                    "parents": [parent_id] if parent_id else []
                }
                folder = drive_service.files().create(body=folder_metadata, fields="id").execute()
                print(f"📂 Created folder: {folder_name}")
                return folder["id"]

        # 🔥 Step 3: Create `VOTD` folder (if it doesn't exist)
        votd_folder_id = get_or_create_folder("VOTD")
        
        # 🔥 Step 4: Create `{YEAR}` folder inside `VOTD`
        current_year = datetime.now().strftime("%Y")
        year_folder_id = get_or_create_folder(current_year, votd_folder_id)

        # 🔥 Step 5: Create `{MM_Month}` folder inside `{YEAR}`
        current_month = datetime.now().strftime("%m_%B")  # Example: "02_February"
        month_folder_id = get_or_create_folder(current_month, year_folder_id)

        # ✅ Step 6: Upload the given file inside `{MM_Month}` folder
        print(f"📂 Checking for file: {file_path}...")

        if os.path.exists(file_path):
            filename = os.path.basename(file_path)
            print(f"✅ Found '{filename}'. Uploading...")
            file_metadata = {"name": filename, "parents": [month_folder_id]}
            media = MediaFileUpload(file_path, mimetype="image/png")  # Adjust if needed
            drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
            print(f"✅ Uploaded '{filename}' to Google Drive inside: VOTD/{current_year}/{current_month}/")
        else:
            print(f"❌ ERROR: File not found - {file_path}")

    except Exception as e:
        print(f"❌ ERROR: {e}")

    # ✅ End execution timer
    total_time = time.time() - start_time
    print(f"\n⏱️ Total execution time: {total_time:.2f} seconds\n")

# # Example Usage (Called from `main.py`)
# if __name__ == "__main__":
#     upload_to_google_drive()