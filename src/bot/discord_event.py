import logging
import discord

from bot.settings import settings
from bot.english import is_english_word_or_phrase, search_word
from bot.anki import add_to_anki

logger = logging.getLogger(__name__)

intents = discord.Intents.default()
client = discord.Client(intents=intents)
intents.message_content = True

COMMAND = "!add"

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not message.content.startswith(COMMAND):
        return

    if str(message.author) != "uesholib":
        await message.channel.send(f"{message.author} のメッセージは受け付けてないよ")
        return

    text = message.content[len(COMMAND) + 1:].strip()
    if is_english_word_or_phrase(text):
        words = text.split()
        if len(words) == 1:
            word = words[0]
            english_word = search_word(word)
            await message.channel.send(f"[{english_word.word}]\npronunciation: {english_word.pronunciation}\nmeaning: {english_word.meaning}\nexample: {english_word.example}")


def discord_run():
    client.run(settings.discord_token)

