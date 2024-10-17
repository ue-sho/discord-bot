from .enlish import contains_japanese, add_audio_to_text

import requests


def add_to_anki(deck_name, front, pronunciation, jp_translation, meaning, example):
    print(f'Adding to Anki: Front: {front}, Pronunciation: {pronunciation}, Japanese Translation: {jp_translation}, Meaning: {meaning}, Example: {example}')
    back = ""

    if pronunciation:
        back += f"【発音】{pronunciation}<br><br>"

    if jp_translation:
        back += f"【日本語訳】{jp_translation}<br><br>"

    if meaning:
        back += f"【英語訳】{meaning}<br><br>"

    if example:
        example = example.replace(front, f'<font color="red">{front}</font>')
        back += f"【例文】{example}"

    if not contains_japanese(front):
        front = add_audio_to_text(front)

    data = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck_name,
                "modelName": "Basic",
                "fields": {
                    "Front": front,
                    "Back": back
                },
                "tags": ["discord"]
            }
        }
    }
    response = requests.post('http://localhost:8765', json=data)
    print(response.text)
    sync_anki()  # 同期を実行

def sync_anki():
    data = {
        "action": "sync",
        "version": 6
    }
    response = requests.post('http://localhost:8765', json=data)
    print(response.text)
