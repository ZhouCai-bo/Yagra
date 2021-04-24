#from flask import Flask, request, render_template, session
#import MySQLdb
import hashlib
#import os
import re
from urls import urls
#import cgi

'''
app = Flask(__name__)
app.debug = True
app.secret_key = 'secret_key'
image_url_prefix = 'images/'
'''


def doSQL():
	return 0

def application(env, start_response):
	path = env.get('PATH_INFO', '').lstrip('/')
	print(path)
	for regex, callback in urls:
		print(111)
		match = re.search(regex, path)
		if match  is not None:
			return callback(env, start_response)
	print(222)
	start_response('200 OK', [('Content_Type', 'text/html')])
	return [b'Hello World']
'''
@app.route('/')
def hello():
    return 'hello world'

@app.route('/index/')
def index():
    return render_template('index.html')

@app.route('/profile/')
def profile():
    return render_template('profile.html') 

@app.route('/yagra/')
def yagra():
	return render_template('yagra/login.html')

@app.route('/login_event', methods = ['GET', 'POST'])
def login_event():
	if request.method == 'GET':
		return render_template('yagra/login.html')
	else:
		username = request.form.get('username')
		password = request.form.get('password')
		
		db = MySQLdb.connect("localhost", "ubuntu", "lijia250", "test_db")
		cursor = db.cursor()
		sql = "SELECT * FROM user_db WHERE username='" +\
			  username + "' AND password='" +\
			  getDigest(password) +\
			  "';"
		cursor.execute(sql)
		results = cursor.fetchall()
		db.close()

		if len(results) != 0:
			session['username'] = username
			#用户还未上传图片
			if results[0][2] is None:
				image_url = image_url_prefix + 'testBaidu.jpg'
				no_image = True
			else:
				image_url = image_url_prefix + results[0][2]
				no_image = False
			return render_template("yagra/profile.html", 
								   image = image_url, 
								   tag = no_image, 
								   username = username)
		#用户不存在
		return render_template('yagra/login.html', tip = '*该用户名不存在或密码错误哟！')

@app.route('/register_event', methods = ['GET', 'POST'])
def register_event():
	if request.method == 'GET':
		return render_template('yagra/login.html')
	else:
		username = request.form.get('username')
		password = request.form.get('password')
		
		db = MySQLdb.connect("localhost", "ubuntu", "lijia250", "test_db")
		cursor = db.cursor()
		sql = "SELECT * FROM user_db WHERE username='" + username + "';"
		cursor.execute(sql)
		results = cursor.fetchall()

		if len(results) == 0:
			sql = "INSERT INTO user_db(username, password) VALUES('" +\
				  username +\
				  "','" +\
				  str(getDigest(password)) +\
				  "');"
			cursor.execute(sql)
			db.commit()
			db.close()
			
			image_url = image_url_prefix + 'testBaidu.jpg'
			session['username'] = username
			return render_template("yagra/profile.html", 
								   image = image_url, 
								   tag = True, 
								   username = username,)
		else:
			return render_template("yagra/login.html", 
								   tip = '*该手机号码已被注册，请直接登录！')

@app.route('/upload_event', methods = ['GET', 'POST'])
def upload_event():
	if request.method == 'POST':
		f = request.files['image']
		username = session.get('username')
		file_type = os.path.splitext(f.filename)[-1]
		file_name = getDigest(username)
		#file_name = str(hashlib.md5(session.get('username')))
		path = '/home/ubuntu/sources/demo0/images/' + file_name + file_type
		f.save(path)
		
		db = MySQLdb.connect("localhost", "ubuntu", "lijia250", "test_db")
		cursor = db.cursor()
		sql = "UPDATE user_db SET profile_image='" +\
			  file_name + file_type +\
			  "' WHERE username='" +\
			  username +\
			  "';"
		cursor.execute(sql)
		db.commit()
		db.close()

		image_url = image_url_prefix + file_name + file_type
		return render_template('yagra/profile.html', 
							   image = image_url, 
							   tag = False, 
							   username = username)
	#应该不会执行到
	return render_template('yagra/login.html')
'''
'''
if __name__ == '__main__':
    app.run()
'''
