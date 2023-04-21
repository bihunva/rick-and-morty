import requests
from django.conf import settings

from characters.models import Character


def scrape_characters() -> list[Character]:
    next_url_to_scrape = settings.RICK_AND_MORTY_API_CHARACTERS_URL

    characters = []
    while next_url_to_scrape is not None:
        characters_response = requests.get(next_url_to_scrape).json()

        for character_data in characters_response["results"]:
            characters.append(
                Character(
                    api_id=character_data["id"],
                    name=character_data["name"],
                    status=character_data["status"],
                    species=character_data["species"],
                    gender=character_data["gender"],
                    image=character_data["image"],
                )
            )

        next_url_to_scrape = characters_response["info"]["next"]

    return characters


def save_characters(characters: list[Character]) -> None:
    for characters in characters:
        characters.save()


def sync_characters_with_api() -> None:
    characters = scrape_characters()
    save_characters(characters)
