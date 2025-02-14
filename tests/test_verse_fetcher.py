import requests_mock
from data_scrape import get_verse_of_the_day # view data_scrape/__init__.py

def test_fetch_verse_of_the_day():
    """Test if verse text and reference are successfully extracted and contain values."""
    test_url = "https://www.bible.com/verse-of-the-day"

    # ✅ Mock the response for requests.get
    with requests_mock.Mocker() as mocker:
        mocker.get(test_url, text='''
            <a href="/bible/compare/123"><p>Some verse text here</p></a>
            <a href="/bible/123"><p>John 3:16</p></a>
        ''')

        reference, verse_text = get_verse_of_the_day(test_url)

    # ✅ Ensure verse text and reference contain values (not empty, not "Unknown")
    assert verse_text and verse_text != "Unknown Verse", "❌ Extracted verse text is missing!"
    assert reference and reference != "Unknown Reference", "❌ Extracted reference is missing!"

    print(f"✅ Test passed: Extracted Verse - {verse_text}, Reference - {reference}")