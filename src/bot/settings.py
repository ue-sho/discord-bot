from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    discord_token: str
    anki_media_dir: str
    anki_connect_url: str
    deck_name: str
    openai_api_key: str


settings = Settings()  # type: ignore
