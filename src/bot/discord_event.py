import logging

import discord
from discord import app_commands

from bot.anki import add_to_anki
from bot.english import is_english_word_or_phrase
from bot.settings import settings

logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    await tree.sync()


@tree.command(
    name="add-word",
    description="Add English word or phrase to Anki. Only uesho can be used.",
)
async def add_english(interaction: discord.Interaction, text: str):
    print(str(interaction.user))
    if str(interaction.user) != "uesholib":
        await interaction.response.send_message(
            f"{interaction.user} のメッセージは禁止してるよ"
        )
        return

    if is_english_word_or_phrase(text):
        add_to_anki(text)
        await interaction.response.send_message("追加したよ")


def discord_run():
    client.run(settings.discord_token)
