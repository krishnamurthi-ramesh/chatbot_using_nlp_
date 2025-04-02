import requests
import json

with open("config.json") as config_file:
    config = json.load(config_file)

def get_weather(city="New York"):
    api_key = config["weather_api_key"]
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        return f"🌤 {response['weather'][0]['description'].capitalize()} | Temp: {response['main']['temp']}°C"
    return "Sorry, I couldn't fetch the weather."

def get_news():
    api_key = config["news_api_key"]
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url).json()
    if response.get("articles"):
        return response["articles"][0]["title"]
    return "No news found."

