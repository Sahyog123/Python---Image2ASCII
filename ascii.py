import shutil
import tkinter
from tkinter import filedialog

import PIL
from PIL import Image
from PyQt5.QtWidgets import QMainWindow


from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic


ui = None

def image_to_ascii(path):
    #image_path = input("Enter the path to the image field : \n")

    image_path = path

    try:
        image = Image.open(image_path)
    except:
        print(image_path, "Unable to find image ")


    # Resize the image to a smaller size to fit the ASCII art
    width, height = image.size
    aspect_ratio = height / width
    new_width = 120
    new_height = aspect_ratio * new_width * 0.55
    image = image.resize((new_width, int(new_height)))


    # Store image in a cariable
    image = image.convert('L')

    #chars = ["@", "J", "D", "%", "*", "P", "+", "Y", "$", ",", "."]
    chars = ["@", "#", "*", "+", "-", " "]

    pixels = image.getdata()
    new_pixels = [chars[pixel // 51] for pixel in pixels]
    new_pixels = ''.join(new_pixels)

    # split string of chars into multiple strings of length that is equal to the new width and then create a list
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)

    # write to a text file.
    with open("ascii_image.txt", "w") as f:
        f.write(ascii_image)

# User Interface code from here onwards
class UserInterface(QMainWindow):
    def __init__(self):
        super(UserInterface, self).__init__()
        uic.loadUi("UserInterface.ui", self)
        self.show()


    def on_Upload_btn_pressed(self):
        tkinter.Tk().withdraw()  #  bug - prevents an empty tkinter window from appearing

        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpeg *.jpg *.webp")])
        if file_path:
            print(file_path)
            Image1 = self.findChild(QLabel, "Image1")
            pixmap = QPixmap(file_path)
            Image1.setPixmap(pixmap)
            image_to_ascii(file_path)

            with open("ascii_image.txt", "r") as f:
                text_content = f.read()
                Image2 = self.findChild(QLabel, "Image2")
                Image2.setText(text_content)

    def on_Save_btn_pressed(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save As", "", "Text Files (*.txt)")
        if file_path:
            shutil.copyfile("ascii_image.txt", file_path)


def show_window():
    app = QApplication([])
    window = UserInterface()
    app.exec_()

show_window()
#image_to_ascii()
