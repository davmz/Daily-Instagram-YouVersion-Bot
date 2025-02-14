from PIL import Image

def crop_image(input_filename, output_filename, margin_percent=0.02):
    """Crops the image to remove white edges while preserving quality."""
    try:
        with Image.open(input_filename) as img:
            width, height = img.size
            crop_margin = int(height * margin_percent)  # Dynamically adjust based on image size
            
            # Crop the image but keep high quality
            cropped_img = img.crop((crop_margin, crop_margin, width - crop_margin, height - crop_margin)).copy()
            
            # Save with max quality
            cropped_img.save(output_filename, format="PNG", optimize=True)
        
        print(f"✅ Cropped image saved as {output_filename} (High Quality)")
        return output_filename

    except Exception as e:
        print(f"❌ Error cropping image: {e}")
        return input_filename  # If cropping fails, return original