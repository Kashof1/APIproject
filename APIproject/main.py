import logging
import os
from pathlib import Path
from typing import Union
from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from APIproject.core.weather import weather

logs_file = Path(Path().resolve(), "log.txt")
logs_file.touch(exist_ok=True)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=os.environ.get("LOGLEVEL", "INFO"),
    handlers=[logging.FileHandler(logs_file), logging.StreamHandler()],
)

log = logging.getLogger(__name__)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

weather_api = weather()


@app.get("/items/{item_id}")
async def read_item(item_id):
    log.info(f"loaded item {item_id}")
    return {"item_id": item_id}


@app.get("/weather")
def get_weather(latitude: float = 51.5002, longitude: float = -0.120000124, options:str=""):
    log.info(options)
    log.info(f"Requested latitude: {latitude} and longitude: {longitude}")
    output = weather_api.get_weather(longitude=longitude, latitude=latitude,options=options)
    return {"weather": output}


@app.get("/", response_class=HTMLResponse)
def html_output(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "data": ["hello", 1, False]},
    )

@app.get("/chart", response_class=HTMLResponse)
def chart_output(request: Request, latitude: float = 51.5002, longitude: float = -0.120000124, city="London", options:str = "temperature_2m", limit:int=50):
    data = weather_api.get_weather(latitude=latitude, longitude=longitude, options=options)
    labels_list = data['hourly']['time'][:limit]
    values_list = data['hourly']['temperature_2m'][:limit]
    labels = ",".join(labels_list)
    values = str(values_list)[1:-1]
    labelsvaluespair = []
    for x in range (len(labels_list)):
        labelsvaluespair.append([labels_list[x], values_list[x]])
    return templates.TemplateResponse(
        "weather.html",
        {"request": request, "data": [data, labels, values, labelsvaluespair], "city": [city.title(), latitude, longitude]},
    )

@app.post("/weather_send")
async def weather_send(request: Request, city:str=Form(), rain: Optional[str] = Form(None)):
    cities = {"berlin": [52.52, 13.41], "london": [51.51, -0.13], "paris": [48.8566, 2.3522]}
    options = "temperature_2m"
    if rain:
        options +=",rain"
    if city in cities:
        return chart_output(request=request, latitude=cities[city][0], longitude=cities[city][1], options=options, city=city.title())
    return chart_output(request=request,options=options, city=city.title())
