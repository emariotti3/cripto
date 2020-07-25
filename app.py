# -*- coding: ascii -*-

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os, re
import lsb as lsb
import eof as eof

FILE_PATH = os.path.abspath(os.path.dirname(__file__))
EOF_FOLDER = 'EOF'
LSB_FOLDER = 'LSB'
ALLOWED_EXTENSIONS = {'png', 'jpg'}
PIXELES_DISPLAYED = 15
SYS_IMG = 'IMG_PAGE'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'
app.secret_key = os.urandom(24)

def get_full_path(filename):
    return os.path.join(FILE_PATH, app.config['UPLOAD_FOLDER'], filename)

def get_path(filename):
    return os.path.join(app.config['UPLOAD_FOLDER'], filename)

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
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        if not f == SYS_IMG:
            os.remove(get_path(f))
    return render_template("index.html")


@app.route('/eof_demo', methods=['GET'])
def render_eof():
    return render_template("eof.html")

@app.route('/eof_result', methods=['GET', 'POST'])
def eof_result():
    message_to_hidde = request.form['message_to_hidde']
    filename = uploaded(request)
    path_in = get_full_path(filename)
    path_out = get_full_path(eof.PATH_OUT)
    eof.append_hidden_message(path_in, message_to_hidde, path_out)
    orginal_binary = eof.get_img_binary(path_in)
    stegoimage_binary = eof.get_img_binary(path_out)
    return render_template("eof_result.html", src_img=get_path(filename), stego_img=get_path(eof.PATH_OUT), original_binary=orginal_binary, stegoimage_binary=stegoimage_binary)

@app.route('/lsb_demo', methods=['GET'])
def render_lsb():
    return render_template("lsb.html")

@app.route('/lsb_result', methods=['POST'])
def lsb_result():
    message_to_hidde = request.form['message_to_hidde']
    filename = uploaded(request)
    path_in = get_full_path(filename)
    path_out = get_full_path(lsb.PATH_OUT)
    message_hidden = lsb.embed_hidden_message(path_in, message_to_hidde, path_out)
    original_pixel_rgb = lsb.get_bytes_for_pixels(path_in)[:PIXELES_DISPLAYED]
    stego_pixel_rgb =  lsb.get_bytes_for_pixels(get_path(lsb.PATH_OUT))[:PIXELES_DISPLAYED]
    joined_bytes = "".join([byte for pixel in stego_pixel_rgb for byte in pixel] )
    bytes_message = lsb.get_bytes(message_to_hidde)
    return render_template("lsb_result.html", message_hidden=message_hidden, src_img=get_path(filename), stego_img=get_path(lsb.PATH_OUT), pixeles_originales= original_pixel_rgb, pixeles_modificados=stego_pixel_rgb, bytes_message=bytes_message, bits=joined_bytes)

if __name__ == '__main__':
   app.run(debug=True) 
