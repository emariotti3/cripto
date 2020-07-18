# Imported PIL Library from PIL import Image
from PIL import Image

PATH_IN = "test.png"
PATH_OUT = "out.png"

# Open an Image
def open_image(path):
  newImage = Image.open(path)
  return newImage

# Save Image
def save_image(image, path):
  image.save(path, 'png')

# Create a new image with the given size
def create_image(i, j):
  image = Image.new("RGB", (i, j), "white")
  return image

# Get the pixel from the given image
def get_pixel(image, i, j):
    # Inside image bounds?
    width, height = image.size
    if i > width or j > height:
      return None

    # Get Pixel
    pixel = image.getpixel((i, j))
    return pixel

def convert_grayscale(src_img, dst_img, width, height):

  # Get output image pixel map
  pixels = dst_img.load()

  for i in range(width):
    for j in range(height):
      pixel = get_pixel(src_img, i, j)

      # Get R, G, B values (This are int from 0 to 255)
      red =   pixel[0]
      green = pixel[1]
      blue =  pixel[2]

      # Transform to grayscale
      # TODO: aca hacer la transformacion de pixeles para
      # meter el mensaje
      gray = (red * 0.299) + (green * 0.587) + (blue * 0.114)

      # Set Pixel in new image
      pixels[i, j] = (int(gray), int(gray), int(gray))

  # Return new image
  return dst_img


def embed_hidden_message():
  input_img = open_image(PATH_IN)
  width, height = input_img.size
  output_img = create_image(width, height)
  output_img = convert_grayscale(input_img, output_img, width, height)
  save_image(output_img, PATH_OUT)

embed_hidden_message()
