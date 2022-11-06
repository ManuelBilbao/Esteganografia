import os
from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pathlib

ASCII = 'ascii'

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

def hidder():
    textFilePath = askopenfilename()
    textFileSize = os.path.getsize(textFilePath)

    imageFilePath = askopenfilename()
    imageFileSize = os.path.getsize(imageFilePath)
    Tk().withdraw()

    if(textFileSize * 8 >= imageFileSize):
        print("El texto es demaciado grande para la imagen")
        exit()
    
    imageFile = Image.open(str(imageFilePath))
    textFile = open(str(textFilePath), encoding = ASCII).read()

    textFileBits = []
    imagePixels = imageFile.load()
    imageWidth, imageHeight = imageFile.size

    for b in bytes(textFile, ASCII):
        textFileBits += get_bits(b)
    textFileBits += [0, 0, 0, 0, 0, 0, 0, 0]

    writed = 0

    for x in range(imageWidth):
        if not keep_writing(writed, textFileBits):
            break

        for y in range(imageHeight):
            if not keep_writing(writed, textFileBits):
                break

            red = imagePixels[x, y][0]
            if keep_writing(writed, textFileBits):
                red = alter_last_bit(red, textFileBits[writed])
                writed += 1

            green = imagePixels[x, y][1]
            if keep_writing(writed, textFileBits):
                green = alter_last_bit(green, textFileBits[writed])
                writed += 1

            blue = imagePixels[x, y][2]
            if keep_writing(writed, textFileBits):
                blue = alter_last_bit(blue, textFileBits[writed])
                writed += 1

            imagePixels[x, y] = (red, green, blue)


    path = pathlib.PurePath(imageFilePath)
    imageFile.save(str(path.parents[0]) + '/modified_image.png')


hidder()