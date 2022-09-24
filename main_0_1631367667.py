#create the Easy Editor photo editor here!

from fileinput import filename
import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog, # Dialogue for opening files (and folders)
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)

from PyQt5.QtCore import Qt # needs a Qt.KeepAspectRatio constant to resize while maintaining proportions
from PyQt5.QtGui import QPixmap # screen-optimised
from PIL import Image
#--------------------------------------------
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)
#--------------------------------------------
app = QApplication([])
win = QWidget()       
win.resize(700, 500) 
win.setWindowTitle('Easy Editor')
lb_image = QLabel("Image")
btn_dir = QPushButton("Folder")
lw_files = QListWidget()
 
btn_left = QPushButton("Left")
btn_right = QPushButton("Right")
btn_flip = QPushButton("Mirror")
btn_sharp = QPushButton("Sharpness")
btn_bw = QPushButton("B/W")
 
row = QHBoxLayout()          # Main line
col1 = QVBoxLayout()         # divided into two columns
col2 = QVBoxLayout()
col1.addWidget(btn_dir)      # in the first - directory selection button
col1.addWidget(lw_files)     # and file list
col2.addWidget(lb_image, 95) # in the second - image
row_tools = QHBoxLayout()    # and button bar
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)
 
row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)
 
win.show()

workdir = ''
 
def filter(files, extensions):
   result = []
   for filename in files:
       for ext in extensions:
           if filename.endswith(ext):
               result.append(filename)
   return result
 
def chooseWorkdir():
   global workdir
   workdir = QFileDialog.getExistingDirectory()
 
def showFilenamesList():
   extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
   chooseWorkdir()
   filenames = filter(os.listdir(workdir), extensions)
   lw_files.clear()
   for filename in filenames:
       lw_files.addItem(filename)
 
btn_dir.clicked.connect(showFilenamesList)

class ImageProcessor():
   def __init__(self):
      self.dir = None
      self.filename = None
      self.image = None
      self.save_dir = "Modified/"

   def loadImage(self, dir, filename):
      self.dir = dir
      self.filename = filename
      image_path = os.path.join(dir, filename)
      self.image = Image.open(image_path)

   def showImage(self, path):
      lb_image.hide()
      pixmapimage = QPixmap(path)
      w, h = lb_image.width(), lb_image.height()   #get height, width
      pixmapimage = pixmapimage.scaled(w,h, Qt.KeepAspectRatio) #image fit in window
      lb_image.setPixmap(pixmapimage)             #set the image
      lb_image.show()

   def do_bw(self):
      self.image = self.image.convert("L")
      self.saveImage()
      #show my saved imaged
      image_path = os.path.join(self.dir, self.save_dir, self.filename)
      self.showImage(image_path)

    #--------------------------------------------
    
   def do_left(self):
       self.image = self.image.transpose(Image.ROTATE_90)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)
 
   def do_right(self):
       self.image = self.image.transpose(Image.ROTATE_270)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)
 
   def do_flip(self):
       self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)
 
   def do_sharpen(self):
       self.image = self.image.filter(SHARPEN)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)

     #--------------------------------------------

   def saveImage(self):
      path = os.path.join(self.dir, self.save_dir)
      #creating the folder
      if not(os.path.exists(path) or os.path.isdir(path)):
           os.mkdir(path)
      #save image to folder
      image_path = os.path.join(path, self.filename)
      self.image.save(image_path)
      

workimage = ImageProcessor()

def showChosenImage():
   if lw_files.currentRow() >= 0:
      filename = lw_files.currentItem().text()
      workimage.loadImage(workdir, filename)
      image_path = os.path.join(workimage.dir, workimage.filename)
      workimage.showImage(image_path)

#connceting buttons
lw_files.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)

#--------------------------------------------
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_flip.clicked.connect(workimage.do_flip)
#--------------------------------------------


app.exec()
