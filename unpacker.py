#!/usr/env/bin python3
'''
https://github.com/hexpwn/sirius-cmdr-fw-unpacker

Unpacker for the Sirius XM Commander Touch radio
Ref:
https://www.siriusretail.com/SXVCT1/SXVCT1_update_v36.zip
https://shop.siriusxm.com/siriusxm-commander-touch.html

License: IDGAF
'''
import sys
import struct
import os
import shutil
from time import sleep

# Check arguments
if len(sys.argv) != 2:
    print("[ERROR] Please provide a filename for the image to be \
unpacked.\n./unpacker <filename.027>")
    exit(-1)
else:
    imagefile = sys.argv[1]

# Create filesystem structure
try:
    os.listdir("FWdump")
    shutil.rmtree("FWdump", True)
except FileNotFoundError:
    pass

os.mkdir("FWdump")
os.chdir("FWdump")


# Process the image
with open("../" + imagefile, 'rb') as image:
    rawimg = image.read()

    s_ = rawimg.split(b"/")
    imgname         = s_[0].decode('utf-8')
    contents        = s_[1]
    num_files       = struct.unpack("H", contents[3:5])[0]
    header_size    = struct.unpack("H", contents[1:3])[0]
    checksum        = contents[5:9].hex()
    start = header_size + 8
    print(f"Image name: {imgname}")
    print(f"Number of files: {num_files}")
    print(f"Checksum: {checksum}")
    print(f"Header size: {header_size}")
    print(f"Start offset: {start}")
    print('-'*80)

    for i in range(num_files):
        dir_flag    = False
        fn_size     = rawimg[start+2]
        fn_start    = start + 3 
        fn_end      = fn_start + fn_size
        filename = rawimg[fn_start:fn_end].decode('UTF-8')
        f_off   = struct.unpack("I", rawimg[fn_start + 34:fn_start + 38])[0]
        f_size  = struct.unpack("I", rawimg[fn_start + 38:fn_start + 42])[0]
        start += 44

        filename = filename.replace("\\","/")
        if f_size == 0xffffffff and f_off == 0xffffffff:
            dir_flag = True

        if dir_flag:
            print(f"Creating directory {filename}...")
            os.mkdir(filename)
            continue
        else:
            with open(filename, "wb") as outfile:
                print(f"Saving {filename}...")
                outfile.write(rawimg[f_off:f_off + f_size])

print("done")
exit(0)
