import emoji
import re
from bs4 import BeautifulSoup

def remove_html_tags(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()

def replace_emojis(comment):
    return emoji.demojize(comment)

def convert_to_lowercase(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        unique_comments = f.readlines()

    # Remove HTML tags and replace emojis
    processed_comments = [replace_emojis(remove_html_tags(comment.lower())) for comment in unique_comments]

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(processed_comments)

if __name__ == "__main__":
    input_file = "unique_comments.txt"
    output_file = "output_preprocess.txt"

    convert_to_lowercase(input_file, output_file)
