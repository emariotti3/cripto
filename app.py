# -*- coding: ascii -*-

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import lsb as lsb
import eof as eof

FILE_PATH = os.path.abspath(os.path.dirname(__file__))
EOF_FOLDER = 'EOF'
LSB_FOLDER = 'LSB'
ALLOWED_EXTENSIONS = {'png', 'jpg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'
app.secret_key = os.urandom(24)

def get_path(filename):
    return os.path.join(FILE_PATH, app.config['UPLOAD_FOLDER'], filename)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def uploaded(request):
    filename = ''
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(FILE_PATH, app.config['UPLOAD_FOLDER'], filename))
    return filename


@app.route('/', methods=['GET'])
def index():
   return render_template("index.html")

@app.route('/eof_demo', methods=['GET', 'POST'])
def render_eof():
    return render_template("eof.html")

@app.route('/eof_result', methods=['GET', 'POST'])
def eof_result():
    message_to_hidde = request.form['message_to_hidde']
    filename = uploaded(request)

    path_in = get_path(filename)
    path_out = get_path(eof.PATH_OUT)
    eof.append_hidden_message(path_in, message_to_hidde, path_out)
    
    image_file = url_for('static', filename=filename)
    orginal_binary = eof.get_img_binary(path_in)
    stegoimage_binary = eof.get_img_binary(path_out)
    return render_template("eof_result.html",  src_img=image_file, stego_img=eof.PATH_OUT3,original_binary=orginal_binary, stegoimage_binary=stegoimage_binary)

@app.route('/lsb_demo', methods=['GET', 'POST'])
def render_lsb():
    return render_template("lsb.html")

@app.route('/lsb_result', methods=['POST'])
def lsb_result():
    userEmail = request.form['message_to_hidde']
    filename = uploaded(request)
    message_hidden = lsb.embed_hidden_message(os.path.join(FILE_PATH, app.config['UPLOAD_FOLDER'], filename), userEmail )
    image_file = url_for('static', filename=filename)

    original = lsb.get_bytes_for_pixels(os.path.join(FILE_PATH, app.config['UPLOAD_FOLDER'], filename))[:15]
    modificados =  lsb.get_bytes_for_pixels(lsb.PATH_OUT3)
    seq = "".join([j for i in modificados for j in i] )
    mb = lsb.cadena(userEmail)
    
    return render_template("lsb_result.html", message_hidden=message_hidden, src_img=image_file, stego_img=lsb.PATH_OUT3, pixeles_originales= original, pixeles_modificados=modificados[:15], mensaje_bytes=mb, seq=seq)


if __name__ == '__main__':
   app.run(debug=True)