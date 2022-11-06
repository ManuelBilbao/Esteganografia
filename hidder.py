import os
from utils import *
from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pathlib

ASCII = 'ascii'

def alter_last_bit(original: int, replace_bit: int) -> int:
    pixel_color = get_bits_from_byte(original)
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

    print("Ocultando el mensaje...")
    
    imageFile = Image.open(str(imageFilePath))
    textFile = open(str(textFilePath), encoding = ASCII).read()

    textFileBits = []
    imagePixels = imageFile.load()
    imageWidth, imageHeight = imageFile.size

    for b in bytes(textFile, ASCII):
        textFileBits += get_bits_from_byte(b)
    textFileBits += [0, 0, 0, 0, 0, 0, 0, 0]

    writed = 0

    for x in range(imageWidth):
        if not keep_writing(writed, textFileBits):
            break

        for y in range(imageHeight):
            if not keep_writing(writed, textFileBits):
                break

            redPixel = imagePixels[x, y][0]
            if keep_writing(writed, textFileBits):
                redPixel = alter_last_bit(redPixel, textFileBits[writed])
                writed += 1

            greenPixel = imagePixels[x, y][1]
            if keep_writing(writed, textFileBits):
                greenPixel = alter_last_bit(greenPixel, textFileBits[writed])
                writed += 1

            bluePixel = imagePixels[x, y][2]
            if keep_writing(writed, textFileBits):
                bluePixel = alter_last_bit(bluePixel, textFileBits[writed])
                writed += 1

            imagePixels[x, y] = (redPixel, greenPixel, bluePixel)


    path = pathlib.PurePath(imageFilePath)
    imageFile.save(str(path.parents[0]) + '/modified_image.png')
    print("El mensaje se ha ocultado correctamente!")


hidder()