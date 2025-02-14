# 📖 Instagram Verse Bot

🚀 An automated bot that posts the **YouVersion Verse of the Day** to Instagram daily. It fetches the verse image, adds aesthetic music, generates a caption, and uploads it automatically using GitHub Actions.

## ✨ Features
- 📜 Fetches **Verse of the Day** from YouVersion
- 🖼️ Saves verse images in a structured folder format (e.g., `02_February`)
- 🎵 Adds a **random aesthetic background music** from a stored MP3 database
- 🤖 **Automates posting to Instagram** (private account for personal use)
- ⏰ Runs **daily using GitHub Actions**
- 🗑️ Deletes the previous month's images automatically

## 🛠️ Technologies Used
- **Python** (requests, automation)
- **Instagram API** (Instabot)
- **GitHub Actions** (for automation)
- **Cloud Storage / Local Storage** (for images & MP3s)

## 🚀 How It Works
1. **Scrapes the Verse of the Day** from YouVersion
2. **Saves the image** in a monthly folder (`02_February`)
3. **Adds a random music file** to the post
4. **Posts the verse to Instagram automatically** using GitHub Actions
5. **Deletes old month’s images** when a new month starts

## 🔧 Setup Instructions
1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/instagram-verse-bot.git
****
