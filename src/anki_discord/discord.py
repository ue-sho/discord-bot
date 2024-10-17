import discord
from .settings import settings
from .english import is_english_word_or_phrase, search_word
from .anki import add_to_anki

intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.channel.id != settings.discord_channel_id or message.author == client.user:
        return

    text = message.content.strip()
    if is_english_word_or_phrase(text):
        words = text.split()
        if len(words) == 1:
            word = words[0]
            pronunciation, jp_translation, meaning, example = search_word(word)
            if pronunciation or jp_translation or meaning or example:
                add_to_anki(settings.deck_name, word, pronunciation, jp_translation, meaning, example)
            else:
                add_to_anki(settings.deck_name, word, "", "", word, "")  # 単語が見つからない場合、その単語を表と裏にセット
        else:
            phrase = text
            add_to_anki(settings.deck_name, phrase, "", "", phrase, "")  # フレーズの場合、そのフレーズを表と裏にセット

def discord_run():
    client.run(settings.discord_token)

