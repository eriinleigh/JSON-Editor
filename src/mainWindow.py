#! /usr/bin/env python
# -*- coding: utf-8 -*-

######################################################
############ JSON Editor #############################
############# Erin Terre #############################
######################################################
### mainWindow.py - ##################################
## Contains the interface for the main window ########
######################################################

import commands
import json
import popups
import sys
from PyQt4 import QtGui, QtCore
from functools import partial
from collections import OrderedDict
from formWidget import Form
from tabWidget import Tab


class Window(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.stringData = "{}"
		self.update = False
		self.lastEvent = "Form"
		self.initUI()

	def initUI(self):
		self.setMinimumSize(1700, 700)
		self.setWindowTitle("JSON Text - No Document")

		self.centralWidget = QtGui.QWidget()
		self.horizontalLayout = QtGui.QHBoxLayout(self.centralWidget)

		## create form interface
		self.form = Form(self)
		self.horizontalLayout.addWidget(self.form)

		## create buttons
		self.buttonWidget = QtGui.QWidget()
		self.buttonWidget.setMaximumSize(50,600)
		self.verticalLayout = QtGui.QVBoxLayout(self.buttonWidget)

		spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.button1 = QtGui.QPushButton(">")
		self.button1.clicked.connect(partial(commands.updateTabView, self))
		self.button1.setMinimumSize(25,25)
		self.button1.setMaximumSize(25,25)

		self.button2 = QtGui.QPushButton("<")
		self.button2.clicked.connect(partial(commands.updateFormView, self))
		self.button2.setMinimumSize(25,25)
		self.button2.setMaximumSize(25,25)

		spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)

		self.verticalLayout.addItem(spacerItem1)
		self.verticalLayout.addWidget(self.button1)
		self.verticalLayout.addWidget(self.button2)
		self.verticalLayout.addItem(spacerItem2)

		self.horizontalLayout.addWidget(self.buttonWidget)
		
		## create tab
		self.tab = Tab(self)
		self.horizontalLayout.addWidget(self.tab)

		self.setCentralWidget(self.centralWidget)

		## Create main menu
		mainMenu = self.menuBar()
		mainMenu.setNativeMenuBar(False)
		fileMenu = mainMenu.addMenu('File')

		## Add open button to file menu
		newButton = QtGui.QAction('New File', self)
		newButton.setShortcut('Ctrl+N')
		newButton.setStatusTip('New ')
		newButton.triggered.connect(partial(commands.mainWindow_New, self))
		fileMenu.addAction(newButton)

		## Add open button to file menu
		openButton = QtGui.QAction('Open File', self)
		openButton.setShortcut('Ctrl+O')
		openButton.setStatusTip('Open JSON file')
		openButton.triggered.connect(partial(commands.mainWindow_Open, self))
		fileMenu.addAction(openButton)

		## Add open button to file menu
		saveButton = QtGui.QAction('Save as...', self)
		saveButton.setShortcut('Ctrl+Shift+S')
		saveButton.setStatusTip('Save File')
		saveButton.triggered.connect(partial(commands.mainWindow_Save, self))
		fileMenu.addAction(saveButton)

		## Add open button to file menu
		compareButton = QtGui.QAction('Compare Files', self)
		compareButton.setStatusTip('Open Compare Window')
		compareButton.triggered.connect(partial(popups.showCompareWindow, self))
		fileMenu.addAction(compareButton)