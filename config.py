import os

from dotenv import load_dotenv

DOTENV_PATH = ".env"


class Config:
    def __init__(self):
        load_dotenv(DOTENV_PATH)
        self.private_key = os.getenv("MARVEL_PRIVATE_KEY")
        self.public_key = os.getenv("MARVEL_PUBLIC_KEY")
