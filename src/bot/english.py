import os
import string

import requests
from bs4 import BeautifulSoup
from gtts import gTTS
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

ANKI_MEDIA_DIR = (
    "/Users/uesho/Library/Application Support/Anki2/User 1/collection.media"
)
MAX_RETRIES = 3


def is_english_word_or_phrase(text: str) -> bool:
    words = text.split()
    return all(word.isalpha() for word in words)


def contains_japanese(text: str) -> bool:
    for char in text:
        if "\u0800" <= char <= "\u4e00":
            return True
    return False


def clean_filename(filename: str) -> str:
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return "".join(c for c in filename if c in valid_chars)


def add_audio_to_text(text: str) -> str:
    try:
        tts = gTTS(text, lang="en")
    except Exception as e:
        print(f"Unable to generate sound for {text}: {e}")
        return text

    filename = clean_filename(text)
    audio_file = f"{filename}.mp3"
    audio_path = os.path.join(ANKI_MEDIA_DIR, audio_file)
    tts.save(audio_path)
    return f"{text} [sound:{audio_file}]"


class EnglishWord:
    def __init__(
        self, word: str, meaning: str, etymology: str, example: str, situation: str
    ):
        self.word = word
        self.meaning = meaning
        self.etymology = etymology
        self.example = example
        self.situation = situation


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

    url = f"https://dictionary.cambridge.org/us/dictionary/english/{word.lower()}"
    response = session.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        pronunciation = soup.find("span", class_="ipa dipa lpr-2 lpl-1").text.strip()
    except AttributeError:
        pronunciation = None

    try:
        meaning = (
            soup.find(class_="def-block ddef_block")
            .find("div", class_="def ddef_d db")
            .text.strip()
        )
    except AttributeError:
        meaning = None

    try:
        example = (
            soup.find(class_="def-block ddef_block")
            .find("div", class_="examp dexamp")
            .text.strip()
        )
    except AttributeError:
        example = None

    return EnglishWord(word, pronunciation, meaning, example)


def fetch_image_url(text: str):
    search_query = f"{text} picture Pexels"  # 検索クエリ
    search_url = f"https://www.google.com/search?tbm=isch&q={search_query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    img_tags = soup.find_all("img")

    if len(img_tags) > 1:
        return img_tags[1]["src"]  # 最初の画像を無視して2番目の画像を取得
    return None
