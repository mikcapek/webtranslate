import os
from flask import Flask, redirect, flash, url_for, render_template, request
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename



app = Flask(__name__ , template_folder = './templates')
# babel = Babel(app)
mail = Mail(app)

app.secret_key = 'YourSuperSecreteKey'

UPLOAD_FOLDER = 'UPLOAD_FOLDER'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}

# add mail server config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'prekladyproskoly@gmail.com' 
app.config['MAIL_PASSWORD'] = 'dftifkrliunfzxqt'
app.config['MAIL_ASCII_ATTTACHMENTS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['BABEL_DEFAULT_LOCALE'] = 'en'




# @babel.localeselector
# def get_locale():
# 	return 'en'
    # if request.args.get('lang'):
    #     session['lang'] = request.args.get('lang')
    # return session.get('lang', 'en')

@app.route('/')
def home():
	return render_template('index.html', TRANSLATE_PRICE_STANDARD = 240, TRANSLATE_PRICE_EXPRESS = 280, CORRECT_PRICE_STANDARD = 100, CORRECT_PRICE_EXPRESS = 140, SUBTITLE_PRICE_STANDARD = 100, SUBTITLE_PRICE_EXPRESS= 140, TRANSCRIPT_PRICE_STANDARD= 50, TRANSCRIPT_PRICE_EXPRESS= 80  )

@app.route('/o-nas')
def onas():
	return render_template('o-nas.html')

@app.route('/sluzby')
def sluzby():
	return render_template('sluzby.html')

@app.route('/cenik')
def cenik():
	return render_template('cenik.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/contactform', methods = ['GET', 'POST'])
def contactform():
	

	if request.method == 'POST':


		user_name = str(request.form)
		
		sender_email = request.form['email']

		msg = Message("Message from your visitor" + user_name,
	                    sender=sender_email,
	                    recipients=['prekladyproskoly@gmail.com'])
		msg.body = (user_name)

		if "attachment" not in request.files:
			flash('No file part')
			return "where my file"
		file = request.files['attachment']
        # if user does not select file, browser also
        # submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as fp:
			msg.attach("image.png", "image/png", fp.read())




			# file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			# return redirect(url_for('uploaded_file',
			# 						filename=filename))
		
	
   


		# <sends messages>

		# msg.attach(app.config['UPLOAD_FOLDER'], filename)

	
		
		
		

		# <sends but only from directory>
		# with open(request.form['attachment'], 'rb') as f:
			# msg.attach("somefile", 'image/jpg', f.read())

		# if request.files:
		# 	attachment = request.files['attachment']

		# 	attachment.save(data)
		# 	msg.attach((attachment).read())
			
	

		mail.send(msg)

		# flash("zprava byla odeslana!")
		return redirect(request.url)
		

		
	return render_template('/contactform.html')

if __name__ == '__main__':
	app.run(debug=True)

