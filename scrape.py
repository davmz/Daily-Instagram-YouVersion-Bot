import requests
from bs4 import BeautifulSoup

URL = "https://www.bible.com/verse-of-the-day"

def get_verse_image():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the img tag within the div with class "cursor-pointer relative w-full"
    img_tag = soup.find("div", class_="cursor-pointer relative w-full").find("img")
    
    print(img_tag) # alt="Proverbs 17:17 - A friend loves at all times, and a brother is born for a time of adversity."

    # if img_tag:
    #     img_url = img_tag['src']
    #     img_alt = img_tag['alt']
        
    #     # Extract verse text and reference from the alt attribute
    #     verse_reference, verse_text = img_alt.split(' ', 1)
        
    #     # Download the image
    #     img_response = requests.get(img_url)
    #     with open('verse_image.jpg', 'wb') as file:
    #         file.write(img_response.content)
        
    #     return verse_reference, verse_text, 'verse_image.jpg'
    # else:
    #     return "Unknown Reference", "Unknown Verse", None

def get_verse_text():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the <a> tag where href starts with "/bible/compare/"
    verse_text_tag = soup.find("a", href=lambda x: x and x.startswith("/bible/compare/"))
    verse_text = verse_text_tag.get_text(strip=True) if verse_text_tag else "Unknown Verse"

    # Find the <a> tag where href starts with "/bible/" but NOT "/bible/compare/"
    verse_reference_tag = soup.find("a", href=lambda x: x and x.startswith("/bible/") and "/bible/compare/" not in x)

    # Extract the text inside <p> within this <a> tag
    verse_reference = verse_reference_tag.find("p").get_text(strip=True) if verse_reference_tag else "Unknown Reference"

    return verse_reference, verse_text


if __name__ == "__main__":
    get_verse_image()