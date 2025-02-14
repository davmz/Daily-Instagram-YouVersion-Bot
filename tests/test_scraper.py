import pytest
from unittest.mock import patch, MagicMock
from data_scrape.scraper import capture_verse_image

@patch("data_scrape.scraper.get_browser")
@patch("data_scrape.scraper.get_verse_image_data")
@patch("data_scrape.scraper.get_verse_of_the_day")
@patch("data_scrape.scraper.crop_image")
def test_capture_verse_image(mock_crop_image, mock_get_verse_of_the_day, mock_get_verse_image_data, mock_get_browser):
    """Tests if capture_verse_image() runs without errors using mocked dependencies."""
    
    # ✅ Mock browser & page
    mock_browser = MagicMock()
    mock_page = MagicMock()
    mock_get_browser.return_value = (mock_browser, mock_page)

    # ✅ Mock verse image locator
    mock_verse_image = MagicMock()
    mock_get_verse_image_data.return_value = mock_verse_image

    # ✅ Mock verse text extraction
    mock_get_verse_of_the_day.return_value = ("John 3:16", "For God so loved the world...")

    # ✅ Mock cropping function
    mock_crop_image.return_value = "test_image.png"

    # ✅ Run function
    result_image, reference, text = capture_verse_image()

    # ✅ Ensure function returns expected values
    assert result_image == "test_image.png", "❌ Image path is incorrect!"
    assert reference == "John 3:16", "❌ Reference is incorrect!"
    assert text == "For God so loved the world...", "❌ Verse text is incorrect!"