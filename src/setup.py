from distutils.core import setup
import py2exe
setup(windows=[{"script":"__init__.py"}], 
	options={"py2exe": {"includes":["sip"] , "dll_excludes": ["MSVCP90.dll", "HID.DLL", "w9xpopen.exe"]}}
	)