#! /usr/bin/env python
# -*- coding: utf-8 -*-

#####################################################
############ JSON Editor ############################
############# Erin Terre ############################
#####################################################
### commands.py - ###################################
## Contains functions used by multiple interfaces ###
#####################################################

import ast
import json
import ntpath
import popups
import sys
from PyQt4 import QtGui, QtCore
from collections import OrderedDict
from functools import partial
from compareWindow import CompareWindow

############################################
##### getJsonData() ########################
##### return jsonData ######################
############################################

def getJsonData(jsonString):
    return json.loads(jsonString, object_pairs_hook=OrderedDict)

###########################################
##### mainWindow_Open() ###################
##### open file in mainWindow #############
###########################################

def mainWindow_New(window):
	if window.update:
		## if changes have been made check if user wants to save first
		popups.showSaveFile(window)

	window.form.clearFormWidget()
	window.tab.clearTextView()
	window.tab.clearTreeView()

	window.setWindowTitle("JSON Text - New Document")

###########################################
##### mainWindow_Open() ###################
##### open file in mainWindow #############
###########################################

def mainWindow_Open(window):
	if window.update:
		## if changes have been made check if user wants to save first
		popups.showSaveFile(window)

	try:
		mainName, jsonData = openFile(window, "Open File")
	except TypeError, NameError:
		return

	windowName = "JSON Text - " + mainName
	window.setWindowTitle(windowName)
	
	## build form from loaded JSON file
	window.form.clearFormWidget()
	window.form.buildForm(jsonData, False, window.form.formWidget)
	window.form.jsonData = jsonData
	
	## build text and tree from loaded JSON file
	window.tab.clearTreeView()
	window.tab.updateTabs(jsonData)

	window.update = True

###########################################
##### openFile() ##########################
##### basic open function #################
###########################################

def openFile(window, dialogText):
	filePath = QtGui.QFileDialog.getOpenFileName(window, dialogText, '', 'JSON Files (*.json)')

	## check if canceled
	if not filePath:
		return

	stringData = open(filePath).read()
	fileName = ntpath.basename(str(filePath))

	## run checkJsonData for invalid syntax
	if checkJsonData(str(stringData)):
		jsonData = getJsonData(str(stringData))
		return fileName, jsonData
	else: 
		popups.showInvalidSyntax()

############################################
##### checkJsonData() ######################
##### check if jsonData is valid ###########
############################################

def checkJsonData(jsonString):
    try:
        json.loads(jsonString, object_pairs_hook=OrderedDict)
    except ValueError, e:
        return False
    return True

###########################################
##### mainWindow_Save() ###################
##### save file in mainWindow #############
###########################################

def mainWindow_Save(window):
	try:
		## if changes were recently made in the Tab section then update Form View with those changes
		if window.lastEvent == "Tab":
			updateFormView(window)

		jsonData = window.form.updateJsonData()
		filePath = QtGui.QFileDialog.getSaveFileName(window, "Save File", '', 'JSON Files (*.json)')

		## check if canceled
		if not filePath:
			return

		with open(filePath, 'w') as outputFile:
			json.dump(jsonData, outputFile, indent=4)

		window.update = False

	except NameError:
		return

#############################################
##### textEvent() ###########################
##### set the mainWindows lastEvent to Tab ##
#############################################

def textEvent(window):
	window.lastEvent = "Tab"

##############################################
##### formEvent() ############################
##### set the mainWindows lastEvent to Form ##
##############################################

def formEvent(window):
	window.lastEvent = "Form"

#####################################################
##### updateTabView() ###############################
##### update both Tabs with the data from the Form ##
#####################################################

def updateTabView(window):
	jsonData = window.form.updateJsonData()

	if jsonData:
		## build text and tree for jsonData pulled for the Form
		window.tab.clearTreeView()
		window.tab.updateTabs(jsonData)
		window.update = True
		window.lastEvent = "Tab"
	else:
		popups.showInvalidSyntax()
		return

########################################################
##### updateFormView() #################################
##### update the Form with the data from the Text Tab ##
########################################################

def updateFormView(window):
	stringData = getStringData(window.tab.textEditor)

	if checkJsonData(str(stringData)):
		jsonData = getJsonData(str(stringData))

		window.form.clearFormWidget()
		window.form.buildForm(jsonData, False, window.form.formWidget)
		window.form.jsonData = jsonData
		window.update = True
		window.lastEvent = "Form"
	else:
		popups.showInvalidSyntax()

###############################################
##### getStringData() #########################
##### get the string data from a text editor ##
###############################################

def getStringData(textEditor):
	stringData = textEditor.toPlainText()
	return stringData

#############################################
##### compareFiles_Open() ###################
##### open two files in compareWindow #######
#############################################

def compareFiles_Open(window):
	try:
		leftName, leftJsonData = openFile(window, "Open File 1")
		rightName, rightJsonData = openFile(window, "Open File 2")
	except TypeError, NameError:
		return

	updateLabel(window.leftLabel, leftName)
	updateLabel(window.rightLabel, rightName)

	window.updateLeftTextView(leftJsonData)
	window.updateRightTextView(rightJsonData)

	## run comparison function to highlight differences
	CompareWindow.compareFiles_Hilight(window, window.leftTextEditor, window.rightTextEditor)

############################################
##### updateLabel() ########################
##### set label name #######################
############################################

def updateLabel(label, fileName):
    label.setText(fileName)