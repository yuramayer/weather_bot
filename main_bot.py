import requests
from bs4 import BeautifulSoup as BS
from date_checking import get_url, return_date
from weather_getting import is_ok, get_weather
import telebot
import config

# serv - weather.rambler.ru
serv_url = 'https://weather.rambler.ru/v-yaroslavle/'


bot = telebot.TeleBot(config.token)


# handler for new messages 
@bot.message_handler(commands=['start', 'new'])
def welcome(message):
	bot.send_message(message.chat.id, '{}{}{}{} Отправь мне дату в июле или августе, и я подскажу прогноз погоды в Ярославле на твое число. \n\n{} Я принимаю дату как через точку, так и через пробел, и даже знаю слова!'.format(chr(0x1F481), chr(0x200D), chr(0x2640), chr(0xFE0F), chr(0x270C)))
	bot.register_next_step_handler(message, send_weather)


def send_weather(message) -> None:
	"""Sending the message to user"""
	weather_dict = fill_weather_dict(message) # filling the weather_dict
	if weather_dict:
		day, month = return_date()
		forecast = new_message(day, month, weather_dict)
		bot.send_message(message.chat.id, forecast, parse_mode='Markdown')
	else:
		bot.send_message(message.chat.id, '{} Попробуй еще раз, в формате "29.07", "30 08" или "8 августа". Для нового запроса нажми /new'.format(chr(0x1F914)))


def fill_weather_dict(message):
	"""Getting the weather_dict with all the params"""
	date = message.text
	url = get_url(date, serv_url)
	if url:
		r = requests.get(url)
		if is_ok(r):
			html = BS(r.content, 'html.parser')
			return get_weather(html)


def new_message(day: str, month: str, weather_dict) -> str:
	"""Creating message w/ weather"""
	forecast = '*Прогноз погоды в Ярославле на {} {}*:\n\n\n'.format(day, month)
	if 'temperature' in weather_dict:
		temp = weather_dict['temperature']
		if isinstance(temp, str):
			forecast += '{} *Температура*: _{}°C_\n\n'.format(chr(0x26A1), temp)
		else:
			forecast += '{} *Температура*:\n\n{} Ночью: {}°C\n\n{} Утром: {}°C\n\n{} Днем: {}°C\n\n{} Вечером: {}°C\n\n'.format(chr(0x26A1), chr(0x1F567), temp[0], chr(0x1F562), temp[1], chr(0x1F55C), temp[2], chr(0x1F564), temp[3])
	if 'precipation' in weather_dict:
		forecast += '{} *Ожидаемые осадки*: {}%\n\n'.format(chr(0x1F327), weather_dict['precipation'])
	else:
		forecast += '{} *Осадков* не ожидается!\n\n'.format(chr(0x2600))
	if 'pressure' in weather_dict:
		forecast += '{} *Давление*: {} мм\n\n'.format(chr(0x1F321), weather_dict['pressure'])
	if 'wind' in weather_dict:
		forecast += '{} *Скорость ветра*: {} м/с\n\n'.format(chr(0x1F4A8), weather_dict['wind'])
	if 'sunrise' in weather_dict:
		forecast += '{} *Рассвет*: {}\n\n'.format(chr(0x1F305), weather_dict['sunrise'])
	if 'sunset' in weather_dict:
		forecast += '{} *Закат*: {}\n\n'.format(chr(0x1F307), weather_dict['sunset'])
	forecast += '{} _Для нового прогноза нажми /new!_'.format(chr(0x1F449))
	return forecast




if __name__ == '__main__':
	while True:
		try:
			bot.polling(none_stop=True)
		except Exception:
			pass