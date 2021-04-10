from flask import Flask, request, render_template
import MySQLdb
import json

app = Flask(__name__)
app.debug = True

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
		sql = "SELECT * FROM test_table WHERE name='" + username + "' AND password='" + password + "';"
		cursor.execute(sql)
		results = cursor.fetchall()
		db.close()
		return "got " + str(len(results)) + " results."

@app.route('/register_event', methods = ['GET', 'POST'])
def register_event():
	if request.method == 'GET':
		return render_template('yagra/login.html')
	else:
		username = request.form.get('username')
		password = request.form.get('password')
		
		db = MySQLdb.connect("localhost", "ubuntu", "lijia250", "test_db")
		cursor = db.cursor()
		sql = "SELECT * FROM test_table WHERE name='" + username + "';"
		cursor.execute(sql)
		results = cursor.fetchall()
		
		if len(results) == 0:
			sql = "INSERT INTO test_table VALUES('" + username + "','" + str(hash(password)) + "');"
			print(sql)
			cursor.execute(sql)
			db.commit()
			
			db.close()
			return render_template("yagra/login.html")
		else:
			return render_template("yagra/login.html", existed = True)

if __name__ == '__main__':
    app.run()
