# import time

from icecream import ic
import matplotlib.pyplot as plt
from skimage import io
from skimage.util import random_noise
from statements import useful_methods
from statements.useful_methods import rand_string
from utils.file_util import save_file, delete_file


def change_photo(photo, file_ex):
    filename = ''

    number = useful_methods.rand_num(1, 5)
    rand_str = rand_string(str_length=10)
    filename = filename + rand_str + file_ex
    save_file(photo, filename)
    # todo to delete
    image = io.imread(filename)
    print(type(image))
    noised_filename = filename.replace('.jpg', '_rotated.jpg')
    sigma = float(number) / 175
    noised = random_noise(image, var=sigma ** 2)
    plt.imsave(noised_filename, noised)
    plt.close()
    try:
        delete_file(filename)
    except OSError as e:
        print(type(e), e)

    ic('saved')
    return noised_filename
