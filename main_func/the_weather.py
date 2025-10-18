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
        weather_info = respons.json()
        location_name = weather_info['location']['name']
        location_country = weather_info['location']['country']
        current_temp_c = weather_info['current']['temp_c']
        current_feelslike_c = weather_info['current']['feelslike_c']
        current_condition = weather_info['current']['condition']['text']
        current_humidity = weather_info['current']['humidity']

        weather_message = (
            f"🌍 Погода в {location_name}, {location_country}:\n"
            f"☁️ {current_condition}\n"
            f"🌡 Температура: {current_temp_c}°C  (ощущается как {current_feelslike_c}°C)\n"
            f"💧 Влажность: {current_humidity}%")
        return weather_message
