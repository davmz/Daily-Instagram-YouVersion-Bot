import pytest
import requests_mock
from data_scrape.verse_fetcher import get_verse_of_the_day

def test_get_verse_of_the_day():
    """Tests if get_verse_of_the_day() correctly extracts verse text and reference."""
    test_url = "https://www.bible.com/verse-of-the-day"

    # ✅ Mock requests.get response
    with requests_mock.Mocker() as mocker:
        mocker.get(test_url, text='''
            <a href="/bible/compare/123"><p>Test Verse</p></a>
            <a href="/bible/123"><p>John 3:16</p></a>
        ''')

        reference, verse_text = get_verse_of_the_day(test_url)

    # ✅ Ensure extracted values are not empty
    assert verse_text and verse_text != "Unknown Verse", "❌ Extracted verse text is missing!"
    assert reference and reference != "Unknown Reference", "❌ Extracted reference is missing!"