from http.cookies import SimpleCookie
from urllib import parse
import MySQLdb
import hashlib
import random
import os
import io
import cgi
from jinja2 import Environment, FileSystemLoader

db_addr = 'localhost'
db_user = 'ubuntu'
db_pwd = 'lijia250'
image_url_prefix = 'images/'

def getDBConn(db_name):
	return MySQLdb.connect(db_addr, db_user, db_pwd, db_name)

def getDigest(string):
	md5 = hashlib.md5()
	md5.update(string.encode('utf-8'))
	return md5.hexdigest()

def getTemplate(name):
	file_loader = FileSystemLoader('templates', encoding = 'utf-8')
	e = Environment(loader = file_loader)
	return e.get_template(name)

def getRequestBody(env):
	try:
		request_body_size = int(env.get('CONTENT_LENGTH', 0))
	except(ValueError):
		request_body_size = 0
	
	#获取http请求体，并编码为uft-8
	request_body = env['wsgi.input'].read(request_body_size)
	request_body = str(request_body, encoding = 'utf-8')
	#解析参数
	return parse.parse_qs(request_body)

def index(env, start_response):
	start_response('200 OK', [('Content_type', 'text/html')])
	return [b'Hello World']

def yagra(env, start_response):
	start_response('200 OK', [('Content_type', 'text/html')])
	template = getTemplate('yagra/login.html')
	return template.render().encode('utf-8')

def login(env, start_response):
	data = getRequestBody(env)
	
	username = data.get('username')[0]
	password = data.get('password')[0]
	
	db = getDBConn('test_db')
	cursor = db.cursor()
	sql = "SELECT * FROM user_db WHERE username=%s AND password=%s;"
	cursor.execute(sql, [username, getDigest(password)])
	results = cursor.fetchall()
	db.close()

	if len(results) != 0:
		start_response('200 OK', 
					   [('Content-type', 'text/html'), 
					    ('Set-Cookie', 'username=' + username),
						('Set-Cookie', 'session=' + str(random.randint(1, 99999)))
					   ]
					  )
		
		#用户还未上传图片,显示默认图片
		if results[0][2] is None:
			image_url = image_url_prefix + 'testBaidu.jpg'
			no_image = True
		else:
			image_url = image_url_prefix + results[0][2]
			no_image = False
		return getTemplate('yagra/profile.html')\
					      .render(image = image_url, 
							      tag = no_image, 
							      username = username)\
						  .encode('utf-8')
	#用户不存在
	start_response('200, OK', [('Content-type', 'text/html')])
	return getTemplate('yagra/login.html')\
					  .render(tip = '*该用户名不存在或密码错误哦！')\
				      .encode('utf-8')

def register(env, start_response):
	data = getRequestBody(env)
	
	username = data.get('username')[0]
	password = data.get('password')[0]
	
	db = getDBConn('test_db')
	cursor = db.cursor()
	sql = "SELECT * FROM user_db WHERE username=%s;"
	cursor.execute(sql, [username])
	results = cursor.fetchall()

	if len(results) == 0:
		sql = "INSERT INTO user_db(username, password) VALUES(%s,%s);"
		cursor.execute(sql, [username, str(getDigest(password))])
		db.commit()
		db.close()
		
		image_url = image_url_prefix + 'testBaidu.jpg'
		
		start_response('200 OK', 
					   [('Content-type', 'text/html'), ('Set-Cookie', 'username=' + username)])
		return getTemplate("yagra/profile.html")\
						   .render(image = image_url, 
							       tag = True, 
							       username = username,)\
						   .encode('utf-8')
	else:
		db.close()
		start_response('200 OK', [('Content-type', 'text/html')])
		return getTemplate("yagra/login.html")\
		                   .render(tip = '*该手机号码已被注册，请直接登录！')\
						   .encode('utf-8')

def upload(env, start_response):
	form = cgi.FieldStorage(fp = env['wsgi.input'], 
							environ = env, 
							keep_blank_values = True)
	image = form['image'].value
	HTTP_COOKIE = env.get('HTTP_COOKIE', '')
	cookie = SimpleCookie(HTTP_COOKIE)
	
	username = cookie.get('username').value

	file_type = os.path.splitext(form['image'].filename)[-1]
	file_name = getDigest(username)

	path = '/home/ubuntu/sources/demo0/images/' + file_name + file_type
	f = open(path, mode = 'wb+')
	f.write(image)
	
	db = getDBConn('test_db')
	cursor = db.cursor()
	sql = "UPDATE user_db SET profile_image=%s WHERE username=%s;"
	cursor.execute(sql, [file_name + file_type, username])
	db.commit()
	db.close()
	image_url = image_url_prefix + file_name + file_type
	
	start_response('200 OK', [('Content-type', 'text/html')])
	return getTemplate('yagra/profile.html')\
					   .render(image = image_url, 
							   tag = False, 
							   username = username)\
					   .encode('utf-8')

def logout(env, start_response):
	cookie = SimpleCookie(env.get('HTTP_COOKIE'))
	cookie['session']['max-age'] = 0
	start_response('200 OK', 
	               [('Content-type', 'text/html'), ('Set-Cookie', cookie.output())])
	return getTemplate('yagra/login.html').render().encode('utf-8')

urls = [
	(r'^$', index),
	(r'yagra/?$', yagra),
	(r'login_event/?$', login),
	(r'register_event/?$', register),
	(r'upload_event/?$', upload),
	(r'logout_event/?$', logout)
]
