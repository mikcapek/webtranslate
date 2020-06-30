import os
from flask import Flask, redirect, flash, url_for, render_template, request
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename


app = Flask(__name__ , template_folder = './templates')

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

mail = Mail(app)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/o-nas')
def onas():
	return render_template('o-nas.html')



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

		flash("zpráva byla odeslána!")
		return redirect(request.url)
		

		
	return render_template('/contactform.html')

if __name__ == '__main__':
	app.run(debug=True)

