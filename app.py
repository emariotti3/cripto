# -*- coding: ascii -*-

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import lsb as ss

BASEDIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(24)

@app.route('/')
def index():
   return render_template("index.html")

@app.route('/messageToHidde', methods=['POST'])
def messageToHidde():
    if request.method == "POST":
        MENSAJE = ss.embed_hidden_message2()
        return render_template("lsb.html", comment=MENSAJE)#request.form["text_input"])
    return render_template("lsb.html")

@app.route('/text', methods=['GET', 'POST'])
def text(comments=[]):
    if request.method == "GET":
        return render_template("lsb.html", comments=comments)    
    comments.append(request.form["text_input"])  
    return redirect(url_for('text'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/lsb_endpoint', methods=['GET', 'POST'])
def lsb_endpoint():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(BASEDIR, app.config['UPLOAD_FOLDER'], filename))
            return redirect(request.url)
    return render_template("lsb.html")

def uploaded(request):
    filename = ''
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(BASEDIR, app.config['UPLOAD_FOLDER'], filename))
    return filename

@app.route('/encodearBIENPERRO', methods=['POST'])
def encodearBIENPERRO():
    userEmail = request.form['message_to_hidde']
    filename = uploaded(request)
    message_hidden = ss.embed_hidden_message(os.path.join(BASEDIR, app.config['UPLOAD_FOLDER'], filename), userEmail )
    image_file = url_for('static', filename=filename)
    return render_template("lsb.html", message_hidden=message_hidden, src_img=image_file, stego_img=ss.PATH_OUT3 )

if __name__ == '__main__':
   app.run(debug=True)