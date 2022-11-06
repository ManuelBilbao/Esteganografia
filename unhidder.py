from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def get_bit(readByte: int, n: int) -> int:
    return int((readByte & (1 << n)) / (1 << n))

def get_bits(readByte: int) -> list[int]:
    bits = []
    for i in range(8)[::-1]:
        bits += [get_bit(readByte, i)]

    return bits

def bits_to_int(bits: list[int]) -> int:
    return sum([bit << i for i, bit in enumerate(bits[::-1])])

def bits_to_char(bits: list[int]) -> str | None:
    if sum(bits) == 0:
        return None

    return chr(bits_to_int(bits))

def read_bit(pixel_color: int) -> None:
    return get_bits(pixel_color)[-1]

def unhidder():

    filename = askopenfilename()
    Tk().withdraw() 

    imageFile = Image.open(str(filename))
    imagePixels = imageFile.load()

    imageWidth, imageHeight = imageFile.size

    keepReading = True
    readByte = []
    message = ""

    for x in range(imageWidth):
        if not keepReading:
            break

        for y in range(imageHeight):
            if not keepReading:
                break

            if keepReading:
                readByte += [read_bit(imagePixels[x, y][0])]
                if len(readByte) == 8:
                    char = bits_to_char(readByte)

                    if char is None:
                        keepReading = False
                        continue

                    message += char
                    readByte = []

            if keepReading:
                readByte += [read_bit(imagePixels[x, y][1])]

                if len(readByte) == 8:
                    char = bits_to_char(readByte)

                    if char is None:
                        keepReading = False
                        continue

                    message += char
                    readByte = []

            if keepReading:
                readByte += [read_bit(imagePixels[x, y][2])]

                if len(readByte) == 8:
                    char = bits_to_char(readByte)

                    if char is None:
                        keepReading = False
                        continue

                    message += char
                    readByte = []
    print(message)


unhidder()