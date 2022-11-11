import logging
from APIproject.core.utils import get_url

log = logging.getLogger(__name__)

class weather:

    arrayofoptions = ['rain']

    def __init__(self):
        log.info("LOADED WEATHER")
        self.url = 'https://api.open-meteo.com/v1/forecast'

    def weatherOptionSort(self, options:str):
        optionslist = list(options.split(","))
        for current in optionslist:
            if current in self.arrayofoptions:
                pass
            #need to work on sorting input options and then filtering them through. Also need to add them to the url, and then call that all from the API

    def get_weather(self, longitude:float, latitude:float, options:str):
        new_url = f"{self.url}?latitude={latitude}&longitude={longitude}&hourly=temperature_2m"
        log.info(new_url)
        weatherdata = get_url(new_url)
        return weatherdata

