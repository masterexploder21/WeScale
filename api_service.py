# This file is responsible only for communicating with API and returning data

from cassiopeia import Summoner, Champion, get_champion
from cassiopeia.datastores.riotapi.common import APIError
import cassiopeia as cass


class ApiService:
    riot_api_key = ""

    def __init__(self, settings, riot_api_key):
        cass.apply_settings(settings)
        if riot_api_key is None:
            raise Exception("Environmental variable for Riot API key is not set!")
        cass.set_riot_api_key(riot_api_key)

    def print_summoner(name: str, region: str):
        summoner = Summoner(name=name, region=region)
        print("Name:", summoner.name)
        print("ID:", summoner.id)
        print("Account ID:", summoner.account_id)
        print("Level:", summoner.level)
        print("Ranks:", summoner.ranks)
