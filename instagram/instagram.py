import requests
import json
import time

# ✅ Instagram API Credentials (Replace these with your actual values)
ACCESS_TOKEN = "YOUR_LONG_LIVED_ACCESS_TOKEN"
INSTAGRAM_USER_ID = "YOUR_INSTAGRAM_USER_ID"

def upload_image_to_instagram(image_url, caption):
    """Uploads an image as a draft to Instagram via the Graph API."""
    url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_USER_ID}/media"
    payload = {
        "image_url": image_url,  # Direct URL to the image
        "caption": caption,
        "access_token": ACCESS_TOKEN
    }

    print("📤 Uploading image to Instagram as a draft...")
    response = requests.post(url, data=payload)
    result = response.json()

    if "id" in result:
        media_id = result["id"]
        print(f"✅ Successfully uploaded draft (Media ID: {media_id})")
        return media_id
    else:
        print(f"❌ Error uploading draft: {result}")
        return None

def publish_draft(media_id):
    """Publishes an uploaded draft image to Instagram."""
    url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_USER_ID}/media_publish"
    payload = {
        "creation_id": media_id,
        "access_token": ACCESS_TOKEN
    }

    print("📢 Publishing the draft image to Instagram...")
    response = requests.post(url, data=payload)
    result = response.json()

    if "id" in result:
        print(f"✅ Post published successfully (Post ID: {result['id']})")
        return True
    else:
        print(f"❌ Error publishing post: {result}")
        return False

def process_instagram_upload(image_url, caption):
    """Handles the complete Instagram posting process."""
    media_id = upload_image_to_instagram(image_url, caption)
    if media_id:
        time.sleep(3)  # Allow Instagram time to process the upload
        publish_draft(media_id)

# # Example Usage (Called from `main.py`)
# if __name__ == "__main__":
#     IMAGE_URL = "https://your-server.com/path-to-image.png"  # Change this to your image URL
#     CAPTION = "Philippians 4:6-7 #VerseOfTheDay #Bible"

#     process_instagram_upload(IMAGE_URL, CAPTION)