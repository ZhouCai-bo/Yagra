import re
from urls import urls


def application(env, start_response):
	path = env.get('PATH_INFO', '').lstrip('/')
	print(path)
	for regex, callback in urls:
		match = re.search(regex, path)
		if match  is not None:
			return callback(env, start_response)
	
	start_response('200 OK', [('Content_Type', 'text/html')])
	return [b'Hello World']


