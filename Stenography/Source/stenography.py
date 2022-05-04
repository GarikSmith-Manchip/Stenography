#
#   Extraction and Hiding Image in Image
#
#   Author  Date            Description
#   GSM     Oct 07, 2021    Building hide funtionality
#

#   Includes
import numpy as np
from PIL import Image

#   Constants
MAXBITS   = 8
STOREBITS = 2
MAXCOLOUR = 256

def GetLSB ( value ):
    value = value << MAXBITS - STOREBITS
    value = value % MAXCOLOUR
    return value >> MAXBITS - STOREBITS

def RemoveLSB ( value ):
    value = value >> STOREBITS
    return value << STOREBITS

def GetMSB ( value ):
    return value >> MAXBITS - STOREBITS

def Shift ( value ):
    return value << MAXBITS - STOREBITS

#   Encrypt Image with Integer
def EncryptDecryptImage ( path, key ):
    #   Handle File Load
    file  = open ( path, "rb" )
    image = file.read ( )
    file.close

    #   Encrypt File
    output = bytearray ( image )
    for a, values in enumerate ( output ):
        output[a] = values ^ int ( key )

    #   Save Encrypted File
    file = open ( path, "wb" )
    file.write ( output )
    file.close ( )

def CreateNewImage ( data, size, mode ):
    image = Image.new ( "RGB", size )
    image.putdata ( data )

    if mode == "hide":
        path = "__hidden.bmp"
    elif mode == "extract":
        path = "__secret.bmp"

    image.save ( path )

    return path

#   Extract Image
def Extract ( hidden, key ):
    #   Decrypt File
    print ( "[+] Decrypting Image" )
    EncryptDecryptImage ( hidden, key )

    # Was File Decrypted
    try:
        hidden = Image.open ( hidden )
    except IOError:
        print ( "[-] Incorrect password" )
        exit ( )

    hiddenwidth  = hidden.size[0]
    hiddenheight = hidden.size[1]
    size         = hidden.size
    data         = []

    hidden = hidden.load ( )

    for height in range ( hiddenheight ):
        for width in range ( hiddenwidth ):
            #   Handle Hidden Image
            hidden_red   = hidden[width, height][0]
            hidden_green = hidden[width, height][1]
            hidden_blue  = hidden[width, height][2]

            hidden_red   = GetLSB ( hidden_red )
            hidden_green = GetLSB ( hidden_green )
            hidden_blue  = GetLSB ( hidden_blue )

            hidden_red   = Shift ( hidden_red )
            hidden_green = Shift ( hidden_green )
            hidden_blue  = Shift ( hidden_blue )

            #   Reveal Secret Image
            data.append ( ( hidden_red, hidden_green, hidden_blue ) )

    path = CreateNewImage ( data, size, "extract" )

#   Hide Image
def Hide ( cover, secret, key ):
    secretwidth  = secret.size[0]
    secretheight = secret.size[1]
    size         = secret.size
    data         = []

    cover  = cover.load ( )
    secret = secret.load ( )

    for height in range ( secretheight ):
        for width in range ( secretwidth ):
            #   Handle Secret Image
            secret_red   = secret[width, height][0]
            secret_green = secret[width, height][1]
            secret_blue  = secret[width, height][2]
            secret_red   = GetMSB ( secret_red )
            secret_green = GetMSB ( secret_green )
            secret_blue  = GetMSB ( secret_blue )

            #   Handle Cover Image
            cover_red   = cover[width, height][0]
            cover_green = cover[width, height][1]
            cover_blue  = cover[width, height][2]
            cover_red   = RemoveLSB ( cover_red )
            cover_green = RemoveLSB ( cover_green )
            cover_blue  = RemoveLSB ( cover_blue )

            #   Handle New Image
            data.append ( ( secret_red + cover_red, secret_green + cover_green, secret_blue + cover_blue ) )

    path = CreateNewImage ( data, size, "hide" )

    print ( "[+] Encrypting Image" )
    EncryptDecryptImage ( path, key )
