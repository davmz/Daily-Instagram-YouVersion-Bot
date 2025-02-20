import datetime

def format_verse_reference(verse_reference):
    """Formats the verse reference by removing spaces and replacing `:` with `.`."""
    return verse_reference.replace(" ", "").replace(":", ".")

def generate_filename(verse_reference):
    """Generates a filename in the format YYYY-MM-DD_VOTD_versereference.png"""
    now = datetime.datetime.now()
    formatted_reference = format_verse_reference(verse_reference)  # 🛠 Apply formatting fix
    return f"{now.strftime('%Y-%m-%d')}_VOTD_{formatted_reference}.png"