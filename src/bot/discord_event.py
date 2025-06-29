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
    logger.info(f"We have logged in as {client.user}")
    await tree.sync()


@tree.command(
    name="add-word",
    description="Add English word or phrase to Anki. Only uesho can be used.",
)
async def add_english(interaction: discord.Interaction, text: str):
    if str(interaction.user) != "uesholib":
        await interaction.response.send_message(
            f"{interaction.user} のメッセージは禁止してるよ"
        )
        return

    if is_english_word_or_phrase(text):
        add_to_anki(text)
        await interaction.response.send_message(f"{text} を追加したよ")

@tree.command(
    name="ping",
    description="Ping the bot to check if it's alive.",
)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong! The bot is alive.")


def discord_run():
    logger.info("Attempting to start Discord bot...")
    try:
        client.run(settings.discord_token)
    except Exception as e:
        logger.error(f"Discord bot encountered an error: {e}", exc_info=True)
    logger.info("Discord bot has stopped.")
