import numpy as np
import pickle
import os
import cv2
import sys
import main


def Decode_interval(tag, pixels_freq):
    output_codes = []
    while True:
        for code, (start, width) in pixels_freq.items():
            if 0 <= (tag - start) < width:
                tag = (tag - start) / width
                output_codes.append(code)
                if len(output_codes) == main.Block_size:
                    return output_codes
                break


def loadData():
    dbfile = open('pixels_freq', 'rb')
    db = pickle.load(dbfile)
    dbfile.close()
    return db


pixels_freq = loadData()
print("save tags is done")

# 6-load tags
loaded_dividers = np.load('data.npy')
print("load tags is done")


# 7-decode each tag
i = 0
decoded_pixels = []
while(i < len(loaded_dividers)):
    decoded_block_size = Decode_interval(
        loaded_dividers[i], pixels_freq)
    decoded_pixels += decoded_block_size
    print(i)
    i += 1


print("decoded pixels is done")
print("---------------------")
# 8-generate photo
print("watch decoded image")

decoded_pixels= decoded_pixels[:len(decoded_pixels)-main.padding]
print("decoded_pixels", len(decoded_pixels))
decoded_pixels = np.reshape(decoded_pixels, (main.height, main.width))
cv2.imwrite("decodedimage.png", decoded_pixels)

sys.exit()
