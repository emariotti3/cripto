from PIL import Image

PATH_OUT = "lsb_out.png"
BITS_FOR_PIXEL = 3
NULL = '00000000'

def ascii_a_binario(textoPlano):
  byte_array = textoPlano.encode('ascii')
  binary_int = int.from_bytes(byte_array, "little")
  binary_string = bin(binary_int).replace("0b","")
  while len(binary_string) < 8:
    binary_string = '0'+binary_string
  return binary_string

def binario_a_ascii(textoBinario):
  binary_int = int(textoBinario, 2)
  binary_array = binary_int.to_bytes(1, "little")
  return binary_array.decode('ascii')

def get_string_of_bits(messege):
  return ''.join(ascii_a_binario(chararcter) for chararcter in messege)

def get_chunk_of_bit_por_pixel(m, pixel_number):
  '''Retorna los bits de la cadena/string correspientes a un pixel en base al numero de pixel
  Si se esta fuera de rango se completan o devuelven ceros'''
  index_first_bit = pixel_number * BITS_FOR_PIXEL
  index_last_bit = index_first_bit + BITS_FOR_PIXEL
  message_size = len(m)
  if index_last_bit <= message_size:
    return m[index_first_bit:index_last_bit]
  if index_first_bit > message_size:
    return '0' * BITS_FOR_PIXEL
  finals_bit = BITS_FOR_PIXEL - len(m[index_first_bit:])
  return m[index_first_bit:] + '0' * finals_bit

def replace_last_bits(original_value, last_bits):
  number_of_bits = len(last_bits)
  original_byte = bin(original_value)
  return int(original_byte[:-number_of_bits] + last_bits, 2)

def generate_stegoimage(src_img, messege_to_hide, cant_bits=1):
  estego_img = Image.new("RGB", src_img.size, "white")
  pixeles = estego_img.load()
  width, height = src_img.size
  bits_to_hide = get_string_of_bits(messege_to_hide)
  for i in range(width):
    for j in range(height):
      red,green,blue, *_ = src_img.getpixel((i, j))[:]
      pixel_number = i * height + j
      last_bit_red, last_bit_green, last_bit_blue= get_chunk_of_bit_por_pixel(bits_to_hide, pixel_number)
      pixeles[i, j] = (replace_last_bits(red, last_bit_red), replace_last_bits(green, last_bit_green), replace_last_bits(blue, last_bit_blue))
  return estego_img

def recovered_message(estego_img, cant_bits=1):
  width, height = estego_img.size
  mensaje = []
  substr = ""
  for i in range(width):
    for j in range(height):
      r,g,b = estego_img.getpixel((i, j))[:]
      substr += str(bin(r))[-1] + str(bin(g))[-1] + str(bin(b))[-1]
      if (len(substr) >= 8):
        chunk = substr[0:8]
        substr = substr[8:]
        mensaje.append(chunk)
  letters = [ binario_a_ascii(letter) for letter in mensaje if letter != NULL]
  return "".join(letters)

def get_message_of_lsb(src_img):
  stego_image = Image.open(src_img)
  message_hidden = recovered_message(stego_image)
  stego_image.close()
  return message_hidden

def formated_byte(binary):
  return (NULL + binary.replace("0b",""))[-8:]

def get_bytes_for_pixels(src_img):
  input_img = Image.open(src_img)
  width, height = input_img.size
  bytesarr = []
  for i in range(width):
    for j in range(height):
      red,green,blue, *_ = input_img.getpixel((i, j))[:]
      bytesarr.append([formated_byte(str(bin(red))), formated_byte(str(bin(green))), formated_byte(str(bin(blue)))])
  input_img.close()
  return bytesarr[:40]

def get_bytes(messege):
  return [[formated_byte(format(ord(character), 'b')) , character] for character in messege]

def embed_hidden_message(path_in, message_to_hidde, path_out):
  input_img = Image.open(path_in)
  output_img = generate_stegoimage(input_img, message_to_hidde) 
  output_img.save(path_out)
  input_img.close()
  stego_image = Image.open(path_out)
  message_hidden = recovered_message(stego_image)
  stego_image.close()
  return message_hidden


