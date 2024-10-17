from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    discord_token: str
    discord_channel_id: str
    anki_media_dir: str
    anki_connect_url: str
    deck_name: str

settings = Settings()  # type: ignore
