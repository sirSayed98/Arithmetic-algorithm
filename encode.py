from PIL import Image
from collections import defaultdict
from fractions import Fraction
import numpy as np
from collections import OrderedDict
import json

# Opening JSON file
with open('sample.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)




def Build_probability(pixels):
    counts = defaultdict(int)
    for code in pixels:
        counts[code] += 1
    output_pixels_frequency = dict()
    length = len(pixels)
    cumulative_count = 0
    for code in counts:
        code_width = counts[code]
        freq_pair = Fraction(cumulative_count, length), Fraction(
            code_width, length)  # build line of code with its width(frequency)
        output_pixels_frequency[code] = freq_pair
        cumulative_count += code_width

    print("Build probaability is done")
    return output_pixels_frequency


def Encode_interval(pixels, pixels_freq):
    start = Fraction(0, 1)  # start interval
    width = Fraction(1, 1)  # width   interval
    for code in pixels:
        code_start, code_width = pixels_freq[code]
        start += code_start * width
        width *= code_width
    # slides guide  #average is better than start
    return np.float64(start+width/2)

    # I use np.float64 to store it logical size as
    # Fraction is object and make size of npy file much bigger
    # but we will get some wrong values of pixels
    # if you return it as fraction no wrong value you will get
    # you can use np.float32 , np.float16 but accuracy will be worse
