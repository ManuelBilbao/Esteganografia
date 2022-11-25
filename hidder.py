import os
from utils import *
from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import time
from aes import *

ASCII = 'ascii'

def alter_last_bit(original: int, replace_bit: int) -> int:
    pixel_color = get_bits_from_byte(original)
    pixel_color[-1] = replace_bit
    return bits_to_int(pixel_color)

def hidder():
    print("Seleccione el texto")
    textFilePath = askopenfilename()
    textFileSize = os.path.getsize(textFilePath)
    
    print("Seleccione la imagen")
    imageFilePath = askopenfilename()
    Tk().withdraw()

    imageFile = Image.open(str(imageFilePath))
    imageWidth, imageHeight = imageFile.size 

    key = generate_key()

    if(textFileSize >= imageWidth * imageHeight * 3 / 8):
        print("El texto es demasiado grande para la imagen")
        exit()


    textFile = open(str(textFilePath), encoding = ASCII).read()
    print('Encriptando mensaje y generando key...')
    encryptedTextFile = encrypter(key, textFile)
    print('Mensaje encriptado!')
    time.sleep(1)
    print("Ocultando el mensaje...")

    textFileBits = []
    imagePixels = imageFile.load()

    for b in bytes(encryptedTextFile.decode(), ASCII):
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

            try:
                imagePixels[x, y] = (
                    redPixel, greenPixel, bluePixel, imagePixels[x, y][3]
                )
            except Exception:
                imagePixels[x, y] = (redPixel, greenPixel, bluePixel)

    imageFile.save('./modified_image.' + imageFilePath.split(".")[-1])
   
    print("El mensaje se ha ocultado correctamente!")

if __name__ == "__main__":
    hidder()
