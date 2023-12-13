import emoji
import re
from bs4 import BeautifulSoup
from html import unescape, escape

CUSTOM_STOP_WORDS = ["may", "might", "shall", "would", "could", "a", "an", "the"]
CUSTOM_SPECIAL_CHARACTERS = ["*", "&", ",", ".", "<", ">", "+", "/", ":", ";", "«", "»", "=", "(", ")", "[", "]", "{", "}", "\"", "-", "”", "“"]

# Manual contraction expansion mapping
contraction_mapping = {
    "ain't": "am not",
    "aren't": "are not",
    "can't": "cannot",
    "couldn't": "could not",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "Don't": "do not",
    "hadn't": "had not",
    "hasn't": "has not",
    "haven't": "have not",
    "he's": "he is",
    "I'd": "I would",
    "I'll": "I will",
    "I'm": "I am",
    "I’m": "i am",
    "i’m": "i am",
    "i'm": "i am",
    "I've": "I have",
    "isn't": "is not",
    "it's": "it is",
    "let's": "let us",
    "mustn't": "must not",
    "shan't": "shall not",
    "she's": "she is",
    "shouldn't": "should not",
    "that's": "that is",
    "there's": "there is",
    "they're": "they are",
    "we're": "we are",
    "weren't": "were not",
    "what's": "what is",
    "where's": "where is",
    "who's": "who is",
    "won't": "will not",
    "wouldn't": "would not",
    "you'd": "you would",
    "you'll": "you will",
    "you're": "you are",
    "you've": "you have",
    "people’s": "people",
    "who’s": "who has",
    "y’all": "you all",
    "didn’t": "did not",
    "can’t": "can not",
    "she’s": "she is",
    "don’t": "do not",
    "kardashian’s": "kardashians",
    "they’re": "they are",
    "it’s": "it is",
    "billionaireit’s": "billionaire it is",
    "doesn’t": "does not",
    "hadn’t": "had not",
    "that’s": "that is ",
    "i’ve": "i have",
    "monroe’s": "monroes",
    "you’re": "you are",
    "‘": "'",
    "’": "'",
    "couldn’t": "could not",
    "they've": "they have",
    "wasn't": "was not",
    "i've": "i have",
    "They've": "They have",
    "Wasn't": "was not",
    "i'd": "i would",
    "5'10": "5 10",
    "sheep's": "sheeps",
    "Couldn't": "could not",
    "here's": " here is",
    "idiot's": "idiots",
    "i'll": "i will",
    "apple's": "apple",
    "l'oreal": "loreal",
    "donald's": "donalds",
    "mcdonald's": "mcdonalds",
    "d'esprit": "desprit",
    "c'est": "cest",
    "y'a": "ya",
    "country's": "country is",
    "tati's": "tatis",
    "40's": "40s",
    "companies'": "companies",
    "company's": "companies",
    "parent's": "parents",
    "we've": "we have",
    "would've": "would have",
    "one's": "ones",
    "jamie's": "jamies",
    "b'i": "but i",
    "wong's": "wongs",
    "man's": "mans",
    "must've": "must have",
    "should've": "should have",
    "asperger's": "aspergers",
    "body's": "bodys",
    "kid's": "kids",
    "disney's": "disneys",
    "wade's": "wades",
    "5'3": "5 3",
    "james's": "james",
    "colour's": "colours",
    "grandmother's": "grandmothers",
    "baby's": "babys",
    "father's": "fathers",
    "let's":"let us",
    "else's": "elses",
    "berry's": "berrys",
    "blessing's": "blessings",
    "pete's": "petes",
    "god's": "gods",
    "person's": "persons",
    "they'll": "they will",
    "jaimie's": "jaimies",
    "it'll": "it will",
    "could've": "could have",
    "it'llnever": "it will never",
    "it'll": "it will",
    "might've": "might have",
    "drunk'n": "drunk and",
    "doctor's": "doctors",
    "ain't": "is not",
    "couldn't": "could not",
    "couldn’t": "could not",
    "women's": "womens",
    "couldn't": "could not",
    "haven't": "have not",
    "they'd": "they would",
    "you've": "you have",
    "n't": " not",
    "'ll": " will",
    "c'mon": "come on",
    "i'm": "i am",
    "werne't": "were not",
    "she'd": "she would"
}

def remove_html_tags_and_urls(text):
    soup = BeautifulSoup(unescape(text), 'html.parser')
    clean_text = re.sub(r'https?://\S+|www\.\S+|<.*?>', '', soup.get_text())
    return clean_text

def replace_emojis(comment):
    comment = comment[2:] if comment.startswith("b'") else comment
    comment = re.sub(r'\\x[0-9a-fA-F]{2}', lambda x: bytes.fromhex(x.group(0)[2:]).decode('utf-8', 'ignore'), comment)
    return emoji.demojize(comment)

def clean_special_characters(comment):
    cleaned_comment = re.sub(r'(?<!\w)\'|\'(?!\w)|(?<! )([?!%])', r' \1 ', comment)
    cleaned_comment = cleaned_comment.replace('%', 'percentage_symbol')
    cleaned_comment = cleaned_comment.replace('!', 'exclamation_symbol').replace('?', 'question_symbol')

    for char in CUSTOM_SPECIAL_CHARACTERS:
        cleaned_comment = cleaned_comment.replace(char, '')
    
    return cleaned_comment

def remove_stopwords(comment):
    tokens = comment.split()
    filtered_tokens = [word for word in tokens if word.lower() not in CUSTOM_STOP_WORDS]
    return ' '.join(filtered_tokens)

def expand_contractions_manually(text):
    for contraction, expansion in contraction_mapping.items():
        text = text.replace(contraction, expansion)

    return text
def convert_to_lowercase(input_file, output_file):
    with open(input_file, "rb") as f:
        unique_comments = [line.strip() for line in f.readlines()]

    processed_comments = [
        expand_contractions_manually(
        remove_stopwords(
            clean_special_characters(
                replace_emojis(
                    remove_html_tags_and_urls(
                            comment.decode("utf-8") if isinstance(comment, bytes) else comment                
                    ).lower()
                )
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
    convert_to_lowercase(output_file, output_file)