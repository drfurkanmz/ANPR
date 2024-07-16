import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

dosya = "/Users/furkan/Downloads/"
araba = cv.imread(dosya + "araba.jpg")
araba2 = cv.imread(dosya + "araba2.jpg")
araba3 = cv.imread(dosya + "araba3.jpeg")
araba4 = cv.imread(dosya + "araba4.jpeg")
araba5 = cv.imread(dosya + "araba5.jpeg")
araba6 = cv.imread(dosya + "araba6.jpeg")

/Users/furkan/Desktop/platedet kopyası.py
def EdgeDetectMorph(image):
    grayimage = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(grayimage, (5, 5), 0)

    _, otsu_threshold = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)


    return otsu_threshold


def FindArea(image,closedimage):
    imagecopy = image.copy()
    konuminfos = []
    contours, _ = cv.findContours(closedimage, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv.contourArea(contour)
        if area > 500 :

            x, y, w, h = cv.boundingRect(contour)
            aspect_ratio = w / float(h)

            if 3 < aspect_ratio < 6:

                cv.rectangle(imagecopy, (x, y), (x + w, y + h), (0, 255, 0), 2)
                konuminfos = [x,y,w,h]

    return imagecopy , konuminfos

def Plate (image,liste):
    x,y,w,h = liste
    return image[y:h+y, x:w+x]

closed1 = EdgeDetectMorph(araba4)
cv.imshow("closed yerler",closed1)
tespitlimg, liste = FindArea(araba4,closed1)

cv.imshow("bulunan yerler",tespitlimg)

plaka = Plate(tespitlimg,liste)

cv.imshow('plaka', plaka)
def PlakaMorphAndDetectPlaces(plaka):
    plakagray = cv.cvtColor(plaka, cv.COLOR_BGR2GRAY)
    _, threshplaka = cv.threshold(plakagray, 128, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    contours, _ = cv.findContours(threshplaka, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    bulunankoseler = []
    a = 0
    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        if w > 5 and h > 5 :  # Karakterlerin boyutlarına göre filtreleme

            bulunankoseler.append((x, y, w, h))
            a += 1

    return bulunankoseler






bulunankonumlar = PlakaMorphAndDetectPlaces(plaka)
bulunankonumlar = sorted(bulunankonumlar, key=lambda x: x[0])

def Words(image,konumlar):
    images = {}
    i= 0
    for konum in konumlar :
        i+=1
        x,y,w,h = konum
        img_crop = image[y:y + h, x:x + w]
        images[f'img{i}'] = img_crop

    return images

harfler = Words(plaka,bulunankonumlar)

def HarfTemplates ():
    words = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","R","S","T","U","V","Y","Z","X","W","1","2","3","4","5","6","7","8","9","0"]
    templates = {}

    for word in words:
        img_crop = cv.imread(dosya + f'{word}.png')
        img_crop = cv.cvtColor(img_crop,cv.COLOR_BGR2GRAY)

        _, binary = cv.threshold(img_crop, 128, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        x, y, w, h = cv.boundingRect(contours[0])
        img_crop = binary[y:y + h, x:x + w]

        img_crop = cv.resize(img_crop, (38, 20), interpolation=cv.INTER_AREA)
        templates[f'img{word}'] = img_crop
    return templates

templates = HarfTemplates()



def ResizeCharAndCompare(harfler,temp):
    okunanplaka = ""
    for name, img in harfler.items():

        resizeimg = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        _, binary = cv.threshold(resizeimg, 128, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        x, y, w, h = cv.boundingRect(contours[0])
        resizeimg = binary[y:y + h, x:x + w]
        resizeimg = cv.resize(resizeimg, (38, 20), interpolation=cv.INTER_AREA)



        high1=0
        for name1,img1 in temp.items():

            result = cv.matchTemplate(resizeimg, img1, method=cv.TM_CCORR_NORMED)
            if result > high1 :
                high1 = result
                bulunanharf = name1




        okunanplaka = okunanplaka + bulunanharf[3]
        high1=0

    return okunanplaka

def ResizeCharAndCompare1(harfler,temp): ##Turk plakasi icin ozellestirilmis
    okunanplaka = ""
    rakamlar = ["1","2","3","4","5","6","7","8","9","0"]
    i = 0
    kernel = np.ones((5,5),np.uint8)
    for name, img in harfler.items():

        if (i < 2 or i > 4):
            resizeimg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            _, binary = cv.threshold(resizeimg, 128, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
            contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            x, y, w, h = cv.boundingRect(contours[0])
            resizeimg = binary[y:y + h, x:x + w]
            resizeimg = cv.resize(resizeimg, (38, 20), interpolation=cv.INTER_AREA)

            high1 = 0
            for name1, img1 in temp.items():
                if (name1[3] in rakamlar):

                    result = cv.matchTemplate(resizeimg, img1, method=cv.TM_CCORR_NORMED)
                    if result > high1:


                        high1 = result
                        bulunanharf = name1

                else:
                    continue

        else :
            resizeimg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            _, binary = cv.threshold(resizeimg, 128, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
            contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            x, y, w, h = cv.boundingRect(contours[0])
            resizeimg = binary[y:y + h, x:x + w]
            resizeimg = cv.resize(resizeimg, (38, 20), interpolation=cv.INTER_AREA)

            high1 = 0
            for name1, img1 in temp.items():

                result = cv.matchTemplate(resizeimg, img1, method=cv.TM_CCORR_NORMED)
                if result > high1:


                    high1 = result
                    bulunanharf = name1

        i += 1



        okunanplaka = okunanplaka + bulunanharf[3]
        high1=0

    return okunanplaka







str = ResizeCharAndCompare1(harfler,templates)
print(str)

cv.waitKey(0)

