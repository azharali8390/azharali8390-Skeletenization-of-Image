from PIL import Image
import numpy as np
import cv2
import os
import string
import  random


def assignment3(image):
    ROOT_DIR = os.path.abspath(os.curdir) + '/static/images'
    img_grey = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    rows, cols = img_grey.shape
    thresh = 128
    img_binary = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)[1]

    pixels_value_of_gray_image = np.array(img_binary)

    SE = np.zeros((8, 9))
    SE = [[0, 0, 0, 2, 1, 2, 1, 1, 1],
          [1, 2, 0, 1, 1, 0, 1, 2, 0],
          [1, 1, 1, 2, 1, 2, 0, 0, 0],
          [0, 2, 1, 2, 1, 1, 0, 2, 1],
          [2, 0, 0, 1, 1, 0, 1, 1, 2],
          [1, 1, 2, 1, 1, 0, 2, 0, 0],
          [2, 1, 1, 0, 1, 1, 0, 0, 2],
          [2, 0, 0, 1, 1, 0, 1, 1, 2]]
    hit_miss_matrix = np.zeros((rows, cols))
    Thinned_Image = np.zeros((rows, cols))
    check = 0
    # padding
    #we make a matrix with 2 extra rows and  cols to pad the image
    pad_image = np.zeros((rows + 2, cols + 2))
    for i in range(1, rows + 1):
        for j in range(1, cols + 1):
            pad_image[i][j] = pixels_value_of_gray_image[i - 1][j - 1]
    # print(pad_image)
    img3 = Image.fromarray(pad_image)
    # convoloving
    sub_image = np.zeros(9)
    for k in range(8):
        for i in range(1, rows):
            for j in range(1, cols):
                sub_image[0] = pad_image[i - 1][j - 1]
                sub_image[1] = pad_image[i - 1][j]
                sub_image[2] = pad_image[i - 1][j + 1]
                sub_image[3] = pad_image[i][j - 1]
                sub_image[4] = pad_image[i][j]
                sub_image[5] = pad_image[i][j + 1]
                sub_image[6] = pad_image[i + 1][j - 1]
                sub_image[7] = pad_image[i + 1][j]
                sub_image[8] = pad_image[i + 1][j + 1]
                for m in range(0, 9):
                    if SE[k][m] != 2:
                        if sub_image[m] != SE[k][m]:
                            if sub_image[m] != 255:
                                check = 0
                                break
                            else:
                                check = 1
                        else:
                            check = 1
                if check == 1:
                    hit_miss_matrix[i][j] = 255  # 1
                else:
                    hit_miss_matrix[i][j] = 0
                    # now we will calculate thinned image.
        for i in range(0, rows):
            for j in range(0, cols):
                Thinned_Image[i][j] = (pixels_value_of_gray_image[i][j] - (hit_miss_matrix[i][j]))
                # Thinned_Image[i][j] = (pixels_value_of_gray_image[i][j] & (~(hit_miss_matrix[i][j])))
        for i in range(0, rows):
            for j in range(0, cols):
                pixels_value_of_gray_image[i][j] = Thinned_Image[i][j]
                pad_image[i + 1][j + 1] = Thinned_Image[i][j]
        check = 0
    img3 = Image.fromarray(Thinned_Image)
    rand1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7)) + '.jpg'
    img3.convert('RGB').save(ROOT_DIR + '/' + str(rand1))
    return {'output': str(rand1)}
