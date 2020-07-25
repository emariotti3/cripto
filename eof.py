import shutil, tempfile, os

PATH_OUT = "eof_out.png"
PATH_OUT3= "static\\" + PATH_OUT


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


# i = 65
# with open('outputfile.bin', 'wb') as f:
#     f.write(bytes([i]))
#     f.write('A'.encode('ascii'))
#     f.write(bytes('A', encoding='ascii'))


#     >>> import tempfile
# >>> f = tempfile.TemporaryFile()
# >>> f.write(b'Welcome to TutorialsPoint')
# >>> import os
# >>> f.seek(os.SEEK_SET)
# >>> f.read()
# b'Welcome to TutorialsPoint'
# >>> f.close()