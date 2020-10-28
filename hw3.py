import sys
from PIL import Image
from image_info import image_info
from PySide2.QtWidgets import(QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QWidget,
QLineEdit,QComboBox,QPushButton,QLabel)
from PySide2.QtCore import Slot
#header
#Hw3.py 
#abstract: create a gui where the user can input a image to search for and be 
#presented with an image that is most relevant to their search tags.
#What works: everything, but presenting the correct image if they were to search for an image 
# and matched 2 pictures but presents the one that comes first alphabetically

class mySearch(QWidget):
    def __init__(self):
        super().__init__()
        vbox = QVBoxLayout()
        self.mylist = ["Sepia","Thumbnail","Negative","Grayscale","None"]
        self.userline = QLineEdit("Enter a image tag")
        self.userline.setMinimumWidth(250)
        self.userline.returnPressed.connect(self.on_submit)
        self.filterbox = QComboBox()
        self.filterbox.addItems(self.mylist)
        self.nameline = QLabel("")
        vbox.addWidget(self.userline)
        vbox.addWidget(self.filterbox)
        vbox.addWidget(self.nameline)



        self.setLayout(vbox)

    
    @Slot()
    def on_submit(self):
        search = self.userline.text()
        keylist = search.split()
        self.nameline.setText("Image name: " + image_info[keyimage(image_info,keylist)]['title'])
        imageopen = Image.open(image_info[keyimage(image_info,keylist)]['id'] + ".jpg")
        filter1(imageopen,self.filterbox.currentText()).show()
        print(self.filterbox.currentText())

def filter1(image,filter):
    height = image.height
    width = image.width
    if(filter == "Thumbnail"):
        sourcew = 0
        canvas = Image.new('RGB',(width//2,(height//2)+1))
        for w in range(0,width,2):
            sourceh = 0
            for h in range(0,height,2):
                pixel = image.getpixel((w,h))
                canvas.putpixel((sourcew,sourceh),pixel)
                sourceh +=1
            sourcew+=1
        print("Width: " + str(sourcew) + " Height: " + str(sourceh))
        print(str(width//2) + " " + str(height//2))
    
    elif(filter == "Sepia"):
        sourcew = 0
        canvas = Image.new('RGB',(width,height))
        for w in range(0,width):
            for h in range(0,height):
                pixel = image.getpixel((w,h))
                canvas.putpixel((w,h),sepia(pixel))
    elif(filter == "Negative"):
        canvas = Image.new('RGB',(width,height))
        for w in range(0,width):
            for h in range(0,height):
                pixel = image.getpixel((w,h))
                red = 255-pixel[0]
                green = 255 - pixel[1]
                blue = 255 - pixel[2]
                pixelnegative = (red,green,blue)
                canvas.putpixel((w,h),pixelnegative)
    elif(filter == "Grayscale"):
        canvas = Image.new('RGB',(width,height))
        for w in range(0,width):
            for h in range(0,height):
                pixel = image.getpixel((w,h))
                canvas.putpixel((w,h),grayscale(pixel))
    if(filter == "None"):
        return image
    return canvas
            
def grayscale(p):
    new_red = int(p[0] * 0.299)
    new_green = int(p[1] * 0.587)
    new_blue = int(p[2] * 0.114)
    lumi = new_red + new_green + new_blue
    return(lumi,)*3
def sepia(p):
    # tint shadows
    if p[0] < 63:
        r,g,b = int(p[0] * 1.1), p[1], int(p[2] * 0.9)
    # tint midtones
    elif p[0] > 62 and p[0] < 192:
        r,g,b = int(p[0] * 1.15), p[1], int(p[2] * 0.85)
    # tint highlights
    else:
        r = int(p[0] * 1.08)
        if r > 255:
            r = 255
        g,b = p[1], int(p[2] * 0.5)
    return r, g, b

def keyimage(image_info,keylist):
    image_number = 0
    max = 0
    image_index = 0
    while(image_number < len(image_info)):
        count =0
        for j in image_info[image_number]['tags']:
            for i in keylist:
                if(i.capitalize() == j.capitalize()):
                    count+=1
        print(count)
        if(max<count):
            max = count
            image_index = image_number
            # image_name = image_info[image_number]['id']
        image_number+=1
    return image_index
app = QApplication([])

my_win = mySearch()

my_win.show()

app.exec_()
