import shutil, tempfile, os

PATH_OUT = "eof_out.png"

def append_hidden_message(path_in, message_to_hidde, path_out):
    shutil.copy2(path_in, path_out)
    tmp_file = tempfile.TemporaryFile()
    tmp_file.write(message_to_hidde.encode('ascii'))
    tmp_file.seek(0)
    with open(path_out, "ab") as myfile:
        myfile.write(tmp_file.read())
    tmp_file.close()


def get_img_binary(src_image):
    with open(src_image, "rb") as myfile:
        return myfile.read()
