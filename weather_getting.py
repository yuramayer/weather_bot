import requests
from bs4 import BeautifulSoup as BS
import re
from typing import Dict

page_type_dict = {}
weather_dict = {}


# web-page checking 
def is_ok(r) -> bool:
	"""Return True when we get the page"""
	if r.status_code == 200:
		return True


# checking the type (we've got two types: generalized and detailed)
def check_page_type(html) -> None:
	"""Enter the page type (general, detail) to page_type_dict"""
	temp_lst = html.findAll('div', {'class': '_1HBR'})
	if temp_lst:
		page_type_dict['general'] = True
		page_type_dict['detail'] = False
	else:
		page_type_dict['general'] = False
		page_type_dict['detail'] = True


# import temperature to the weather dict
def get_temp(html) -> None:
	"""Getting the temperature from web-page"""
	if page_type_dict['general']:
		t_text = html.find('div', {'class': '_1HBR'}).text
		t_digit = ''.join([i for i in t_text if i.isdigit()])
		weather_dict['temperature'] = t_digit
	else:
		re_temp_class = re.compile('.*_2ezK.*') # regex template: str w/ '_2ezK'
		temp_class = html.find('div', {'class': re_temp_class}) 
		# we've got smth like: 'Ночью14°Утром19°Днём24°Вечером22°
		weather_lst = temp_class.text.split('°') # ['Ночью14','Утром19',...]
		int_weather_lst = [int(number.group()) for number in ( # for all the elems 
			re.search(r'\d+', word) for word in weather_lst) if number] # keep integers
		# result: [14, 19, 24, 22]
		weather_dict['temperature'] = int_weather_lst


# we've got a lot of params on the website in the table
def get_table(html) -> None:
	"""Getting precipation, wind, pressure and all the other stuff"""
	re_table_class = re.compile('.*2iSP.*') # familiar regex template (str w/ '2iSP')
	table_class = html.find('div', {'class': re_table_class})
	table_lst = re.findall('[А-Я|A-Z][^А-Я|A-Z]*', table_class.text) # regex for capitals

	for param in table_lst:
		if 'Осадки' in param:
			weather_dict['precipation'] = re.search(r'\d+', param).group()
		elif 'Ветер' in param:
			weather_dict['wind'] = re.search(r'\d+', param).group()
		elif 'Давление' in param:
			weather_dict['pressure'] = re.search(r'\d+', param).group()
		elif 'Восход' in param:
			weather_dict['sunrise'] = ':'.join(re.findall(r'\d+', param))
		elif 'Закат' in param:
			weather_dict['sunset'] = ':'.join(re.findall(r'\d+', param))


# all the weather functions together
def get_weather(html):
	"""Filling and return the weather_dict"""
	check_page_type(html)
	get_temp(html)
	get_table(html)
	return weather_dict
