from PIL import Image

def decode_message_from_image(img: Image.Image) -> str:
    img = img.convert("RGB")
    width, height = img.size
    pixels = img.load()
    binary = ''
    chars = ''

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary += str(r & 1)

            if len(binary) >= 8:
                byte = binary[:8]
                binary = binary[8:]
                char = chr(int(byte, 2))
                chars += char

                if chars.endswith("<END>"):
                    return chars[:-5]

    return chars
