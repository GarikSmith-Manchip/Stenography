#
#   Processing Image for Stenography
#
#   Author  Date            Description
#   GSM     Oct 01, 2021    Design and research stenography libraries
#   GSM     Oct 07, 2021    Testing Numpy
#

#   Imports
import numpy as np
from PIL import Image
from stenography import Hide, Extract

#   Encrypt Image
def GetEncryptKey ( ):
    key = input ( "[o] Enter a password: " )
    print ( "[-] You entered: " + str ( key ) )
    return key


#   Hide Image
def ProcessCoverSecret ( cover, secret ):
    print ( "[+] Processing Images" )

    cover  = Image.open ( cover )
    secret = Image.open ( secret )
    key    = GetEncryptKey ( )

    Hide ( cover, secret, key )

def ProcessOutput ( hidden ):
    print ( "[+] Extracting Image" )

    key    = GetEncryptKey ( )
    Extract ( hidden, key )
