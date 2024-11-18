import requests
from octorest import OctoRest




def get_data_from_octoprint(url):
    api = OctoRest(url, apikey)
    response = api.get(url)
    data = response.json()
    return data