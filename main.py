from flask import Flask, render_template

app = Flask(__name__)

"""
HTTP Pages
"""
@app.route('/')
def home():
	return render_template('home.html')

@app.route('/chat/')
def chat():
	return render_template('chat.html')

@app.route('/login/')
def login():
	return render_template('login.html')

@app.route('/register/')
def register():
	return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
