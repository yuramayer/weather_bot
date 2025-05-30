"""Get current weather for the web"""

import requests


def get_weather() -> tuple:
    """Returns the weather logo & phrase from open meteo"""

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 55.75,
        "longitude": 37.61,
        "current_weather": True
    }
    resp = requests.get(url, params=params, timeout=60)
    code = resp.json()['current_weather']['weathercode']
    return interpret_weather_code(code)


def interpret_weather_code(code: int) -> tuple:
    """Interprete the weather code to the phrase"""

    if code in [0, 1]:
        return "☀️", "Солнечно"
    if code in [2, 3]:
        return "☁️", "Облачно"
    if code in [51, 61, 63, 65, 80, 81, 82]:
        return "🌧️", "Дождь"
    return "❓", "Неизвестно"
