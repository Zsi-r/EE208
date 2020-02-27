import cv2
import math
import numpy as np

def ImgResize(pic, scale):  # change the size of the picture
    rows = int(round(pic.shape[1] * scale, 0))#注意行和列是相反的
    columns = int(round(pic.shape[0] * scale, 0))
    return cv2.resize(pic, (rows, columns))

def IntensityAndTheta(im, x, y):
    dx = int(im[x + 1, y]) - int(im[x - 1, y])
    dy = int(im[x, y + 1]) - int(im[x, y - 1])
    intensity = math.hypot(dx, dy)
    theta = int(math.atan2(dy, dx) * 180 / math.pi + 180)  # 以度数为单位
    return intensity, theta

def isValid(img, x, y):
    return (x >= 1) and (x <= (img.shape[0]-3)) and (y >= 1) and (y <= (img.shape[1]-3))

def getMainDirection(img, x0, y0):  # 找到关键点的主方向
    DirectionHist = [0] * 36
    radius = 16
    for i in range(x0 - radius, x0 + radius + 1):
        for j in range(y0 - radius, y0 + radius + 1):
            if not isValid(img, i, j):
                continue
            intensity, theta = IntensityAndTheta(img, i, j)
            theta = theta // 10
            if (theta == 36): theta = 0
            DirectionHist[theta] += intensity
    max = 0
    mainDirectoin = 0
    for item in DirectionHist:
        if (max < item):
            max = item
    mainDirectoin = DirectionHist.index(max)*10
    return mainDirectoin

def insertValue(img, x, y, maindirection):  # x,y:float
    x0 = int(x)
    y0 = int(y)
    theta = (
            IntensityAndTheta(img, x0, y0)[1] * (x0 + 1 - x) * (y0 + 1 - y) +
            IntensityAndTheta(img, x0 + 1, y0)[1] * (x - x0) * (y0 + 1 - y) +
            IntensityAndTheta(img, x0, y0 + 1)[1] * (x0 + 1 - x) * (y - y0) +
            IntensityAndTheta(img, x0 + 1, y0 + 1)[1] * (x - x0) * (y - y0)
    )
    intensity = (
            IntensityAndTheta(img, x0, y0)[0] * (x0 + 1 - x) * (y0 + 1 - y) +
            IntensityAndTheta(img, x0 + 1, y0)[0] * (x - x0) * (y0 + 1 - y) +
            IntensityAndTheta(img, x0, y0 + 1)[0] * (x0 + 1 - x) * (y - y0) +
            IntensityAndTheta(img, x0 + 1, y0 + 1)[0] * (x - x0) * (y - y0)
    )
    degree = theta - maindirection
    if degree < 0: degree += 360
    if degree==360.0:degree =0
    return degree,intensity

def get128vector(img, cx, cy):  # get 128-dimention vector of each corner point
    maindirection = getMainDirection(img, cx, cy) * math.pi / 180.0
    sin = math.sin(maindirection)  # cx,cy:x and y of the corner point
    cos = math.cos(maindirection)

    # 接下来计算4*4=16个块在物体坐标系下的梯度
    x0 = cx + 8 * sin - 8 * cos
    y0 = cy - 8 * cos - 8 * sin
    # 由几何关系可得上面两行代码，此时坐标转到第一个块的最左上角的像素点
    Hist = []
    for i in range(4):  # x1,y1每个块的左上角像素坐标
        for j in range(4):
            x1 = x0 + 4 * i * cos
            y1 = y0 + 4 * j * sin
            # 接下来对每个块里的16个点进行插值(求梯度)
            histtemp = [0] * 8
            for i2 in range(4):
                for j2 in range(4):
                    x2 = x1 + i2*cos
                    y2 = y1 + j2*sin
                    if isValid(img, x2, y2):
                        dir ,intensity = insertValue(img, x2, y2, maindirection)
                        histtemp[int(dir / 45)] += intensity
            Hist += histtemp  # 将8维梯度方向直方图加入到描述子中，由此重复16次，每个角点生成128维描述子

    # 接下来对128维SIFT描述子归一化
    sum = 0
    for i in Hist:
        sum += i
    sum = math.sqrt(sum)
    for item in Hist:
        if sum!=0:
            item /= sum

    return Hist

def getSift(url, scale=1):
    img = cv2.imread(url, cv2.IMREAD_GRAYSCALE)
    #if scale!=1:
    #    img = ImgResize(img, scale)
    #else:
    #    img = ImgResize(img, scale)
    img = ImgResize(img, scale)

    cornersTemp = cv2.goodFeaturesToTrack(img,40,0.01,10)
    corners = []
    cornerVector = []
    for corner in cornersTemp:  # [[[ 44. 234.]],[[1. 2.]]] ---> [(44,234),(1,2)]
        corners.append((int(corner[0][0]),int(corner[0][1])))
        cornerVector.append(get128vector(img, int(corner[0][0]), int(corner[0][1])))

    return corners,cornerVector

def draw(img_t,corner_t,img_i,corner_i):

    rows_t,columns_t = img_t.shape[0],img_t.shape[1]
    rows_i,columns_i = img_i.shape[0],img_i.shape[1]

    output = np.zeros((max([rows_t,rows_i]),columns_i+columns_t,3),dtype='uint8')
    output[:rows_i,:columns_i,:] = np.dstack([img_i])
    output[:rows_t,columns_i:columns_i+columns_t,:] = np.dstack([img_t])

    for i in range(len(corner_t)):

        xt,yt = corner_t[i]
        xi,yi = corner_i[i]

        color = (101,67,257)
        cv2.circle(output, (int(xi),int(yi)), 4, color, 1)
        cv2.circle(output, (int(xt)+columns_i,int(yt)), 4, color, 1)
        cv2.line(output, (int(xi),int(yi)), (int(xt)+columns_i,int(yt)), color, 1)
    cv2.imshow("My Sift result", output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__=='__main__':

    urlt = "target.jpg"#target image
    urli = "dataset/3.jpg"#another input image
    scale = 1 #输入图片(不是target图片)的放大倍数

    corner_t,vector_t = getSift(urlt)
    corner_i,vector_i = getSift(urli,scale)

    chosen = [0]*len(corner_i)#记录角点是否已被记录

    #下面进行角点的匹配,采用欧氏距离遍历
    threshold = 1
    res_t = []#存放匹配的角点，两个list一一对应
    res_i = []

    currentIndex_t = 0
    for vt in vector_t:
        currentIndex_i = 0
        bestIndex = 0 #最佳匹配角点的下标
        min = 100000 #初始值，用来记录最小欧氏距离，即最佳匹配点的距离
        secondmin = 100000 #用来记录次小欧氏距离
        for vi in vector_i:#遍历一遍input image的所有角点，找到最佳匹配点
            sum = 0
            for i in range(128):
                sum += (vt[i]- vi[i])**2
            sum = math.sqrt(sum)
            if (chosen[currentIndex_i]==0 and sum<min):
                secondmin = min
                min = sum
                bestIndex = currentIndex_i
            currentIndex_i += 1
        if ((min/secondmin)<threshold):
            res_t.append(corner_t[currentIndex_t])
            res_i.append(corner_i[bestIndex])
            chosen[bestIndex] = 1
        currentIndex_t += 1

    img_i = cv2.imread(urli)
    img_t = cv2.imread(urlt)
    img_i = ImgResize(img_i,scale)
    draw(img_t,corner_t,img_i,corner_i)
