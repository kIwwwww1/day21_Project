from os import getenv
from dotenv import load_dotenv
import httpx

load_dotenv()

API = getenv('API_KEY')
# http://api.weatherapi.com/v1/current.json?    key=860120ca416f45bd8fe174232251810 &   q=London    &   aqi=no

async def get_weather(user_city: str):
    async with httpx.AsyncClient() as client:
        user_url = f'http://api.weatherapi.com/v1/current.json?key={API}&q={user_city}&aqi=no' 
        respons = await client.get(user_url)
        return respons.text
