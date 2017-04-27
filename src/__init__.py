#! /usr/bin/env python
# -*- coding: utf-8 -*-


import sys
from PyQt4 import QtGui, QtCore
from mainWindow import Window

if __name__ == '__main__':

	app = QtGui.QApplication(sys.argv)
	window = Window()
	window.show()
	sys.exit(app.exec_())