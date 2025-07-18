
import random
import requests
from telegram import Update
from telegram.ext import CallbackContext
from config import WEATHER_API_KEY, CITY_NAME

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    data = requests.get(url).json()
    weather = data['weather'][0]['description']
    temp = data['main']['temp']
    return f"{weather}, {temp}°C"

def generate_recommendation(route_number, weather_desc, load_percent):
    recommendation = ""
    if load_percent > 90:
        recommendation += "🔴 Высокая загруженность маршрута. Добавьте 1–2 единицы транспорта. "
    elif load_percent < 30:
        recommendation += "🟢 Низкая загрузка. Возможна оптимизация интервалов. "
    else:
        recommendation += "🟡 Средняя загрузка. Работайте в штатном режиме. "

    if "дожд" in weather_desc or "снег" in weather_desc:
        recommendation += "Учитывайте погодные условия: возможны задержки. "

    return f"📍 Маршрут №{route_number}\n👥 Загруженность: {load_percent}%\n🌦 Погода: {weather_desc}\n\n💡 {recommendation}"

def handle_text(update: Update, context: CallbackContext):
    text = update.message.text.strip()

    if text.isdigit():
        route = int(text)
        weather = get_weather(CITY_NAME)
        load = random.randint(30, 100)
        reply = generate_recommendation(route, weather, load)
        update.message.reply_text(reply)
    else:
        update.message.reply_text("Введите номер маршрута (только цифры).")
