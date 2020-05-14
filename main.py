from PIL import Image
import numpy as np
import encode
import decode
import cv2
import json
import os
import pickle

# help in storing pixels_freq
def storeData(thisdict):
    if os.path.exists('pixels_freq'):
        os.remove("pixels_freq")

    dbfile = open('pixels_freq', 'ab')
    # source, destination
    pickle.dump(thisdict, dbfile)
    dbfile.close()


def validate_numeric(value_string, numeric_type=int):
    """Validate a string as being a numeric_type"""
    try:
        return numeric_type(value_string)
    except ValueError:
        raise


Block_size = 0
while True:
    Block_size = input('Enter Block_size:  ')
    try:
        Block_size = validate_numeric(Block_size, int)
    except ValueError:
        print("Try again - that wasn't an integer ")
        continue
    else:
        break

# if you make Block_size more than 4 you will get more wrong pixels

# 1-read image
# Opening JSON file
with open('sample.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)

path = json_object['path']
im = Image.open(path)
width, height = im.size  # get width and height
size = width*height
print("width of photo: ", width)
print("height of photo: ", height)
print("size: ", size)


# 2-flaten image
pixels = list(im.getdata())  # read values of pixels

padding = 0
while len(pixels) % Block_size != 0:
    padding += 1
    pixels += [0]
if(padding>0):
    print("added ",padding," for padding")


# handle if pixels%16 != 0


# 3-get probability
pixels_freq = encode.Build_probability(pixels)

# 4-encode intervals foreach Block_size
i = 0
dividers = []
while(i < size):
    tag = encode.Encode_interval(pixels[i:i+Block_size], pixels_freq)
    dividers.append(tag)
    i = i+Block_size
print("decode tags is done")

typeOfsaving = 0
while True:
    typeOfsaving = input('Enter 1-float16 2-float32  3-or more float-64   ')
    try:
        typeOfsaving = validate_numeric(typeOfsaving, int)
    except ValueError:
        print("Try again - that wasn't an integer ")
        continue
    else:
        break

if typeOfsaving == 1:
    arr = np.array(dividers, dtype='float16')
elif typeOfsaving == 2:
    arr = np.array(dividers, dtype='float32')
else:
    arr = np.array(dividers, dtype='float64')

# 5-save array
np.save('data.npy', arr)
storeData(pixels_freq)

# go to decode file automatically
