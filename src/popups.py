#! /usr/bin/env python
# -*- coding: utf-8 -*-

################################################################
############ JSON Editor #######################################
############# Erin Terre #######################################
################################################################
### popups.py - ################################################
## Contains the functions for popups used in the application ###
################################################################

import commands
from PyQt4 import QtGui, QtCore
from compareWindow import CompareWindow


###########################################
#### showInvalidSyntax() ##################
#### display invalid JSON syntax error ####
###########################################

def showInvalidSyntax():
	msg = QtGui.QMessageBox()
	msg.setIcon(QtGui.QMessageBox.Critical)
	msg.setText("The current\selected JSON file is invalid.\nPlease check the syntax and try again.")
	msg.setWindowTitle("ERROR")
	msg.exec_()

###########################################
#### showSaveFile() #######################
#### display save message #################
###########################################

def showSaveFile(window):
	saveMsg = "Would you like to save before you continue?"
	reply = QtGui.QMessageBox.question(window, 'Message', saveMsg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

	if reply == QtGui.QMessageBox.Yes:
		commands.mainWindow_Save(window)
	else: 
		return

###########################################
#### showCompareWindow() ##################
#### display compare window ###############
###########################################

def showCompareWindow(window):
	window.compareWindow = CompareWindow()
	window.compareWindow.show()
	commands.compareFiles_Open(window.compareWindow)
