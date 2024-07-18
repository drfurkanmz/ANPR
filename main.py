from tkinter import Tk, Button
import cv2 as cv
from PlateRecognize import LicensePlateRecognition

def main():
    imgpath = "/Users/furkan/Downloads/opencv-main/images/"
    temppath = "/Users/furkan/Downloads/opencv-main/templates/"
    images = ["araba2.jpg", "araba3.jpeg", "araba4.jpeg", "araba5.jpeg", "araba6.jpeg"]

    recognizer = LicensePlateRecognition(imgpath, temppath, images)

    root = Tk()
    root.title("Change Images")
    root.geometry("800x600")

    next_button = Button(root, text="Next", command=recognizer.next_image)
    next_button.pack(side="right")

    previous_button = Button(root, text="Previous", command=recognizer.previous_image)
    previous_button.pack(side="left")


    recognizer.show_image()
    root.mainloop()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
