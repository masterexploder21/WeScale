# This file is responsible only for communicating with API and returning data
from PIL._imagingmorph import match
from cassiopeia import Summoner, Champion, get_champion
import cassiopeia as cass


class ApiService:
    riot_api_key = ""

    def __init__(self, settings, riot_api_key):
        cass.apply_settings(settings)
        if riot_api_key is None:
            raise Exception("Environmental variable for Riot API key is not set!")
        cass.set_riot_api_key(riot_api_key)

    def get_summoner(self, name):
        summoner = Summoner(name=name, region='EUNE')
        return summoner

    def get_match_list(self, name, begin_index, end_index):
        matches = cass.get_match_history(summoner=self.get_summoner(name), begin_index=begin_index,
                                         end_index=end_index)
        detailed_matches = list()
        for single_match in list(matches):
            match_details = cass.get_match(id=single_match.id, region='EUNE')
            detailed_matches.append(match_details.to_dict())
        return matches

    def get_match(self, match_id):
        return cass.get_match(id=int(match_id), region='EUNE')

    @staticmethod
    def get_main_participant(name, match_dict):
        return next(filter(lambda x: x['summonerName'] == name, match_dict.participants))
