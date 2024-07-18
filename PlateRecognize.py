import numpy as np
import cv2 as cv

class LicensePlateRecognition:
    def __init__(self, imgpath, temppath, images):
        self.imgpath = imgpath
        self.temppath = temppath
        self.images = images
        self.current_image_index = 0

    def EdgeDetectMorph(self, image):
        grayimage = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(grayimage, (5, 5), 0)
        _, otsu_threshold = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        return otsu_threshold

    def FindArea(self, image, closedimage):
        konuminfos = []
        contours, _ = cv.findContours(closedimage, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        i=0
        for contour in contours:
            area = cv.contourArea(contour)
            if area > 500:
                x, y, w, h = cv.boundingRect(contour)
                aspect_ratio = w / float(h)
                if 3 < aspect_ratio < 7:

                    konuminfos.append((x, y, w, h))
                    i+=1
        return  konuminfos

    def Plate(self, image, liste):
        x, y, w, h = liste
        return image[y:h + y, x:w + x]

    def PlakaMorphAndDetectPlaces(self, plaka):
        plakagray = cv.cvtColor(plaka, cv.COLOR_BGR2GRAY)
        _, threshplaka = cv.threshold(plakagray, 128, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        contours, _ = cv.findContours(threshplaka, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        bulunankoseler = []
        for contour in contours:
            x, y, w, h = cv.boundingRect(contour)
            if w > 5 and h > 5:
                bulunankoseler.append((x, y, w, h))
        return sorted(bulunankoseler, key=lambda x: x[0])

    def Words(self, image, konumlar):
        images = {}
        for i, konum in enumerate(konumlar, start=1):
            x, y, w, h = konum
            img_crop = image[y:y + h, x:x + w]
            images[f'img{i}'] = img_crop
        return images

    def HarfTemplates(self):
        words = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "R", "S", "T", "U", "V", "Y", "Z", "X", "W", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        templates = {}
        for word in words:
            img_crop = cv.imread(self.temppath + f'{word}.png')
            img_crop = cv.cvtColor(img_crop, cv.COLOR_BGR2GRAY)
            _, binary = cv.threshold(img_crop, 128, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
            contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            x, y, w, h = cv.boundingRect(contours[0])
            img_crop = binary[y:y + h, x:x + w]
            img_crop = cv.resize(img_crop, (38, 20), interpolation=cv.INTER_AREA)
            templates[f'img{word}'] = img_crop
        return templates

    def ResizeCharAndCompare1(self,harfler, temp):  ##Turk plakasi icin ozellestirilmis
        okunanplaka = ""
        rakamlar = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        i = 0
        kernel = np.ones((5, 5), np.uint8)
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

            else:
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
            high1 = 0

        return okunanplaka

    def ResizeCharAndCompare(self,harfler, temp):
        okunanplaka = ""
        for name, img in harfler.items():
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
            okunanplaka = okunanplaka + bulunanharf[3]
            high1 = 0

        return okunanplaka

    def show_image(self):
        bulunma = False
        image_path = self.imgpath + self.images[self.current_image_index]
        image = cv.imread(image_path)
        image = cv.resize(image,(640,480))
        closed = self.EdgeDetectMorph(image)
        liste = self.FindArea(image, closed)
        for i in range (len(liste)):
            imagecopy = image.copy()
            konum = liste[i]
            x, y, w, h = konum
            plaka = self.Plate(imagecopy, konum)
            harfler = self.Words(plaka, self.PlakaMorphAndDetectPlaces(plaka))
            templates = self.HarfTemplates()
            plaka_text = self.ResizeCharAndCompare1(harfler, templates) #For Turkish Plates
            #plaka_text = self.ResizeCharAndCompare(harfler, templates) For other countries

            if len(plaka_text)>4 and len(plaka_text)<10 and bulunma==False:

                cv.rectangle(imagecopy, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv.imshow('area', imagecopy)
                print('Okunan Plaka:',plaka_text)
                bulunma=True
        if (bulunma==False):
            cv.imshow('area', imagecopy)
            print("Plaka algilanamadi")




    def next_image(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.images)
        self.show_image()

    def previous_image(self):
        self.current_image_index = (self.current_image_index - 1) % len(self.images)
        self.show_image()
