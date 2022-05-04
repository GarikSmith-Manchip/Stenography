#
#   Main Stenography - Image to Image
#
#   Author  Date            Description
#   GSM     Oct 07, 2021    Setting up Arguments from design
#

#   Includes
from argparse   import ArgumentParser
from processing import ProcessCoverSecret, ProcessOutput


#   Set Arguments
parser = ArgumentParser ( )
parser.add_argument ( "-c", "--cover",   dest = "cover",     help = "Cover Image" )
parser.add_argument ( "-s", "--secret",  dest = "secret",    help = "Secret Image" )
parser.add_argument ( "-o", "--output",  dest = "output",    help = "Output File" )
parser.add_argument ( "-f", "--file",    dest = "hidden",    help = "Hidden Image File" )
parser.add_argument ( "-m", "--mode",    dest = "mode",      help = "Mode: extract or hide" )
args = parser.parse_args ( )

#   Mode Handling
if args.mode == "hide":
    print ( "[+] Hide Mode" )
    if args.cover is None:
        print ( "[-] Cover image needed" )
        exit ( )

    if args.secret is None:
        print ( "[-] Secret image needed" )
        exit ( )

    ProcessCoverSecret ( args.cover, args.secret )
elif args.mode == "extract":
    print ( "[+] Extraction Mode" )
    if args.hidden is None:
        print ( "[-] Hidden image needed" )
        exit ( )
    ProcessOutput ( args.hidden )
else:
    print ( "[-] Invalid mode selected" )
    exit ( )
