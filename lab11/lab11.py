import  numpy as np
import cv2

def get_gradient(img):

    img_sobelx = cv2.Sobel(img,cv2.CV_16S,1,0,3)
    gradient_x = cv2.convertScaleAbs(img_sobelx)

    img_sobely = cv2.Sobel(img,cv2.CV_16S,0,1,3)
    gradient_y = cv2.convertScaleAbs(img_sobely)

    gradient=np.hypot(gradient_x,gradient_y)
    gradient=np.asarray(gradient,dtype=np.uint8)

    np.seterr(divide='ignore', invalid='ignore')
    direction = np.divide(img_sobely,img_sobelx)
    direction[np.isnan(direction)]=0.0
    direction[np.isinf(direction)]=0.0

    return (gradient,direction)

def non_maximum(gradient,direction):
    rows= image.shape[0]
    columns = image.shape[1]

    for i in range(1,rows-1):
        for j in range(1,columns-1):
            dtemp1 = 256
            dtemp2 = 256

            if (direction[i][j]>1):
                dtemp1 = (1-1/direction[i][j])*gradient[i-1][j]+1/direction[i][j]*gradient[i-1][j+1]
                dtemp2 = (1-1/direction[i][j])*gradient[i+1][j]+1/direction[i][j]*gradient[i+1][j-1]
            elif(0<=direction[i][j]<=1):
                dtemp1 = (1-direction[i][j])*gradient[i][j+1]+direction[i][j]*gradient[i-1][j+1]
                dtemp2 = (1-direction[i][j])*gradient[i][j-1]+direction[i][j]*gradient[i+1][j-1]
            elif(0>direction[i][j]>-1):
                dtemp1 = (1+direction[i][j])*gradient[i][j+1]-direction[i][j]*gradient[i+1][j+1]
                dtemp2 = (1+direction[i][j])*gradient[i][j-1]-direction[i][j]*gradient[i-1][j-1]
            elif(direction[i][j]<=-1):
                dtemp1 = (1+1/direction[i][j])*gradient[i+1][j]-1/direction[i][j]*gradient[i+1][j+1]
                dtemp2 = (1+1/direction[i][j])*gradient[i-1][j]-1/direction[i][j]*gradient[i-1][j-1]

            if not (dtemp1<=gradient[i][j] and dtemp2<=gradient[i][j]):
                gradient[i][j] = 0

    return gradient

def threshold(gradient,lowradio=0.2,highradio=0.4):
    high = gradient.max()*highradio
    low = gradient.max()*lowradio

    weak = np.int32(70)
    strong = np.int32(255)

    strong_i,strong_j = np.where(gradient >= high)
    weak_i,weak_j = np.where((gradient>=low) & (gradient<high))
    zero_i,zero_j = np.where((gradient<low))

    gradient[strong_i,strong_j] = strong
    gradient[weak_i,weak_j] = weak
    gradient[zero_i,zero_j] = 0

    return gradient,weak,strong

def link_edge(gradient,weak,strong):
    rows,columns = gradient.shape

    for i in range(1,rows-1):
        for j in range(1,columns-1):
            if (gradient[i][j]==weak):
                try:
                    if (gradient[i-1][j-1]==strong or gradient[i-1][j]==strong or gradient[i-1][j+1]==strong
                    or gradient[i][j-1]==strong or gradient[i][j+1]==strong or gradient[i+1][j-1]==strong
                    or gradient[i+1][j]==strong or gradient[i+1][j+1]==strong):
                        gradient[i][j]=strong
                    else:
                        gradient[i][j] = 0
                except IndexError:
                    pass
    return gradient

if __name__=='__main__':

    for i in [1,2,3]:
        image = cv2.imread('{}.jpg'.format(i),cv2.IMREAD_GRAYSCALE)

        gause_img = cv2.GaussianBlur(image,(3,3),0)
        (gradient,direction) = get_gradient(gause_img)
        gradient = non_maximum(gradient,direction)
        gradient,weak,strong = threshold(gradient)
        finaledge = link_edge(gradient,weak,strong)

        Canny_img = cv2.Canny(image, 50, 150)

        cv2.imshow('raw image',image)
        cv2.imshow('my_canny',finaledge)
        cv2.imshow('cv2_canny',Canny_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

