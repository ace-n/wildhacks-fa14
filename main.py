from flask import Flask, render_template, request, redirect, session
from models import User
from urlparse import urlparse
import re

app = Flask(__name__)
app.secret_key ="erhwcnI0979UB&U(#RBuijb6753787iyO*Y@#GBIUdnIO@65rfiguyhc6476uiHODUWCBc:}{6854765678697;]p[l[pJKPIkhbvut756us5i7bHD{W=_W(D)}]]}"

"""
HTTP Pages
"""
@app.route('/', methods=['GET'])
def home():
	return render_template('home.html', data={})

@app.route('/chat/', methods=['GET'])
def chat():

	# Require login
	if 'username' not in session:
		return redirect('/login/')

	return render_template('chat.html', data={})

@app.route('/login/', methods=['GET'])
def login():
	return render_template('login.html', data={})

# Helper function
def verifyLength(name, value, minLength, maxLength):

	errors = []
	if len(value) < minLength:
		errors.append("%s must be > %s characters long." % (name, minLength))
	if len(value) > maxLength:
		errors.append("%s must be <= %s characters long." % (name, maxLength))

	return errors

@app.route('/logout/', methods=['GET'])
def logout():

	# Require login
	if 'username' not in session:
		return redirect('/login/')

	session.pop('username', None)
	return redirect('/')

@app.route('/login/', methods=['POST'])
def login_post():

	# Get POST data
	userName = request.form.get("username", '')
	pw = request.form.get("password", '')

	print userName
	print "[%s]" % pw

	# Verify password
	errors = verifyLength("Passwords", pw, 5, 64)

	# Verify username
	errors.extend(verifyLength("Usernames", userName, 5, 64))
	if not re.search(r"^\w+$", userName):
		errors.append("Usernames can only contain letters and numbers.")

	# Bug out if errors
	if len(errors) == 0:

		# Get user
		userCount = User.select().where(User.password == pw, User.username == userName).count()

		# Redirect depending on validity
		if userCount == 1:

			# User logged in successfully
			session['username'] = userName
			return redirect("/chat/")
		else:
			errors.append("Invalid login.")

	# Done!
	return render_template('login.html', data={"errors": errors, "userName": userName})

@app.route('/register/', methods=['GET'])
def register():
	return render_template('register.html', data={})

@app.route('/register/', methods=['POST'])
def register_post():

	# Get POST data
	userName = request.form["username"]
	pw = request.form["password"]
	imageUrl = request.form["imageUrl"]

	# Verify password
	errors = verifyLength("Passwords", pw, 5, 64)

	# Verify image URL
	errors.extend(verifyLength("Avatar URL", imageUrl, 10, 256))
	if not urlparse(imageUrl):
		errors.append("Invalid Avatar URL.")

	# Verify username
	errors.extend(verifyLength("Usernames", userName, 5, 64))
	if not re.search(r"^\w+$", userName):
		errors.append("Usernames can only contain letters and numbers.")
	if len(errors) == 0:

		# Check if username is already taken
		userObj = None
		errors = []
		
		try:
			User.get(User.username == userName).count()

			# Username is taken - so append an error
			errors.append("That username is already taken.")

		except:
			pass

	# Bug out if errors
	if len(errors):
		return render_template('register.html', data={"errors": errors, "userName": userName, "imageUrl": imageUrl})

	# Create user instance
	userObj = User(username=userName, password=pw, imageUrl=imageUrl)
	userObj.save()

	# Redirect
	login_user(userObj)
	return redirect("/chat")

@app.route('/profile', methods=['GET'])
def profile():

	# Require login
	if 'username' not in session:
		return redirect('/login/')

	user = User.get(User.username == session['username'])

	return render_template('profile.html', data={"imageUrl": user.imageUrl, "userName": user.username})

@app.route('/profile', methods=['POST'])
def profile_post():

	# Get POST data
	userName = request.form["username"]
	curPw = request.form["curPassword"]
	newPw = request.form["newPassword"]
	imageUrl = request.form["imageUrl"]

	# Verify passwords
	errors = verifyLength("Current Password", curPw, 5, 64)
	if len(newPw) != 0:
		errors = verifyLength("New Password", newPw, 5, 64)

	# Verify image URL
	errors.extend(verifyLength("Avatar URL", imageUrl, 10, 256))
	if not urlparse(imageUrl):
		errors.append("Invalid Avatar URL.")

	# Verify username
	errors.extend(verifyLength("Username", userName, 5, 64))
	if not re.search(r"^\w+$", userName):
		errors.append("Usernames can only contain letters and numbers.")
	if len(errors) == 0:

		# Check if username is already taken
		userObj = None
		errors = []
		
		try:
			User.get(User.username == userName).count()

			# Username is taken - so append an error
			errors.append("That username is already taken.")

		except:
			pass

	# Bug out if errors (exit 1 of 2)
	if len(errors):
		return render_template('profile.html', data={"errors": errors, "userName": userName, "imageUrl": imageUrl})

	# Get user instance
	userObj = User.get(User.username == session['username'])
	if userObj.password != curPw:
		return render_template('profile.html', data={"errors": ["Please re-enter your current password."], "userName": userName, "imageUrl": imageUrl})

	# Update user instance
	if len(newPw) != 0:
		 userObj.password = newPw
	userObj.username = userName
	session['username'] = userName
	userObj.imageUrl = imageUrl
	userObj.save()

	# Redirect
	return redirect("/profile")

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
