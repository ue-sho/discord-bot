import logging
import discord

from bot.settings import settings
from bot.english import is_english_word_or_phrase
from bot.anki import add_to_anki

logger = logging.getLogger(__name__)

intents = discord.Intents.default()
client = discord.Client(intents=intents)
intents.message_content = True

COMMAND = "!add"


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not message.content.startswith(COMMAND):
        return

    if str(message.author) != "uesholib":
        await message.channel.send(f"{message.author} のメッセージは受け付けてないよ")
        return

    text = message.content[len(COMMAND) + 1 :].strip()
    if is_english_word_or_phrase(text):
        add_to_anki(text)
        await message.channel.send("追加したよ")


def discord_run():
    client.run(settings.discord_token)
