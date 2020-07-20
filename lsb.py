# Imported PIL Library from PIL import Image
from PIL import Image
import numpy as np

PATH_IN = "test.png"
PATH_OUT = "out.png"

STR ='0b10101011001110100000100110110001011001110101001110000011001010100010110000010011111000011101010110011001010100100111110101011001110100000100110110001011001110101001110000011001010100010110000010011111000011101010110011001010100100111110101011001110100000100110110001011001110101001110000011001010100010110000010011111000011101010110011001010100100111110101011001110100000100110110001011001110101001110000011001010100010110000010011111000011101010110011001010100100111110101011001110100000100110110001011001110101001110000011001010100010110000010011111000011101010110011001010100100111110101011001110100000100110110001011001110101001110000011001010100010110000010011100'

# print("".join([str(x) for x in STR]))
# A = [','.join(format(i, 'd') for i in bytearray(STR, encoding ='utf-8'))] 
# print("allaalalalal",A, mystring )

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
      a,b,c = mensaje_bits[nro_pixel*3:nro_pixel*3+3]
      pixeles[i, j] = (int(reemplazar_ultimo_bit(red, a),2), int(reemplazar_ultimo_bit(green, b),2), int(reemplazar_ultimo_bit(blue, c),2),_)
  return estego_img

def recuperar_mensaje(estego_img, cant_bits=1):
  width, height = estego_img.size
  mensaje = "0b"
  for i in range(width):
    for j in range(height):
      r,g,b = estego_img.getpixel((i, j))[:]
      mensaje += str(bin(r)[-cant_bits:])+str(bin(g)[-cant_bits:])+str(bin(b)[-cant_bits:])
  # return str(''.join(format(ord(x), 'c') for x in mensaje))
  return mensaje


def embed_hidden_message():
  ##FALATA LOS CHEQUEOS DE LARGOS HAY QUE AALIZAR QUE PASA SI ES MAS CORTO O SI SE 
  ##PUEDE PARAMETRIZAR LA CANTIDAD DE BITS QUE SE AGREGAN SI ES MAS LARGO
  mensaje_oculto = "UN MENSAJE OCULTO" #* 300000 * 2  
  print(''.join(format(ord(x), 'b') for x in mensaje_oculto))
  input_img = Image.open(PATH_IN)
  print(input_img.size)
  output_img = ocultar(input_img, ''.join(format(ord(x), 'b') for x in mensaje_oculto))
  output_img.save(PATH_OUT)
  print(recuperar_mensaje(output_img))

embed_hidden_message()
