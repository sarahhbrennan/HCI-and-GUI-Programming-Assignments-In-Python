# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.


"""

from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QFileDialog, QGroupBox, QLabel, QVBoxLayout, QRadioButton, QSlider, QMessageBox
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QPixmap, QCursor
from PyQt5.QtCore import Qt, QPoint, QRect, QSize
import sys

class PaintingApp(QMainWindow):

	#Initialises the main window
    def __init__(self):
        super().__init__()
        
        #position for main window
        top = 100
        left = 100
        width = 1200
        height = 800
        
        icon = 'icons/main.png'
        
        self.setWindowTitle('Sarah Brennan - 2962279 Paint Application')
        self.setGeometry(top, left, width, height)
        #stop user from making app bigger
        self.setFixedSize(width, height)
        self.setWindowIcon(QIcon(icon))
        
        #removes maximise button from main window
        self.setWindowFlags(Qt.Window |
        Qt.CustomizeWindowHint |
        Qt.WindowTitleHint |
        Qt.WindowCloseButtonHint |
        Qt.WindowMinimizeButtonHint |
        Qt.WindowStaysOnTopHint)     
        
        self.initUI()
        
    #initialises GUI for app
    def initUI(self):
        
		#create QImage to be able to draw on, ARGB is used to be able to use transparent, just RGB makes the backgroun black
        self.image = QImage(self.size(), QImage.Format_ARGB32)
        self.image.fill(Qt.transparent)    
        
        #The starting drawing features
        self.drawing = False
        self.brushSize = 1
        self.brushColour = Qt.black        
        self.lastPoint = QPoint()
        self.brushLine = Qt.SolidLine
        self.brushCap = Qt.RoundCap
        self.brushJoin = Qt.RoundJoin
        
        #to be used with eraser to check if it is selected or not
        self.change = False
        #size of eraser
        self._clear_size = 20
        
        #Create Main Menu bar
        mainMenu = self.menuBar()
        
        #Add menu items
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')  
        helpMenu = mainMenu.addMenu('Help')        
        
        #File Menu
        #Icons made by https://www.flaticon.com/authors/dave-gandy Dave Gandy
        openPic = QAction(QIcon('icons/open.png'), 'Open', self)
        openPic.setShortcut('Ctrl+O')
        openPic.setStatusTip('Open Picture')
        fileMenu.addAction(openPic)		
		#Used to call method to open image
        openPic.triggered.connect(self.openFile)
        
        #Icons made by https://www.flaticon.com/authors/dave-gandy Dave Gandy
        savePic = QAction(QIcon('icons/save.png'), 'Save', self)
        savePic.setShortcut('Ctrl+S')
        savePic.setStatusTip('Save Picture')
        fileMenu.addAction(savePic)
        savePic.triggered.connect(self.save)
        
        #Icons made by https://www.flaticon.com/authors/freepik
        clearPic = QAction(QIcon('icons/clear.png'), 'Clear', self)
        clearPic.setShortcut('Ctrl+Del')
        clearPic.setStatusTip('Clear Picture')
        fileMenu.addAction(clearPic)
        clearPic.triggered.connect(self.clear)
        
        #Icons made by https://www.flaticon.com/authors/freepik
        exitApp = QAction(QIcon('icons/exit.png'), 'Exit', self)
        exitApp.setShortcut('Ctrl+Q')
        exitApp.setStatusTip('Exit Application')
        fileMenu.addAction(exitApp)
        exitApp.triggered.connect(self.closeApp)   
        
        #Edit Menu
        #Icons made by https://www.flaticon.com/authors/freepik
        eraseApp = QAction(QIcon('icons/erase.png'), 'Erase', self)
        eraseApp.setShortcut('Ctrl+E')
        eraseApp.setStatusTip('Exit Application')
        editMenu.addAction(eraseApp)
        eraseApp.triggered.connect(self.erase)           
        
        #Help Menu
        #Icons made by https://www.flaticon.com/authors/freepik
        aboutPaint = QAction(QIcon('icons/about.png'), 'About', self)
        aboutPaint.setShortcut('Ctrl+A')
        aboutPaint.setStatusTip('Open Picture')
        helpMenu.addAction(aboutPaint)
        aboutPaint.triggered.connect(self.about)
        
        #Icons made by https://www.flaticon.com/authors/freepik
        helpPaint = QAction(QIcon('icons/help.png'), 'Help', self)
        helpPaint.setShortcut('Ctrl+H')
        helpPaint.setStatusTip('Save Picture')
        helpMenu.addAction(helpPaint)
        helpPaint.triggered.connect(self.helpPopUp)        
        
        #Create tool bar, this adds shortcut links to the toolbar
        self.toolbar = self.addToolBar('Open')
        self.toolbar.addAction(openPic)
        self.toolbar.addAction(savePic)
        self.toolbar.addAction(clearPic)
        self.toolbar.addAction(exitApp)
        self.toolbar.addAction(eraseApp)
        #set to white to prevent drawing being shown
        self.toolbar.setStyleSheet("background-color: white;")
                
        #Group box for brush colours
        self.colourGroup = QGroupBox(self)  
        self.colourGroup.resize(200, 220)   
        self.colourGroup.move(1000, 20)  
        #set to grey to prevent drawing being shown
        self.colourGroup.setStyleSheet("background-color: #DCDCDC;")
        
        vbox = QVBoxLayout()
        self.colourGroup.setLayout(vbox)
        
		#Label at top of group box
        colourLbl = QLabel('Colours', self)
        colourLbl.setStyleSheet("font-size: 20px;")
		#add widget to group box
        vbox.addWidget(colourLbl)
        
        #Brush colour radio buttons
        blackRadio = QRadioButton('Black')
        blackRadio.setIcon(QIcon('icons/black.png'))
        blackRadio.setChecked(True)
		#add widget to group box
        vbox.addWidget(blackRadio)
		#calls method when radio method selected
        blackRadio.toggled.connect(self.black)
        
        self.whiteRadio = QRadioButton('White')
        self.whiteRadio.setIcon(QIcon('icons/white.png'))
		#add widget to group box
        vbox.addWidget(self.whiteRadio)
        self.whiteRadio.toggled.connect(self.white)
        
        blueRadio = QRadioButton('Blue')
        blueRadio.setIcon(QIcon('icons/blue.png'))
		#add widget to group box
        vbox.addWidget(blueRadio)
        blueRadio.toggled.connect(self.blue)
        
        redRadio = QRadioButton('Red')
        redRadio.setIcon(QIcon('icons/red.png'))
		#add widget to group box
        vbox.addWidget(redRadio)
        redRadio.toggled.connect(self.red)
        
        yellowRadio = QRadioButton('Yellow')
        yellowRadio.setIcon(QIcon('icons/yellow.png'))
		#add widget to group box
        vbox.addWidget(yellowRadio)
        yellowRadio.toggled.connect(self.yellow)
        
        greenRadio = QRadioButton('Green')
        greenRadio.setIcon(QIcon('icons/green.png'))
		#add widget to group box
        vbox.addWidget(greenRadio)
        greenRadio.toggled.connect(self.green)
        
        #Group box for brush sizes
        self.sizeGroup = QGroupBox(self)  
        self.sizeGroup.resize(200, 100)   
        self.sizeGroup.move(1000, 240)  
        self.sizeGroup.setStyleSheet("background-color: #DCDCDC;")
        
        vbox = QVBoxLayout()
        self.sizeGroup.setLayout(vbox)
        
        sizeLbl = QLabel('Brush Size', self)
        sizeLbl.setStyleSheet("font-size: 20px;")
        #add widget to group box
        vbox.addWidget(sizeLbl)        
        
        #Brush Sizes slider
		#create horizontal slier
        brushSizeSlider = QSlider(Qt.Horizontal, self)
		#sets the minimum size of slider
        brushSizeSlider.setMinimum(1)
		#selects max size of slider
        brushSizeSlider.setMaximum(10)
		#shows lines beneath slider
        brushSizeSlider.setTickPosition(QSlider.TicksBelow)
		#intervals between sizes in slider
        brushSizeSlider.setTickInterval(1)
		#goes to method for changing brush size when slider changes
        brushSizeSlider.valueChanged[int].connect(self.changeBrushSize)
		#add widget to group box
        vbox.addWidget(brushSizeSlider)
        
        #Group box for brush line type
        self.brushLineGroup = QGroupBox(self)  
        self.brushLineGroup.resize(200, 200)   
        self.brushLineGroup.move(1000, 340)  
        self.brushLineGroup.setStyleSheet("background-color: #DCDCDC;")
        
        vbox = QVBoxLayout()
        self.brushLineGroup.setLayout(vbox)
        
        lineLbl = QLabel('Brush Line Type', self)
        lineLbl.setStyleSheet("font-size: 20px;")
		#add widget to group box
        vbox.addWidget(lineLbl) 
        
        #Brush Line Radio Buttons
        solidRadio = QRadioButton('Solid')
        solidRadio.setChecked(True)
		#add widget to group box
        vbox.addWidget(solidRadio)
        solidRadio.toggled.connect(self.solid)
        
        dashRadio = QRadioButton('Dash Line')
		#add widget to group box
        vbox.addWidget(dashRadio)
        dashRadio.toggled.connect(self.dash)
        
        dashDotRadio = QRadioButton('Dash Dot Line')
		#add widget to group box
        vbox.addWidget(dashDotRadio)
        dashDotRadio.toggled.connect(self.dashDot)
        
        dotRadio = QRadioButton('Dot Line')
		#add widget to group box
        vbox.addWidget(dotRadio)
        dotRadio.toggled.connect(self.dot)
        
        dashDotDotRadio = QRadioButton('Dash Dot Dot Line')
		#add widget to group box
        vbox.addWidget(dashDotDotRadio)
        dashDotDotRadio.toggled.connect(self.dashDotDot)
        
        #Group box for brush cap type
        self.brushCapGroup = QGroupBox(self)  
        self.brushCapGroup.resize(200, 130)   
        self.brushCapGroup.move(1000, 540)  
        self.brushCapGroup.setStyleSheet("background-color: #DCDCDC;")
        
        vbox = QVBoxLayout()
        self.brushCapGroup.setLayout(vbox)
        
        capLbl = QLabel('Brush Cap Type', self)
        capLbl.setStyleSheet("font-size: 20px;")
		#add widget to group box
        vbox.addWidget(capLbl) 
        
        #Brush Cap Radio Buttons
        roundCapRadio = QRadioButton('Round Cap')
        roundCapRadio.setChecked(True)
		#add widget to group box
        vbox.addWidget(roundCapRadio)
        roundCapRadio.toggled.connect(self.roundedCap)
        
        squareRadio = QRadioButton('Square Cap')
		#add widget to group box
        vbox.addWidget(squareRadio)
        squareRadio.toggled.connect(self.square)
        
        flatRadio = QRadioButton('Flat Cap')
		#add widget to group box
        vbox.addWidget(flatRadio)
        flatRadio.toggled.connect(self.flat)
        
         #Group box for brush join type
        self.brushJoinGroup = QGroupBox(self)  
        self.brushJoinGroup.resize(200, 130)   
        self.brushJoinGroup.move(1000, 670)  
        self.brushJoinGroup.setStyleSheet("background-color: #DCDCDC;")
        
        vbox = QVBoxLayout()
        self.brushJoinGroup.setLayout(vbox)
        
        joinLbl = QLabel('Brush Join Type', self)
        joinLbl.setStyleSheet("font-size: 20px;")
		#add widget to group box
        vbox.addWidget(joinLbl) 
        
        #Brush Join Radio Buttons
        roundJoinRadio = QRadioButton('Round Join')
        roundJoinRadio.setChecked(True)
		#add widget to group box
        vbox.addWidget(roundJoinRadio)
        roundJoinRadio.toggled.connect(self.roundedJoin)
        
        squareRadio = QRadioButton('Bevel Join')
		#add widget to group box
        vbox.addWidget(squareRadio)
        squareRadio.toggled.connect(self.bevel)
        
        flatRadio = QRadioButton('Miter Join')
		#add widget to group box
        vbox.addWidget(flatRadio)
        flatRadio.toggled.connect(self.miter)
        
        
	#method for checking if mouse clicked to find where drawing starts
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            #if user is using left mouse button, draw where mouse goes
            self.drawing = True;
            #get the position of where mouse selected
            self.lastPoint = event.pos()
            print(self.lastPoint)
            
	#method for after mouse is selected to track where cursor is drawing
    def mouseMoveEvent(self, event):
        if(event.buttons() == Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColour, self.brushSize, self.brushLine, self.brushCap, self.brushJoin))
			#eraser, deletes what is drawn if eraser is selected
            if self.change:
                r = QRect(QPoint(), self._clear_size * QSize())
                r.moveCenter(event.pos())
                painter.save()
                painter.setCompositionMode(QPainter.CompositionMode_Clear)
                painter.eraseRect(r)
                painter.restore()
            else:
				#if eraser is not selected, draw with what user has selected or default
                painter.drawLine(self.lastPoint, event.pos())
                
            painter.end()
			#get position of cursor
            self.lastPoint = event.pos()
            self.update()
    
    
	#method to check when mouse is released to stop drawing
    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing == False
            
    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())
        
        
	#method to save image to folder
    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "untitled", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ") 
        if filePath == "":
            return
        self.image.save(filePath)
        
        
	#method to open method to edit	
    def openFile(self):
        imagePath, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if imagePath == "":
            return
        self.image.load(imagePath)
        
        
	#method to clear the image already drawn
    def clear(self):
        self.image.fill(Qt.transparent)
        self.update()
        
        
    #method to close app
    def closeApp(self):
        #added feature to check if want image saved before quitting
        buttonReply = QMessageBox.question(self, 'Save?', 'Do you want to save before quitting?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.No:
            self.close()
        else:
            self.save()
            self.close()
    
    
    #method to create eraser to remove part of drawing, similar to paint    
    def erase(self):
        self.change = not self.change
        if self.change:
            #create pixmap for the eraser cursor
            pixmap = QPixmap(QSize(1, 1) * self._clear_size)
            #set the colour of eraser cursor
            pixmap.fill(Qt.white)
            painter = QPainter(pixmap)
            #create outline of eraser cursor
            painter.setPen(QPen(Qt.black, 2))
            painter.drawRect(pixmap.rect())
            painter.end()
            cursor = QCursor(pixmap)
            QApplication.setOverrideCursor(cursor)
            
        else:
            QApplication.restoreOverrideCursor()


    #method to create message box to display about
    def about(self):
        QMessageBox.about(self, "About", "Name: Paint Application \nVersion: 1.0 \nDate of Release: 18/11/2019 \nDesigner: Sarah Brennan - 2962279")
        
        
    #method to create message box to display help
    def helpPopUp(self):   
        QMessageBox.about(self, "Help", "Hurry you fools...and get your work done, no time for help!")


    #method to chenge brush size when slider moved
    def changeBrushSize(self, value):
        self.brushSize = value
 
    
    #methods to change the brush colour to colour selected by user
    def black(self, selected):
        if selected:
            self.brushColour = Qt.black
 
    def white(self, selected):
        if selected:
            self.brushColour = Qt.white
 
    def blue(self, selected):
        if selected:
            self.brushColour = Qt.blue
 
    def red(self, selected):
        if selected:
            self.brushColour = Qt.red
 
    def yellow(self, selected):
        if selected:
            self.brushColour = Qt.yellow
 
    def green(self, selected):
        if selected:
            self.brushColour = Qt.green
            
    #methods to change the line types
    def solid(self, selected):
        if selected:
            self.brushLine = Qt.SolidLine
            
    def dash(self, selected):
        if selected:
            self.brushLine = Qt.DashLine
            
    def dashDot(self, selected):
        if selected:
            self.brushLine = Qt.DashDotLine
            
    def dot(self, selected):
        if selected:
            self.brushLine = Qt.DotLine
            
    def dashDotDot(self, selected):
        if selected:
            self.brushLine = Qt.DashDotDotLine
            
            
    #methods to change cap type of pen
    def roundedCap(self, selected):
        if selected:
            self.brushCap = Qt.RoundCap
            
    def square(self, selected):
        if selected:
            self.brushCap = Qt.SquareCap
            
    def flat(self, selected):
        if selected:
            self.brushCap = Qt.FlatCap
            
            
    #methods to change join type of pen
    def roundedJoin(self, selected):
        if selected:
            self.brushJoin = Qt.RoundJoin
            
    def bevel(self, selected):
        if selected:
            self.brushJoin = Qt.BevelJoin
            
    def miter(self, selected):
        if selected:
            self.brushJoin = Qt.MiterJoin
               
def main():
	app = QApplication(sys.argv)
	painting_app = PaintingApp()
	painting_app.show()
	sys.exit(app.exec_())

main()