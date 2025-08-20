from PIL import Image

def decode_message_from_image(img: Image.Image) -> str:
    img = img.convert("RGB")
    width, height = img.size
    pixels = img.load()
    binary = ''
    byte_list = []

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary += str(r & 1)

            while len(binary) >= 8:
                byte = binary[:8]
                binary = binary[8:]
                byte_list.append(int(byte, 2))

    message_bytes = bytes(byte_list)
    message = message_bytes.decode("utf-8", errors="ignore")

    if "<END>" in message:
        return message.split("<END>")[0]
    return message