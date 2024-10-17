import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import string
import os
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

ANKI_MEDIA_DIR = "/Users/user_name/Library/Application Support/Anki2/User 1/collection.media"

MAX_RETRIES = 3





def is_english_word_or_phrase(text):
    words = text.split()
    return all(word.isalpha() for word in words)

def contains_japanese(text):
    for char in text:
        if '\u0800' <= char <= '\u4e00':
            return True
    return False

def clean_filename(filename):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in filename if c in valid_chars)

def add_audio_to_text(text):
    try:
        tts = gTTS(text, lang='en')
    except Exception as e:
        print(f"Unable to generate sound for {text}: {e}")
        return text

    filename = clean_filename(text)
    audio_file = f'{filename}.mp3'
    audio_path = os.path.join(ANKI_MEDIA_DIR, audio_file)
    tts.save(audio_path)
    return f'{text} [sound:{audio_file}]'


@retry(
    stop=stop_after_attempt(MAX_RETRIES),
    wait=wait_exponential(),
    retry=retry_if_exception_type(requests.exceptions.RequestException),
)
def search_word(word):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134"
    }

    url = f'https://dictionary.cambridge.org/us/dictionary/english/{word.lower()}'
    response = session.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        pronunciation = soup.find('span', class_='ipa dipa lpr-2 lpl-1').text.strip()
    except AttributeError:
        pronunciation = None

    try:
        meaning = soup.find(class_='def-block ddef_block').find('div', class_='def ddef_d db').text.strip()
    except AttributeError:
        meaning = None

    try:
        example = soup.find(class_='def-block ddef_block').find('div', class_='examp dexamp').text.strip()
    except AttributeError:
        example = None

    # Japanese translation
    jp_url = f'https://eow.alc.co.jp/search?q={word}'
    try:
        jp_response = session.get(jp_url, headers=headers, timeout=10)
        jp_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while searching for Japanese translation of '{word}': {e}")
        return pronunciation, None, meaning, example

    jp_soup = BeautifulSoup(jp_response.text, 'html.parser')
    try:
        jp_translation_full = jp_soup.find('meta', {'name': 'description'}).get('content')
        jp_translation_parts = jp_translation_full.split('...【発音】')  # Split on the delimiter
        jp_translation = jp_translation_parts[0]  # Only keep the first part
    except AttributeError:
        jp_translation = None

    return pronunciation, jp_translation, meaning, example






