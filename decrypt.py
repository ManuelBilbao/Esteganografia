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


def bits_to_char(bits: list[int]) -> str | None:
    if sum(bits) == 0:
        return None

    return chr(bits_to_int(bits))


def read_bit(pixel_color: int) -> None:
    return get_bits(pixel_color)[-1]


image = Image.open(input("Ruta: "))
pixels = image.load()

width, height = image.size

keep_reading = True
byte = []
message = ""

for x in range(width):
    if not keep_reading:
        break

    for y in range(height):
        if not keep_reading:
            break

        if keep_reading:
            byte += [read_bit(pixels[x, y][0])]
            if len(byte) == 8:
                char = bits_to_char(byte)

                if char is None:
                    keep_reading = False
                    continue

                message += char
                byte = []

        if keep_reading:
            byte += [read_bit(pixels[x, y][1])]

            if len(byte) == 8:
                char = bits_to_char(byte)

                if char is None:
                    keep_reading = False
                    continue

                message += char
                byte = []

        if keep_reading:
            byte += [read_bit(pixels[x, y][2])]

            if len(byte) == 8:
                char = bits_to_char(byte)

                if char is None:
                    keep_reading = False
                    continue

                message += char
                byte = []

print(message)
