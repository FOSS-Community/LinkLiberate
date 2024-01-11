import random
import string
import validators

from pathlib import Path


def generate_uuid() -> str:
    # Combine uppercase letters, lowercase letters, and digits
    characters: str = string.ascii_letters + string.digits

    # Generate a random 4-character code
    random_code: str = "".join(random.choice(characters) for _ in range(6))

    return random_code


def make_proper_url(url: str) -> str:
    if url.startswith("http://") or url.startswith("https://"):
        return url
    else:
        return f"https://{url}"


def check_link(link: str) -> bool:
    if validators.url(link):
        return True
    return False
