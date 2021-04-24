from urllib import parse
import MySQLdb
import hashlib
from jinja2 import Environment, FileSystemLoader


def getDigest(string):
	md5 = hashlib.md5()
	md5.update(string.encode('utf8'))
	return md5.hexdigest()


def index(env, start_response):
	start_response('200 OK', [('Content_type', 'text/html')])
	return [b'Hello World']

def yagra(env, start_response):
	file_loader = FileSystemLoader('templates', encoding = 'utf-8')
	e = Environment(loader = file_loader)
	template = e.get_template('yagra/login.html')
	return template.render().encode('utf-8')

def login(env, start_response):
	try:
		request_body_size = int(env.get('CONTENT_LENGTH', 0))
	except(ValueError):
		request_body_size = 0

	request_body = env['wsgi.input'].read(request_body_size)
	data = parse.parse_qs(request_body)
	username = data.get('username', [''])[0]
	password = data.get('password', [''])[0]

	#username = cgi.escape(username)
	
	db = MySQLdb.connect("localhost", "ubuntu", "lijia250", "test_db")
	cursor = db.cursor()
	sql = "SELECT * FROM user_db WHERE username='" +\
		  username + "' AND password='" +\
		  getDigest(password) +\
		  "';"
	cursor.execute(sql)
	results = cursor.fetchall()
	db.close()

	file_loader = FileSystemLoader('templates', encoding = 'utf-8')
	e = Environment(loader = file_loader)
	template = e.get_template('yagra/profile.html')
	return template.render().encode('utf-8')

urls = [
	(r'^$', index),
	(r'yagra/?$', yagra),
	(r'login_event/?$', login)
]
