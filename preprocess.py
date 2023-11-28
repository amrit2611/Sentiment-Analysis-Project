import emoji
import re
from bs4 import BeautifulSoup
from html import unescape  # Import unescape function

def remove_html_tags_and_urls(text):
    # Use BeautifulSoup to handle HTML entities
    soup = BeautifulSoup(unescape(text), 'html.parser')

    # Remove HTML tags and URLs
    clean_text = re.sub(r'https?://\S+|www\.\S+|<.*?>', '', soup.get_text())

    return clean_text

def replace_emojis(comment):
    return ''.join(c if c not in emoji.UNICODE_EMOJI else ' ' for c in comment)

def convert_to_lowercase(input_file, output_file):
    with open(input_file, "rb") as f:
        # Read bytes, decode to string, and remove leading/trailing whitespaces
        unique_comments = [line.strip() for line in f.readlines()]

    # Remove HTML tags, URLs, and replace emojis
    processed_comments = [replace_emojis(remove_html_tags_and_urls(comment.decode("utf-8")).lower()) if isinstance(comment, bytes) else replace_emojis(remove_html_tags_and_urls(comment.lower())) for comment in unique_comments]

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines('\n'.join(processed_comments))

if __name__ == "__main__":
    input_file = "unique_comments.txt"
    output_file = "output_preprocess.txt"

    convert_to_lowercase(input_file, output_file)
