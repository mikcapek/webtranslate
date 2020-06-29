from flask import Flask, redirect, url_for, render_template, request
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message

app = Flask(__name__ , template_folder = './templates')

app.secret_key = 'YourSuperSecreteKey'

# add mail server config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'prekladyproskoly@gmail.com' 
app.config['MAIL_PASSWORD'] = 'dftifkrliunfzxqt'
app.config['MAIL_ASCII_ATTTACHMENTS'] = False

mail = Mail(app)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/o-nas')
def onas():
	return render_template('o-nas.html')

@app.route('/contactform', methods = ['GET', 'POST'])
def contactform():

	if request.method == 'POST':
		user_name = str(request.form)
		

		msg = Message("Message from your visitor" + user_name,
	                    sender='YourUser@NameHere',
	                    recipients=['prekladyproskoly@gmail.com'])
		msg.body = (user_name)
		
		with open(request.form['attachment'], 'rb') as f:
			msg.attach("somefile", 'image/jpg', f.read())

		# if request.files:
		# 	attachment = request.files['attachment']

		# 	attachment.save(data)
		# 	msg.attach((attachment).read())
			
	

		mail.send(msg)
		return "Successfully  sent message!"
		
	return render_template('contactform.html')

if __name__ == '__main__':
	app.run(debug=True)

