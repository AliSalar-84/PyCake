from PIL import Image

def encode_message_in_image(img: Image.Image, psypher: str) -> Image.Image:
    img = img.convert("RGB")

    message = psypher + "<END>"
    binary = ''.join(format(ord(c), '08b') for c in message)

    data_index = 0
    width, height = img.size
    pixels = img.load()

    for y in range(height):
        for x in range(width):
            if data_index >= len(binary):
                break
            r, g, b = pixels[x, y]
            r = (r & ~1) | int(binary[data_index])
            pixels[x, y] = (r, g, b)
            data_index += 1

    return img  # Modified image with embedded message

