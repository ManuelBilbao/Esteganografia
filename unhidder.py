from aes import *
from PIL import Image
from utils import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def read_bit(pixel_color: int) -> None:
    return get_bits_from_byte(pixel_color)[-1]

def unhidder():

    filename = askopenfilename()
    Tk().withdraw() 

    imageFile = Image.open(str(filename))
    imagePixels = imageFile.load()

    keyPath = askopenfilename()

    key = upload_key(keyPath)

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

            redPixel = imagePixels[x, y][0]
            greenPixel = imagePixels[x, y][1]
            bluePixel = imagePixels[x, y][2]

            if keepReading:
                readByte += [read_bit(redPixel)]
                if len(readByte) == 8:
                    char = bits_to_char(readByte)

                    if char is None:
                        keepReading = False
                        continue

                    message += char
                    readByte = []

            if keepReading:
                readByte += [read_bit(greenPixel)]

                if len(readByte) == 8:
                    char = bits_to_char(readByte)

                    if char is None:
                        keepReading = False
                        continue

                    message += char
                    readByte = []

            if keepReading:
                readByte += [read_bit(bluePixel)]

                if len(readByte) == 8:
                    char = bits_to_char(readByte)

                    if char is None:
                        keepReading = False
                        continue

                    message += char
                    readByte = []

    print(decrypter(key, message))


if __name__ == "__main__":
    unhidder()
