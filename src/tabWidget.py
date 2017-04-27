#! /usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################################
############ JSON Editor ##################################################
############# Erin Terre ##################################################
###########################################################################
### tabWidget.py - ########################################################
## Contains the interface for the tab widget and its text and tree tabs ###
## along with the functions neccessary to generate/update the tabs ########
###########################################################################

import commands
import json
import popups
import sip
import sys
from PyQt4 import QtGui, QtCore
from functools import partial
from collections import OrderedDict


class Tab(QtGui.QTabWidget):
	def __init__(self, parent):
		QtGui.QTabWidget.__init__(self, parent)
		self.parent = parent
		self.initUI(parent)

	def initUI(self, parent):
		self.setParent(parent)
		self.setObjectName("Tab Widget")
		self.setMinimumSize(550,650)

		self.tab1 = QtGui.QWidget()
		self.tab2 = QtGui.QWidget()

		self.addTab(self.tab1, "Text View")
		self.addTab(self.tab2, "Tab View")
		self.tab1UI()
		self.tab2UI()

		self.currentChanged.connect(self.onChange)

	#########################################
	##### tab1UI() ##########################
	##### the interface for the Text Tab ####
	#########################################

	def tab1UI(self):
		self.textLayout = QtGui.QHBoxLayout()
		self.textEditor = QtGui.QTextEdit()
		self.textEditor.setText("{}")
		self.textEditor.textChanged.connect(partial(commands.textEvent, self.parent))
		self.textLayout.addWidget(self.textEditor)
		self.tab1.setLayout(self.textLayout)
	
	#########################################
	##### tab2UI() ##########################
	##### the interface for the Tree Tab ####
	#########################################

	def tab2UI(self):
		self.treeLayout = QtGui.QHBoxLayout()
		self.treeWidget = QtGui.QTreeWidget()
		self.treeWidget.setHeaderHidden(True)
		self.treeLayout.addWidget(self.treeWidget)
		self.tab2.setLayout(self.treeLayout)

	#############################################
	##### updateTabs() ##########################
	##### update both tabs with the jsonData ####
	#############################################

	def updateTabs(self, jsonData):
		self.updateTextView(jsonData)
		self.updateTreeView(jsonData)

	################################################
	##### updateTextView() #########################
	##### update the text tab with the jsonData ####
	################################################

	def updateTextView(self, jsonData):
		self.textEditor.setText(json.dumps(jsonData, indent=4))

	#########################################
	##### clearTextView() ###################
	##### clears the text tab completely ####
	#########################################

	def clearTextView(self):
		self.textEditor.setText("{}")

	################################################
	##### updateTreeView() #########################
	##### update the tree tab with the jsonData ####
	################################################

	def updateTreeView(self, jsonData):
		self.treeView_BuildTree(jsonData, self.treeWidget)

	#########################################
	##### clearTreeView() ###################
	##### clears the tree tab completely ####
	#########################################

	def clearTreeView(self):
		self.treeLayout.removeWidget(self.treeWidget)
		sip.delete(self.treeWidget)

		self.treeWidget = QtGui.QTreeWidget()
		self.treeWidget.setHeaderHidden(True)
		self.treeLayout.addWidget(self.treeWidget)

	#################################################################################################
	##### onChange() ################################################################################
	##### update the tree tab with the jsonData from the text tab when switching to the tree tab ####
	#################################################################################################

	def onChange(self):
		if self.currentIndex() == 1:
			stringData = commands.getStringData(self.textEditor)

			## check if the jsonData is still valid, before updating the tree
			if commands.checkJsonData(str(stringData)):
				jsonData = commands.getJsonData(str(stringData))

				self.clearTreeView()
				self.updateTreeView(jsonData)
			else:
				popups.showInvalidSyntax()
				return

	############################################
	##### treeView_BuildTree() #################
	##### main tree building function ##########
	############################################

	def treeView_BuildTree(self, jsonData, parent):
		if len(jsonData) > 0:
			for item in jsonData:
				if type(jsonData.get(item)) is OrderedDict:
					newParent = self.treeView_AddParent(parent, json.dumps(item), QtCore.Qt.cyan, QtCore.Qt.black)
					newJsonData = jsonData[item]
					self.treeView_BuildTree(newJsonData, newParent)
				elif type(jsonData.get(item)) is list:
					arrayString = json.dumps(jsonData.get(item))
					newParent = self.treeView_AddParent(parent, json.dumps(item), QtCore.Qt.green, QtCore.Qt.black)
					newJsonData = jsonData[item]
					self.treeView_AddArrayItems(newParent, newJsonData)
				else:
					value = json.dumps(jsonData.get(item))
					title = json.dumps(item) + " : " + value
					self.treeView_AddChild(parent, title, QtCore.Qt.magenta, QtCore.Qt.black)
		else:
			return

	##############################################
	##### treeView_AddParent() ###################
	##### add a parent to tree ###################
	##############################################

	def treeView_AddParent(self, parent, title, bgColor, txtColor):
		item = QtGui.QTreeWidgetItem(parent, [title])
		item.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
		item.setExpanded (True)
		item.setBackgroundColor(0, bgColor)
		item.setTextColor(0, txtColor)
		return item

	############################################
	##### treeView_AddChild() ##################
	##### add child to parent ##################
	############################################

	def treeView_AddChild(self, parent, title, bgColor, txtColor):
		item = QtGui.QTreeWidgetItem(parent, [title])
		item.setBackgroundColor(0, bgColor)
		item.setTextColor(0, txtColor)
		return item

	############################################
	##### treeView_AddArrayItems() #############
	##### add array children to array parent ###
	############################################

	def treeView_AddArrayItems(self, parent, jsonData):
		for i, item in enumerate(jsonData):
			self.treeView_AddChild(parent, json.dumps(item), QtCore.Qt.darkGreen, QtCore.Qt.white)