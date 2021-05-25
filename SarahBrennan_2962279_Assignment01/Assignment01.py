# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 10:45:38 2019

@author: Sarah Brennan 2962279
"""

import sys
import calendar
import json
import requests

from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QCalendarWidget, QLabel, QComboBox, QDoubleSpinBox, QLineEdit, QPushButton, QErrorMessage
from urllib.request import urlopen
from PyQt5.QtCore import QDate
from decimal import Decimal


#import pyqtgraph as pg

class CurrencyConverter(QWidget):
    global currentYear, currentMonth, currentDay

    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    currentDay = datetime.now().day

    def __init__(self, Parent = None):
        super().__init__()
        self.setWindowTitle('Currency Converter - Assignment 1 - Sarah Brennan - 2962279')
        self.setGeometry(400, 300, 680, 322)
        self.initUI()
        self.conversions(QDate.currentDate().toString('yyyy-MM-dd'))
        #self.download_unzip() # call method to test it

    def initUI(self):
        
        #From Currency Label
        
        self.fromLbl = QLabel('From Currency:', self)
        self.fromLbl.move(39, 20)
        
        #Conversion drop down from
        self.fromComboBox = QComboBox(self)
        #Items in dropw down
        self.fromComboBox.addItem('')
        self.fromComboBox.addItem('€ - Euro')
        self.fromComboBox.addItem('£ - GPB')
        self.fromComboBox.addItem('$ - US Dollars')
        #size of dropdown
        self.fromComboBox.resize(200, 20)
        #position of dropdown
        self.fromComboBox.move(133, 18)     
        
        #To Currency Label
        self.toLbl = QLabel('To Currency:', self)
        self.toLbl.move(385, 20)
        
        #Conversion drop down to
        self.toComboBox = QComboBox(self)
        self.toComboBox.addItem('')
        self.toComboBox.addItem('€ - Euro')
        self.toComboBox.addItem('£ - GPB')
        self.toComboBox.addItem('$ - US Dollars')
        self.toComboBox.resize(200, 20)
        self.toComboBox.move(462, 18)
        
        #Amount to convert label
        self.amountLbl = QLabel('Amount to convert:', self)
        self.amountLbl.move(20, 47)  
        
        #Amount to convert spin box
        self.amountTextbox = QDoubleSpinBox(self)
        #sets original value
        self.amountTextbox.setMinimum(1)
        self.amountTextbox.move(133, 45)
        self.amountTextbox.resize(200, 20)
        #used for min and max conversion size
        self.amountTextbox.setRange(1, 1000000)
        
        #Conversion result label
        self.resultLbl = QLabel('Result of conversion based on most recent rates:', self)
        self.resultLbl.move(350, 47)   
        
        #Conversion result text box
        self.resultTextbox = QLineEdit(self)
        self.resultTextbox.move(600, 45)
        self.resultTextbox.resize(62, 20)
        #read only so cannot make changes to text box
        self.resultTextbox.setReadOnly(True)
        
        #Submit button
        self.submitBtn = QPushButton('Submit', self)
        self.submitBtn.move(305, 80)
        #go to function conversionSelected when button selected
        self.submitBtn.clicked.connect(self.conversionSelected)
        
        #Calendar on left side
        self.calendar = QCalendarWidget(self)
        self.calendar.move(20, 120)
        self.calendar.setGridVisible(True)
        #set max date in calendar
        self.calendar.setMaximumDate(QDate(currentYear, currentMonth, calendar.monthrange(currentYear, currentMonth)[1]))
        #set the date selected to be current date when app starts
        self.calendar.setSelectedDate(QDate(currentYear, currentMonth, currentDay))
        self.calendar.clicked.connect(self.printDateInfo)
        
        #Calendar on right side
        self.calendar02 = QCalendarWidget(self)
        self.calendar02.move(350, 120)
        self.calendar02.setGridVisible(True)        
        self.calendar02.setMaximumDate(QDate(currentYear, currentMonth, calendar.monthrange(currentYear, currentMonth)[1]))        
        self.calendar02.setSelectedDate(QDate(currentYear, currentMonth, currentDay))      
        self.calendar02.clicked.connect(self.printDateInfo)
        

    #How date looks
    def printDateInfo(self, qDate):
        print('{0}/{1}/{2}'.format(qDate.month(), qDate.day(), qDate.year()))
        print(f'Day Number of the year: {qDate.dayOfYear()}')
        print(f'Day Number of the week: {qDate.dayOfWeek()}')
        
    #Get information from csv file
    def conversions(self, date):
        access_key = '83a25d0a98d01bcae1d28f8b27ec92ce'
        print(date)
        #date here is to get the date selected from user in left calendar
        url = 'http://data.fixer.io/api/'+ date +'?access_key=' + access_key
        response = requests.get(url)
        data = response.text
        
        parsed = json.loads(data)
        
        print(json.dumps(parsed, indent=4))
        
        date = parsed['date']
        print(date)
        
        #gets rates from fixer.io
        self.eurRate = parsed['rates']['EUR']
        self.gbpRate = parsed['rates']['GBP']
        self.usdRate = parsed['rates']['USD']
                
        """ Print out the current rate compared to euro
        print(self.eurRate)   
        print(self.gbpRate)
        print(self.usdRate)
        """
        
    #Checks to see which combination of currencies are selected. If none selected, error message shown
    def conversionSelected(self):
        #get date selected by left calendar to do conversion on
        self.conversionDate = self.calendar.selectedDate().toString('yyyy-MM-dd')
        self.conversions(self.conversionDate)
        #gets the conversion rate for each e.g. euro to GBP euro to USD etc. and then rounds it to 4 decimal places
        gbpToUSD = round((self.amountTextbox.value() / self.gbpRate) * self.usdRate, 4)
        gbpToEur = round(self.amountTextbox.value() / self.gbpRate, 4)
        gbpToGBP = round((self.amountTextbox.value() / self.gbpRate) * self.gbpRate, 4)
        usdToEur = round(self.amountTextbox.value() / self.usdRate, 4)
        usdToGBP = round((self.amountTextbox.value() / self.usdRate) * self.gbpRate, 4)
        usdToUSD = round((self.amountTextbox.value() / self.usdRate) * self.usdRate, 4)
        eurToEur = round((self.amountTextbox.value() * self.eurRate), 4)
        eurToGBP = round((self.amountTextbox.value() * self.gbpRate), 4)
        eurToUSD = round((self.amountTextbox.value() * self.usdRate), 4)
        
        #if statements that check which combo chosen to do conversion rate
        if str(self.fromComboBox.currentText()) == '€ - Euro' and str(self.toComboBox.currentText()) == '€ - Euro':
            self.resultTextbox.setText(str(eurToEur))
        elif str(self.fromComboBox.currentText()) == '£ - GPB' and str(self.toComboBox.currentText()) == '€ - Euro':
            self.resultTextbox.setText(str(gbpToEur))
        elif str(self.fromComboBox.currentText()) == '$ - US Dollars' and str(self.toComboBox.currentText()) == '€ - Euro':
            self.resultTextbox.setText(str(usdToEur))
        elif str(self.fromComboBox.currentText()) == '€ - Euro' and str(self.toComboBox.currentText()) == '£ - GPB':
            self.resultTextbox.setText(str(eurToGBP))
        elif str(self.fromComboBox.currentText()) == '£ - GPB' and str(self.toComboBox.currentText()) == '£ - GPB':
            self.resultTextbox.setText(str(gbpToGBP))
        elif str(self.fromComboBox.currentText()) == '$ - US Dollars' and str(self.toComboBox.currentText()) == '£ - GPB':
            self.resultTextbox.setText(str(usdToGBP))
        elif str(self.fromComboBox.currentText()) == '€ - Euro' and str(self.toComboBox.currentText()) == '$ - US Dollars':
            self.resultTextbox.setText(str(eurToUSD))
        elif str(self.fromComboBox.currentText()) == '£ - GPB' and str(self.toComboBox.currentText()) == '$ - US Dollars':
            self.resultTextbox.setText(str(gbpToUSD))
        elif str(self.fromComboBox.currentText()) == '$ - US Dollars' and str(self.toComboBox.currentText()) == '$ - US Dollars':
            self.resultTextbox.setText(str(usdToUSD))
        else:
            self.showWarningMessage()
           
    #Error message prints when no rate is selected in either or both combo boxes
    def showWarningMessage(self):
        self.msg = QErrorMessage()
        self.msg.showMessage('Please select currency to convert')
        self.msg.setWindowTitle('Currency Error')
        
    #def graph(self):
        #self.myLayout = QGridLayout()


def main():
	app = QApplication(sys.argv)
	currency_converter = CurrencyConverter()
	currency_converter.show()
	sys.exit(app.exec_())

main()