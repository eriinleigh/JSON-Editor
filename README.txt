------------------ JSON Text ------------------------
------------ Created by: Erin Terre -----------------
--------- Last Update: 04 - 18 - 2017 ---------------
------------- Python 2.7 && PyQt4 -------------------

This application allows the user to:
	- Load/View JSON files into a form interface, text editor, and a tree view
	- Edit JSON files in a form interface or text editor
	- Create JSON files in form interface or text editor
	- Save JSON files

	- Compare 2 JSON files and highlight their differences in a seperate window

USAGE: 
	- for windows: run JSONEditor.exe located in dist folder
	- python __init__.py via command line from the src folder

Features to come:
	- Comparison Window - highlight changes made with different color
	- Comparision Window - automatically update highlighting on text edit

Updates made as of 2/22/17:
	- Added an interactive form interface to the main window with color coded parameters. The form can be used to create JSON files from scratch or generated from a loaded JSON file. The form also allows the user to easily add, remove or edit JSON parameters.
	- Added a tab widget that has both the text view and tree view in it
	- Removed the option to edit with the tree view 
	- Color coded the tree view to match the form interface
	- Added a New File button to the main window
	- Added buttons to update the tabs using the form data and vice versa
	- Added error handeling to catch JSON syntax errors when creating/editing 
	- Removed the option to edit JSON files while comparing
	- Changed comparision hilight color to yellow
	- Compare Files button now immediately prompts the user to select files
	- User may open multiple Compare File windows at a time
	- User may compare new files without closing the current Comparison Window
	- Application title now updates with file name loaded

Files: 
	> __init__.py
		- the main script :: starts application

	> mainWindow.py
		- Contains the interface for the main window

	> tabWidget.py
		- Contains the interface for the tab widget and its text and tree tabs along with the functions neccessary to generate/update the tabs

	> formWidget.py
		- Contains the interface for the form widget and the functions neccessary to generating/adding/deleting form items

	> compareWindow.py
		- Contains the interface for the comparison window and functions neccessary for comparing 2 JSON files

	> commands.py
		- Contains functions used by multiple interfaces

	> popups.py
		- Contains the functions for popups used in the application

	> setup.py
		- script used to package the application for windows as a .exe