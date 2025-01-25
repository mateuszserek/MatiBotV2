from dotenv import load_dotenv
from os import getenv

def get_token(name: str) -> str:
    load_dotenv()
    return getenv(name)