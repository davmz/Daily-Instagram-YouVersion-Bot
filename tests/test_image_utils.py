import os
import pytest
from data_scrape.utils.image_utils import crop_image
from PIL import Image

@pytest.fixture
def sample_image(tmp_path):
    """Creates a temporary sample image for testing."""
    img_path = tmp_path / "test_image.png"
    img = Image.new("RGB", (500, 500), color="white")  # Create white image
    img.save(img_path)
    return img_path

def test_crop_image(sample_image, tmp_path):
    """Tests if crop_image() correctly processes the image."""
    output_path = tmp_path / "cropped_image.png"

    result = crop_image(str(sample_image), str(output_path), margin_percent=0.05)

    # ✅ Ensure cropped image exists
    assert os.path.exists(result), "❌ Cropped image was not created!"

    # ✅ Ensure output file is not the same as input
    assert result != str(sample_image), "❌ Output file should be different from input!"