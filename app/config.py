import os


class Config:
    DEBUG = True
    TOKEN = os.getenv('token_telegram_bot')