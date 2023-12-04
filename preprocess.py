import emoji
import re
from bs4 import BeautifulSoup
from html import unescape, escape  # Import escape function

CUSTOM_STOP_WORDS = ["may", "might", "shall", "would", "could", "a", "an", "the"]
CUSTOM_SPECIAL_CHARACTERS = ["*", "&", ",", ".", "<", ">", "+", "/", ":", ";", "«", "»", "=", "(", ")", "[", "]", "{", "}", "\""]

def remove_html_tags_and_urls(text):
    # Use BeautifulSoup to handle HTML entities
    soup = BeautifulSoup(unescape(text), 'html.parser')

    # Remove HTML tags and URLs
    clean_text = re.sub(r'https?://\S+|www\.\S+|<.*?>', '', soup.get_text())

    return clean_text

def replace_emojis(comment):
    # Remove 'b' prefix if present
    comment = comment[2:] if comment.startswith("b'") else comment

    # Replace byte-encoded emojis
    comment = re.sub(r'\\x[0-9a-fA-F]{2}', lambda x: bytes.fromhex(x.group(0)[2:]).decode('utf-8', 'ignore'), comment)
    
    # Apply demojize
    return emoji.demojize(comment)

def clean_special_characters(comment):
    # Ensure there is at least one space before and after symbols like ?, !, and %
    cleaned_comment = re.sub(r'(?<! )([?!%])', r' \1 ', comment)
    
    # Replace % symbol with 'percentage_symbol'
    cleaned_comment = cleaned_comment.replace('%', 'percentage_symbol')
    
    # Replace ! and ? symbols with 'exclamation_symbol' and 'question_symbol' respectively
    cleaned_comment = cleaned_comment.replace('!', 'exclamation_symbol').replace('?', 'question_symbol')

    # Remove specified special characters
    for char in CUSTOM_SPECIAL_CHARACTERS:
        cleaned_comment = cleaned_comment.replace(char, '')
    
    return cleaned_comment

def remove_stopwords(comment):
    tokens = comment.split()
    filtered_tokens = [word for word in tokens if word.lower() not in CUSTOM_STOP_WORDS]
    return ' '.join(filtered_tokens)

def convert_to_lowercase(input_file, output_file):
    with open(input_file, "rb") as f:
        # Read bytes, decode to string, and remove leading/trailing whitespaces
        unique_comments = [line.strip() for line in f.readlines()]

    # Remove HTML tags, URLs, replace emojis, clean special characters, remove custom stop words
    processed_comments = [
        remove_stopwords(
            clean_special_characters(
                replace_emojis(
                    remove_html_tags_and_urls(
                        comment.decode("utf-8") if isinstance(comment, bytes) else comment
                    ).lower()
                )
            )
        )
        for comment in unique_comments
    ]

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines('\n'.join(processed_comments))

if __name__ == "__main__":
    input_file = "unique_comments.txt"
    output_file = "output_preprocess.txt"

    convert_to_lowercase(input_file, output_file)
