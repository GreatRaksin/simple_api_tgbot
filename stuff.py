import requests as r
import geopy
import os
from datetime import datetime

def read_file(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def git_search(query, language):
    url = 'https://api.github.com/search/repositories'
    params = {'q': query,
              'l': language}
    res = r.get(url, params=params).json()
    message = ''
    for repo in res['items']:
        message += f'<a href="{repo["svn_url"]}">{repo["name"]}</a>\n'
    return message


def get_image():
    content = r.get('https://random.dog/woof.json').json()
    url = content['url']
    return url


def get_city(lat, lon):
    locator = geopy.geocoders.Nominatim(user_agent='geoapiExercises')
    location = locator.reverse(str(lat) + "," + str(lon))
    address = location.raw['address']
    return address


def get_forecast(lat, lon):
    weather_codes = {
        'пасмурно': '☁️ пасмурно',
        'облачно с прояснениями': '🌤️ облачно с прояснениями',
        'небольшой дождь': '🌨 небольшой дождь',
        'переменная облачность': '🌥️ переменная облачность',
        'ясно': '☀️ ясно'
    }
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    params = {
        'lat': lat,
        'lon': lon,
        'appid': os.environ.get('WEATHER_KEY'),
        'units': 'metric',
        'lang': 'ru',
    }
    resp = r.get(url, params=params).json()
    text = '🗓️<strong>{}</strong> <i>{}</i>: \n{}°С, {}\n\n'
    res = ''

    for data in resp['list']:
        date = datetime.fromtimestamp(data["dt"])

        date_res = date.strftime('%d.%m.%y')
        temp = data['main']['temp']
        weather = weather_codes[data['weather'][0]['description']] or data['weather'][0]['description']

        if date.hour == 15:
            daytime = 'днём'
            res += text.format(date_res, daytime, temp, weather)
        elif date.hour == 21:
            daytime = 'вечером'
            res += text.format(date_res, daytime, temp, weather)
    return res
