#! /usr/bin/env python
# -*- coding: utf-8 -*-

#########################################################
############ JSON Editor ################################
############# Erin Terre ################################
#########################################################
### compareWindow.py - ##################################
## Contains the interface for the comparison window #####
## and functions neccessary for comparing 2 JSON files ##
#########################################################

import commands
import json
import sys
from PyQt4 import QtCore, QtGui
from functools import partial


class CompareWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Compare JSON Files")
        self.resize(800, 550)

        self.centralwidget = QtGui.QWidget()

        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 781, 511))

        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)

        self.leftVerticalLayout = QtGui.QVBoxLayout()

        self.leftLabel = QtGui.QLabel(self.horizontalLayoutWidget)
        self.leftLabel.setText("File 1")
        self.leftLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.leftTextEditor = QtGui.QTextEdit()
        self.leftTextEditor.setText("{}")

        ## add to left layout
        self.leftVerticalLayout.addWidget(self.leftLabel)
        self.leftVerticalLayout.addWidget(self.leftTextEditor)

        self.horizontalLayout.addLayout(self.leftVerticalLayout)

        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem)

        self.rightVerticalLayout = QtGui.QVBoxLayout()

        self.rightLabel = QtGui.QLabel(self.horizontalLayoutWidget)
        self.rightLabel.setText("File 2")
        self.rightLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.rightTextEditor = QtGui.QTextEdit()
        self.rightTextEditor.setText("{}")

        ## set both text editors to read only
        self.leftTextEditor.setReadOnly(True)
        self.rightTextEditor.setReadOnly(True)

        ## add to right layout
        self.rightVerticalLayout.addWidget(self.rightLabel)
        self.rightVerticalLayout.addWidget(self.rightTextEditor)

        self.horizontalLayout.addLayout(self.rightVerticalLayout)

        self.setCentralWidget(self.centralwidget)

        ## Create main menu
        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu('File')

        ## Add open files button to file menu 
        ## to allow user to run another comparison without closing the window
        openFilesButton = QtGui.QAction('Open Files', self)
        openFilesButton.setShortcut('Ctrl+O')
        openFilesButton.setStatusTip('Open JSON files')
        openFilesButton.triggered.connect(partial(commands.compareFiles_Open, self))
        fileMenu.addAction(openFilesButton)

    def updateLeftTextView(self, jsonData):
        self.leftTextEditor.setText(json.dumps(jsonData, indent=4))

    def updateRightTextView(self, jsonData):
        self.rightTextEditor.setText(json.dumps(jsonData, indent=4))

    ############################################
    ##### compareFiles_Hilight() ###############
    ##### function to compare two json files ###
    ############################################

    def compareFiles_Hilight(self, leftTextEditor, rightTextEditor):
        leftCursor = leftTextEditor.textCursor()
        rightCursor = rightTextEditor.textCursor()

        ## hilight color
        format = QtGui.QTextCharFormat()
        format.setBackground(QtGui.QBrush(QtGui.QColor("yellow")))

        leftCursor.setPosition(QtGui.QTextCursor.Start)
        rightCursor.setPosition(QtGui.QTextCursor.Start)
        leaveLoop = False

        while leaveLoop != True:
            leftCursor.select(QtGui.QTextCursor.LineUnderCursor)
            rightCursor.select(QtGui.QTextCursor.LineUnderCursor)

            if leftCursor.atEnd() and rightCursor.atEnd() != True:
                rightCursor.mergeCharFormat(format)
                rightCursor.movePosition(QtGui.QTextCursor.Down)

            elif leftCursor.atEnd() != True and rightCursor.atEnd():
                leftCursor.mergeCharFormat(format)
                leftCursor.movePosition(QtGui.QTextCursor.Down)

            elif leftCursor.atEnd() and rightCursor.atEnd():
                leaveLoop = True

            else:
                if self.compareFiles_LineCheck(leftCursor.selectedText(), rightCursor.selectedText()):
                    leftCursor.mergeCharFormat(format)
                    rightCursor.mergeCharFormat(format)

                leftCursor.movePosition(QtGui.QTextCursor.Down)
                rightCursor.movePosition(QtGui.QTextCursor.Down)

    ############################################
    ##### compareFiles_LineCheck() #############
    ##### compares selected lines ##############
    ############################################

    def compareFiles_LineCheck(self, leftLine, rightLine):
        if leftLine != rightLine:
            return True
        else:
            return False
