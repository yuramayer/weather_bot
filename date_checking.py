months = ['июль', 'июля', 'август', 'августа', 'авг']

date_dict = {}

# date checking
def is_right_format(date: str) -> bool:
	"""Checking date type for dot/whitespace between integers"""
	if '.' in date:
		a, b, *_ = date.split('.') # *_ for all the other unpacking values
		if a.isdigit() and b.isdigit():
			date_dict['type'] = 'int_dot_int'
			date_dict['day'] = a
			date_dict['month'] = b
			return True

	elif ' ' in date:
		a, b, *_ = date.split(' ') 
		if a.isdigit() and b.isdigit():
			date_dict['type'] = 'int_space_int'
			date_dict['day'] = a
			date_dict['month'] = b
			return True

		elif a.isdigit() and isinstance(b, str):
			date_dict['type'] = 'int_space_str'
			date_dict['day'] = a
			date_dict['month'] = b
			return True


def is_right_date(date: str) -> bool:
	"""Checking date type for range"""
	day = date_dict['day']
	month = date_dict['month']

	if date_dict['type'] == 'int_dot_int' or date_dict['type'] == 'int_space_int':
		if int(day) in range(0, 32) and int(month) in range(7, 9):
			return True
	
	elif date_dict['type'] == 'int_space_str':
		if int(day) in range(0, 32) and month in months:
			return True


# getting link w/ date
def date_for_link(date: str) -> str:
	"""Transform date to link"""
	day = date_dict['day']
	month = date_dict['month']
	
	if date_dict['type'] == 'int_dot_int' or date_dict['type'] == 'int_space_int':
		if int(month) == 7:
			month = 'july'
		elif int(month) == 8:
			month = 'august'
		return '{}-{}/'.format(day, month)

	elif date_dict['type'] == 'int_space_str':
		if 'ю' in month:
			month = 'july'
		elif 'г' in month:
			month = 'august'
		return '{}-{}/'.format(day, month)


# return date link or None
def get_date_url(date: str) -> str:
	"""Returning date url or None"""
	if is_right_format(date):
		if is_right_date(date):
			return date_for_link(date)


# return main link or None
def get_url(date: str, serv_url: str) -> str:
	"""Returning main url or None"""
	url_date = get_date_url(date)
	if url_date:
		return serv_url + url_date

# get day & month for post
def return_date():
	"""Returning day and month from date_dict"""
	day = date_dict['day']
	month = date_dict['month']
	return day, month
