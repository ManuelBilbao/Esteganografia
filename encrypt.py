from PIL import Image


def get_bit(byte: int, n: int) -> int:
    return int((byte & (1 << n)) / (1 << n))


def get_bits(byte: int) -> list[int]:
    bits = []
    for i in range(8)[::-1]:
        bits += [get_bit(byte, i)]

    return bits


def bits_to_int(bits: list[int]) -> int:
    return sum([bit << i for i, bit in enumerate(bits[::-1])])


def keep_writing(writed: int, bits: list[int]) -> bool:
    return writed < len(bits)


def alter_last_bit(original: int, replace_bit: int) -> int:
    pixel_color = get_bits(original)
    pixel_color[-1] = replace_bit
    return bits_to_int(pixel_color)


text = open(input("Text: "), encoding = "ascii").read()
bits = []
for b in bytes(text, "ascii"):
    bits += get_bits(b)
bits += [0, 0, 0, 0, 0, 0, 0, 0]

image = Image.open(input("Ruta: "))
pixels = image.load()

width, height = image.size
if (len(bits) >= width*height*3):
    print("No entra")
    exit()

writed = 0

for x in range(width):
    if not keep_writing(writed, bits):
        break

    for y in range(height):
        if not keep_writing(writed, bits):
            break

        red = pixels[x, y][0]
        if keep_writing(writed, bits):
            red = alter_last_bit(red, bits[writed])
            writed += 1

        green = pixels[x, y][1]
        if keep_writing(writed, bits):
            green = alter_last_bit(green, bits[writed])
            writed += 1

        blue = pixels[x, y][2]
        if keep_writing(writed, bits):
            blue = alter_last_bit(blue, bits[writed])
            writed += 1

        pixels[x, y] = (red, green, blue)

image.save("/home/manu/Documentos/Facultad/Cripto/TP/imagen.png")
