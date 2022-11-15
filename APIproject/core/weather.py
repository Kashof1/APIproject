import logging
from urllib.parse import quote, urlencode
from APIproject.core.utils import get_url
from APIproject.core.utils import get_url

log = logging.getLogger(__name__)

class weather:

    arrayofoptions = ["temperature_2m", "relativehumidity_2m", "rain", "weathercode", "visibility"]

    def __init__(self):
        log.info("LOADED WEATHER")
        self.base_url = 'https://api.open-meteo.com/v1/forecast'


    def get_weather(self, latitude: float, longitude: float, options: str):
        options = self.validate_options(options=options)
        if len(options) == 0:
            return "No options provided"
        data = {"latitude": latitude, "longitude": longitude}
        query = urlencode(data, True)
        query = quote(query, safe='=&')
        url = f"{self.base_url}?{query}&hourly={options}"
        data = get_url(url)
        return data

    def validate_options(self, options:str):
        options = options.split(",")
        options = [item for item in options if item in self.arrayofoptions]
        return ",".join(options)