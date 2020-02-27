# encoding:utf-8
import cv2
import numpy as np
import matplotlib.pyplot as plt

#每次出现一个图像都按键盘任意键来关闭窗口，不要用鼠标叉掉窗口否则会终止程序

picture_prefix = ''

def hist_color(src):
    image = cv2.imread(picture_prefix+src, cv2.IMREAD_COLOR)
    sum = np.sum(image.reshape(-1, 3), axis=0)
    sum = sum / np.sum(image)
    plt.title('Color Histogram of '+src.upper())
    plt.bar(['blue', 'green', 'red'], sum, width=0.3, color=['royalblue', 'springgreen', 'red'])
    plt.draw()
    plt.waitforbuttonpress(0)
    plt.close('all')


def hist_gray(src):
    image = cv2.imread(picture_prefix+src, cv2.IMREAD_GRAYSCALE)
    onedimention = image.ravel()
    plt.title('Gray Histogram of '+src.upper())
    plt.hist(x=onedimention, bins=256, density=1)
    plt.draw()
    plt.waitforbuttonpress(0)
    plt.close('all')

def hist_gradient(src):
    image = cv2.imread(picture_prefix+src, cv2.IMREAD_GRAYSCALE)
    image = image.astype('int32')
    Ix = (image[:,2:]-image[:,:-2])[1:-1,:]
    Iy = (image[2:,:]-image[:-2,:])[:,1:-1]
    gradient_matrix = np.sqrt(Ix**2+Iy**2)
    onedimention = gradient_matrix.ravel()
    plt.title('Gradient Histogram of '+src.upper())
    plt.hist(x=onedimention, bins=256, density=1)
    plt.draw()
    plt.waitforbuttonpress(0)
    plt.close('all')


if __name__ == '__main__':
    for i in [1,2]:
        picture_name = 'img{}.png'.format(str(i))
        image = cv2.imread(picture_prefix+picture_name)
        cv2.namedWindow(picture_name.upper())
        cv2.imshow(picture_name.upper(),image)
        cv2.waitKey(0)
        hist_color(picture_name)
        hist_gray(picture_name)
        hist_gradient(picture_name)
        cv2.destroyAllWindows()

