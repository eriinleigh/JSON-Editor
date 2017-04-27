#! /usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################################
############ JSON Editor ##################################################
############# Erin Terre ##################################################
###########################################################################
### formWidget.py - #######################################################
## Contains the interface for the form widget #############################
## and the functions neccessary to generating/adding/deleting form items ##
###########################################################################

import ast
import commands
import json
import sip
import sys
import popups
from PyQt4 import QtGui, QtCore
from functools import partial
from collections import OrderedDict


class Form(QtGui.QWidget):
	def __init__(self, parent):
		QtGui.QWidget.__init__(self)
		self.jsonData = OrderedDict({})
		self.parent = parent
		self.initUI(parent)

	def initUI(self, parent):
		self.setParent(parent)
		self.setMinimumSize(800, 650)

		self.horizontalLayout = QtGui.QHBoxLayout()
		self.setLayout(self.horizontalLayout)

		self.scrollArea = QtGui.QScrollArea()
		self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.setObjectName("scrollArea")
		self.scrollArea.setEnabled(True)

		self.horizontalLayout.addWidget(self.scrollArea)

		self.scrollAreaContents = QtGui.QWidget()
		self.contentLayout = QtGui.QHBoxLayout(self.scrollAreaContents)
		self.contentLayout.setMargin(0)

		self.scrollArea.setWidget(self.scrollAreaContents)
		
		## the form widget
		self.formWidget = QtGui.QWidget()
		self.formWidget.setObjectName("mainWidget")

		self.formLayout = QtGui.QFormLayout(self.formWidget)

		gridWidget = QtGui.QFrame()

		gridLayout = QtGui.QGridLayout()
		gridLayout.setMargin(0)

		## the combo box
		self.comboBox = QtGui.QComboBox()
		self.comboBox.addItem("Object")
		self.comboBox.addItem("Attribute")
		self.comboBox.addItem("Array")

		addButton = QtGui.QPushButton("ADD")
		addButton.clicked.connect(partial(self.addItemAction, self.comboBox, False, self.formWidget))
		addButton.setMaximumSize(40,25)

		spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

		gridLayout.addWidget(self.comboBox, 0, 1)
		gridLayout.addWidget(addButton, 0, 2)
		gridLayout.addItem(spacerItem, 0, 3)

		gridWidget.setLayout(gridLayout)

		self.formLayout.addRow(gridWidget)

		self.contentLayout.addWidget(self.formWidget)

	######################################################################################################
	##### buildForm() ####################################################################################
	##### builds the form when making changes to form, updating from text view or loading JSON file ######
	######################################################################################################

	def buildForm(self, jsonData, indent, parent):
		layout = parent.layout()

		indentItem = QtGui.QLabel("")

		if indent:
			indentItem.setMinimumSize(30, 20)
		else:
			indentItem.setMinimumSize(1, 20)

		## run until there are no items in jsonData
		if len(jsonData) > 0:
			for item in jsonData:
				if type(jsonData.get(item)) is OrderedDict:
					itemName = json.dumps(item)
					objectWidget = self.createObjectRow(itemName, parent)
					layout.addRow(indentItem, objectWidget)

					newParent = objectWidget
					newJsonData = jsonData[item]

					objectComboBox = objectWidget.findChild(QtGui.QComboBox, "addCombo")
					objectButton = objectWidget.findChild(QtGui.QPushButton, "addButton")
					objectButton.clicked.connect(partial(self.addItemAction, objectComboBox, True, objectWidget))

					self.linkDeleteButton(objectWidget, False)
					self.buildForm(newJsonData, True, newParent)

				elif type(jsonData.get(item)) is list:
					arrayName = json.dumps(item)
					array = jsonData[item]
					arrayWidget = self.createArrayRow(arrayName, array, parent)
					layout.addRow(indentItem, arrayWidget)

					arrayButton = arrayWidget.findChild(QtGui.QPushButton, "addButton")
					arrayButton.clicked.connect(partial(self.addArrayValue, arrayWidget))

					self.linkDeleteButton(arrayWidget, False)

				else:
					attrName = json.dumps(item)
					attrValue = json.dumps(jsonData.get(item))
					attrWidget = self.createAttributeRow(attrName, attrValue, parent)
					self.linkDeleteButton(attrWidget, False)
					layout.addRow(indentItem, attrWidget)
		else: 
			return

	#######################################################################
	##### updateJsonData() ################################################
	##### updates the stored JSON Data when editing or adding form items ##
	#######################################################################

	def updateJsonData(self):
		newData = OrderedDict({})
		newData, syntax = self.createNewData(newData, self.formWidget, True)

		if syntax:
			self.jsonData = newData
			return self.jsonData
		else:
			return self.jsonData

	#############################################################
	##### createNewData() #######################################
	##### creates a dictionary with all values from the form ####
	#############################################################

	def createNewData(self, dictionary, parent, syntax):
		children = parent.children()

		for child in children:
			objectName = child.objectName()

			if objectName == "objectWidget":
				lineWidget = child.findChild(QtGui.QLineEdit, "name")
				name = str(lineWidget.text())
				objectDictionary = OrderedDict()
				objectDictionary, syntax = self.createNewData(objectDictionary, child, syntax)
				try:
					dictionary.update({ast.literal_eval(name) : objectDictionary})
				except:
					popups.showInvalidSyntax()
					syntax = False

			elif objectName == "attrWidget":
				lineWidget = child.findChild(QtGui.QLineEdit, "name")
				name = str(lineWidget.text())
				lineWidget2 = child.findChild(QtGui.QLineEdit, "attrValue")
				value = str(lineWidget2.text())
				try:
					dictionary.update({ast.literal_eval(name) : ast.literal_eval(value)})
				except:
					popups.showInvalidSyntax()
					syntax = False

			elif objectName == "arrayWidget":
				lineWidget = child.findChild(QtGui.QLineEdit, "name")
				name = str(lineWidget.text())
				array = self.buildArray(child)
				try:
					dictionary.update({ast.literal_eval(name) : array})
				except:
					popups.showInvalidSyntax()
					syntax = False

		return dictionary, syntax


	####################################################################
	##### buildArray() #################################################
	##### creates the array variable using the values from the form ####
	####################################################################

	def buildArray(self, parent):
		array = []

		children = parent.children()

		for child in children:
			objectName = child.objectName()

			if objectName == "arrayItemWidget":
				lineWidget = child.findChild(QtGui.QLineEdit, "arrayItemValue")
				value = str(lineWidget.text())

				## check for null values and add the equivilant None
				if value == "null":
					array.append(None)
				else:
					try:
						array.append(ast.literal_eval(value))
					except:
						popups.showInvalidSyntax()
		return array


	#######################################################################################
	##### deleteItem() ####################################################################
	##### deletes an item from the form and adjusts the interface and stored JSON data ####
	#######################################################################################

	def deleteItem(self, widget, arrayItem):
		## update the global jsonData
		self.updateJsonData()

		parentList = []
		currWidget = widget
		objectName = widget.objectName()

		## get the values for all the parents
		while objectName != "mainWidget":
			try:
				lineWidget = currWidget.findChild(QtGui.QLineEdit, "name")
				name = str(lineWidget.text())
				parentList.append(name)
			except: 
				labelWidget = currWidget.findChild(QtGui.QLabel, "arrayItemNumber")
				name = labelWidget.text()
				parentList.append(name)			
			
			## change to next parent
			currWidget = currWidget.parentWidget()
			objectName = currWidget.objectName()

		## remove the deleted value from the global jsonData
		data = self.jsonData
		for i, item in reversed(list(enumerate(parentList))):
			if i != 0:
				data = data[ast.literal_eval(item)]
			else:
				if arrayItem:
					value = int(item[1:-1])
				else:
					value = ast.literal_eval(item)

				del data[value]
		
		## clear the form
		self.clearFormWidget()

		## rebuild the form with new jsonData
		self.buildForm(self.jsonData, False, self.formWidget)

	###############################################################################
	##### addItemAction() #########################################################
	##### runs the approriate add function according to the selected parameter ####
	###############################################################################

	def addItemAction(self, comboBox, indent, parent):
		selection = comboBox.currentText()

		if selection == "Object":
			self.addObject(indent, parent)
		elif selection == "Attribute":
			self.addAttribute(indent, parent)
		elif selection == "Array":
			self.addArray(indent, parent)
		else:
			return

		self.updateJsonData()

	################################################################
	##### checkIndent() ############################################
	##### check if indent is needed, set its size and return it ####
	################################################################

	def checkIndent(self, indent):
		indentItem = QtGui.QLabel("")

		if indent:
			indentItem.setMinimumSize(30, 20)
		else:
			indentItem.setMinimumSize(1, 20)
		return indentItem

	#############################################
	##### addAttribte() #########################
	##### add a new Attribute row to the form ###
	#############################################

	def addAttribute(self, indent, parent):
		layout = parent.layout()
		indentItem = self.checkIndent(indent)
		attrWidget = self.createAttributeRow('"New Attribute"', '"Value"', parent)
		self.linkDeleteButton(attrWidget, False)
		layout.addRow(indentItem, attrWidget)

	#############################################################
	##### addArray() ############################################
	##### add a new Array row to the form and its first value ###
	#############################################################

	def addArray(self, indent, parent):
		layout = parent.layout()
		indentItem = self.checkIndent(indent)

		array = []
		arrayWidget = self.createArrayRow('"New Array"', array, parent)
		arrayButton = arrayWidget.findChild(QtGui.QPushButton, "addButton")
		arrayButton.clicked.connect(partial(self.addArrayValue, arrayWidget))

		self.linkDeleteButton(arrayWidget, False)
		layout.addRow(indentItem, arrayWidget)
		self.addArrayValue(arrayWidget)

	###############################################
	##### addArrayValue() #########################
	##### add a new Array value row to the form ###
	###############################################

	def addArrayValue(self, parent):
		layout = parent.layout()

		indentItem = QtGui.QLabel("")
		indentItem.setMaximumSize(40, 20)

		arrayItemNumber = len(parent.findChildren(QtGui.QWidget, "arrayItemWidget"))
		arrayItemWidget = self.createArrayItemRow('"New Array Item"', arrayItemNumber, parent)
		self.linkDeleteButton(arrayItemWidget, True)
		
		layout.addRow(indentItem, arrayItemWidget)
		self.updateJsonData()

	###############################################
	##### addAObject() ############################
	##### add a new Object value row to the form ##
	###############################################

	def addObject(self, indent, parent):
		layout = parent.layout()

		indentItem = self.checkIndent(indent)

		objectWidget = self.createObjectRow('"New Object"', parent)
		objectComboBox = objectWidget.findChild(QtGui.QComboBox, "addCombo")
		objectButton = objectWidget.findChild(QtGui.QPushButton, "addButton")
		objectButton.clicked.connect(partial(self.addItemAction, objectComboBox, True, objectWidget))

		self.linkDeleteButton(objectWidget, False)
		layout.addRow(indentItem, objectWidget)

	##################################################################
	##### clearFormWidget() ##########################################
	##### clears the form widget so it can update without clashing ###
	##################################################################

	def clearFormWidget(self):
		self.contentLayout.removeWidget(self.formWidget)
		sip.delete(self.formWidget)

		self.formWidget = QtGui.QWidget()
		self.formWidget.setObjectName("mainWidget")
		self.formLayout = QtGui.QFormLayout(self.formWidget)

		gridWidget = QtGui.QFrame()

		gridLayout = QtGui.QGridLayout()
		gridLayout.setMargin(0)

		## the combo box
		self.comboBox = QtGui.QComboBox()
		self.comboBox.addItem("Object")
		self.comboBox.addItem("Attribute")
		self.comboBox.addItem("Array")

		addButton = QtGui.QPushButton("ADD")
		addButton.clicked.connect(partial(self.addItemAction, self.comboBox, False, self.formWidget))
		addButton.setMaximumSize(40,25)

		spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

		gridLayout.addWidget(self.comboBox, 0, 1)
		gridLayout.addWidget(addButton, 0, 2)
		gridLayout.addItem(spacerItem, 0, 3)

		gridWidget.setLayout(gridLayout)

		self.formLayout.addRow(gridWidget)
		self.contentLayout.addWidget(self.formWidget)

	##################################################################
	##### linkDeleteButton() #########################################
	##### link the rows delete button the associated row widget ######
	##################################################################

	def linkDeleteButton(self, widget, arrayItem):
		delButton = widget.findChild(QtGui.QPushButton, "delButton")
		delButton.clicked.connect(partial(self.deleteItem, widget, arrayItem))

	####################################################
	##### createObjectRow() ############################
	##### creates the interface for an Object Row ######
	####################################################

	def createObjectRow(self, itemName, parent):
		formWidget = QtGui.QFrame()
		formWidget.setObjectName("objectWidget")

		formLayout = QtGui.QFormLayout(formWidget)
		formLayout.setMargin(0)

		gridWidget = QtGui.QFrame()

		gridLayout = QtGui.QGridLayout()
		gridLayout.setMargin(0)

		button = QtGui.QPushButton("DEL")
		button.setMaximumSize(35,25)
		button.setObjectName("delButton")

		label = QtGui.QLabel("Object")
		label.setAlignment(QtCore.Qt.AlignCenter)
		label.setStyleSheet("QLabel { background-color: cyan; color : black; border: 1px solid black; border-radius: 5px;}")
		label.setMinimumSize(50, 25)
		label.setMaximumSize(50, 25)
		label.setObjectName("typeValue")

		lineEdit = QtGui.QLineEdit()
		lineEdit.setText(itemName)
		lineEdit.setMaximumSize(100, 25)
		lineEdit.setObjectName("name")
		lineEdit.textChanged.connect(partial(commands.formEvent, self.parent))

		comboBox = QtGui.QComboBox()
		comboBox.addItem("Object")
		comboBox.addItem("Attribute")
		comboBox.addItem("Array")
		comboBox.setObjectName("addCombo")

		addButton = QtGui.QPushButton("ADD")
		addButton.setMaximumSize(40,25)
		addButton.setObjectName("addButton")

		spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

		gridLayout.addWidget(label, 0, 1)
		gridLayout.addWidget(button, 0, 2)
		gridLayout.addWidget(lineEdit, 0, 3)
		gridLayout.addWidget(comboBox, 0, 4)
		gridLayout.addWidget(addButton, 0, 5)
		gridLayout.addItem(spacerItem, 0, 6)

		gridWidget.setLayout(gridLayout)
		gridWidget.setParent(formWidget)

		formLayout.addRow(gridWidget)
		formWidget.setParent(parent)

		return formWidget
	
	#######################################################
	##### createAttributeRow() ############################
	##### creates the interface for an Attribute Row ######
	#######################################################

	def createAttributeRow(self, attrName, attrValue, parent):
		gridWidget = QtGui.QFrame()
		gridWidget.setObjectName("attrWidget")

		gridLayout = QtGui.QGridLayout()
		gridLayout.setMargin(0)

		label = QtGui.QLabel("Attribute")
		label.setAlignment(QtCore.Qt.AlignCenter)
		label.setStyleSheet("QLabel { background-color: magenta; color : black; border: 1px solid black; border-radius: 5px;}")
		label.setMinimumSize(75, 25)
		label.setMaximumSize(75, 25)
		label.setObjectName("typeLabel")

		button = QtGui.QPushButton("DEL")
		button.setMaximumSize(35,25)
		button.setObjectName("delButton")

		lineEdit = QtGui.QLineEdit()
		lineEdit.setText(attrName)
		lineEdit.setMaximumSize(100,25)
		lineEdit.setObjectName("name")
		lineEdit.textChanged.connect(partial(commands.formEvent, self.parent))

		label2 = QtGui.QLabel(":")
		label2.setMinimumSize(10,20)
		label2.setMaximumSize(10,20)

		lineEdit2 = QtGui.QLineEdit()
		lineEdit2.setText(attrValue)
		lineEdit2.setMinimumSize(300,25)
		lineEdit2.setMaximumSize(300,25)
		lineEdit2.setObjectName("attrValue")
		lineEdit2.textChanged.connect(partial(commands.formEvent, self.parent))

		spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

		gridLayout.addWidget(label, 0, 1)
		gridLayout.addWidget(button, 0, 2)
		gridLayout.addWidget(lineEdit, 0, 3)
		gridLayout.addWidget(label2, 0, 4)
		gridLayout.addWidget(lineEdit2, 0, 5)
		gridLayout.addItem(spacerItem, 0, 6)

		gridWidget.setLayout(gridLayout)
		gridWidget.setParent(parent)

		return gridWidget

	##################################################################
	##### createArrayRow() ###########################################
	##### creates the interface for an Array Row and its values ######
	##################################################################

	def createArrayRow(self, arrayName, array, parent):
		formWidget = QtGui.QFrame()
		formWidget.setObjectName("arrayWidget")

		formLayout = QtGui.QFormLayout(formWidget)
		formLayout.setMargin(0)

		gridWidget = QtGui.QFrame()
		gridWidget.setObjectName("arrayGrid")

		gridLayout = QtGui.QGridLayout()
		gridLayout.setMargin(0)

		button = QtGui.QPushButton("DEL")
		button.setMaximumSize(35,25)
		button.setObjectName("delButton")

		label = QtGui.QLabel("Array")
		label.setAlignment(QtCore.Qt.AlignCenter)
		label.setStyleSheet("QLabel { background-color: lime; color : black; border: 1px solid black; border-radius: 5px;}")
		label.setMinimumSize(50, 25)
		label.setMaximumSize(50, 25)
		label.setObjectName("typeLabel")

		lineEdit = QtGui.QLineEdit()
		lineEdit.setText(arrayName)
		lineEdit.setMaximumSize(100, 25)
		lineEdit.setObjectName("name")
		lineEdit.textChanged.connect(partial(commands.formEvent, self.parent))

		addButton = QtGui.QPushButton("Add Value")
		addButton.setMaximumSize(70,25)
		addButton.setObjectName("addButton")

		spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

		gridLayout.addWidget(label, 0, 1)
		gridLayout.addWidget(button, 0, 2)
		gridLayout.addWidget(lineEdit, 0, 3)
		gridLayout.addWidget(addButton, 0, 4)
		gridLayout.addItem(spacerItem, 0, 5)

		gridWidget.setLayout(gridLayout)
		gridWidget.setParent(formWidget)

		formLayout.addRow(gridWidget)
		formWidget.setParent(parent)

		indentItem = QtGui.QLabel("")
		indentItem.setMaximumSize(40, 20)

		for i, item in enumerate(array):
			itemValue = json.dumps(item)
			arrayItemWidget = self.createArrayItemRow(itemValue, i, formWidget)

			self.linkDeleteButton(arrayItemWidget, True)
			formLayout.addRow(indentItem, arrayItemWidget)

		return formWidget

	####################################################
	##### createArrayItemRow() #########################
	##### creates the interface for an Array Item Row ##
	####################################################

	def createArrayItemRow(self, itemValue, itemNum, parent):
		gridWidget = QtGui.QWidget()
		gridWidget.setObjectName("arrayItemWidget")

		gridLayout = QtGui.QGridLayout()
		gridLayout.setMargin(0)

		indent = QtGui.QLabel()
		indent.setMaximumSize(25,25)

		label = QtGui.QLabel("["+str(itemNum)+"]")
		label.setAlignment(QtCore.Qt.AlignCenter)
		label.setMinimumSize(35,25)
		#label.setMaximumSize(35,25)
		label.setStyleSheet("QLabel { background-color: green; color : white; border: 1px solid black; border-radius: 5px;}")
		label.setObjectName("arrayItemNumber")

		lineEdit = QtGui.QLineEdit()
		lineEdit.setText(itemValue)
		lineEdit.setMaximumSize(300,25)
		lineEdit.setObjectName("arrayItemValue")
		lineEdit.textChanged.connect(partial(commands.formEvent, self.parent))

		button = QtGui.QPushButton("DEL")
		button.setMaximumSize(35,25)
		button.setObjectName("delButton")

		spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

		gridLayout.addWidget(indent, 0, 1)
		gridLayout.addWidget(label, 0, 2)
		gridLayout.addWidget(lineEdit, 0, 3)
		gridLayout.addWidget(button, 0, 4)
		gridLayout.addItem(spacerItem, 0, 5)

		gridWidget.setLayout(gridLayout)
		gridWidget.setParent(parent)

		return gridWidget