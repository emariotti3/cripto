# Imported PIL Library from PIL import Image
from PIL import Image
#import numpy as np

PATH_IN = "test.png"
PATH_OUT = "out.png"


def reemplazar_ultimo_bit(original_value, new_last_bit):
  cantidad_bits = len(new_last_bit)
  original_byte = bin(original_value)
  return original_byte[:-cantidad_bits] + new_last_bit

def ocultar(src_img, mensaje_bits, cant_bits=1):
  estego_img = Image.new("RGB", src_img.size, "white")
  pixeles = estego_img.load()
  width, height = src_img.size

  for i in range(width):
    for j in range(height):
      red,green,blue,_ = src_img.getpixel((i, j))[:]
      nro_pixel = i + j % width
      primer_bit = nro_pixel*3
      ultimo_bit = primer_bit + 3
      if (ultimo_bit >= len(mensaje_bits)):
        break
      a,b,c = mensaje_bits[primer_bit:ultimo_bit]
      #print("OCULTAR a,b,c={}".format(str(mensaje_bits[nro_pixel*3:nro_pixel*3+3])))
      pixeles[i, j] = (int(reemplazar_ultimo_bit(red, a),2), int(reemplazar_ultimo_bit(green, b),2), int(reemplazar_ultimo_bit(blue, c),2),_)
  return estego_img

def recuperar_mensaje(estego_img, cant_bits=1):
  width, height = estego_img.size
  mensaje = []
  substr = ""
  count = 0
  for i in range(width):
    for j in range(height):
      r,g,b = estego_img.getpixel((i, j))[:]
      if (count > 56):
        break
      print("r,g,b = {} {} {}".format(r,g,b))
      print("bin r,g,b = {} {} {}".format(bin(r),bin(g),bin(b)))
      print("last bin r,g,b = {} {} {}".format(str(bin(r))[-1],str(bin(g))[-1],str(bin(b))[-1]))
      print("mensaje = {}".format(mensaje))
      count+=3

      substr += str(bin(r))[-1] + str(bin(g))[-1] + str(bin(b))[-1]
      if (len(substr) >= 8):
        chunk = substr[0:8]
        print("substr {} chunk {}".format(substr, chunk))

        substr = substr[8:]
        mensaje.append(chunk)
  # return str(''.join(format(ord(x), 'c') for x in mensaje))
  #mensaje = str(''.join(binario_a_ascii(x) for x in mensaje))
  print("BIN -> ASCII {}".format(mensaje))
  letters = [binario_a_ascii(letter) for letter in mensaje]
  return "".join(letters)


def binario_a_ascii(textoBinario):
  binary_int = int(textoBinario, 2)
  byte_number = binary_int.bit_length() + 7 // 8

  binary_array = binary_int.to_bytes(byte_number, "little")
  ascii_text = binary_array.decode('ascii')
  #print("BINARIO A ASCII {}".format(ascii_text))

  return ascii_text

def ascii_a_binario(textoPlano):
  byte_array = textoPlano.encode('ascii')

  binary_int = int.from_bytes(byte_array, "little")
  binary_string = bin(binary_int).replace("0b","")
  print("ASCII A BINARIO {}".format(binary_string))
  while len(binary_string) < 8:
    binary_string = '0'+binary_string
  return binary_string

def embed_hidden_message():
  ##FALATA LOS CHEQUEOS DE LARGOS HAY QUE AALIZAR QUE PASA SI ES MAS CORTO O SI SE 
  ##PUEDE PARAMETRIZAR LA CANTIDAD DE BITS QUE SE AGREGAN SI ES MAS LARGO
  mensaje_oculto = "UN MENSAJE OCULTO" * 30000 #* 2  
  #print(''.join(format(ord(x), 'b') for x in mensaje_oculto))
  input_img = Image.open(PATH_IN)
  print(input_img.size)
  output_img = ocultar(input_img, ''.join(ascii_a_binario(x) for x in mensaje_oculto))
  input_img.close()
  output_img.save(PATH_OUT)
  encoded_img = Image.open(PATH_OUT)

  print(recuperar_mensaje(encoded_img))

embed_hidden_message()
