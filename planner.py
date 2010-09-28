#!/usr/bin/python3
import sys, os
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QDialog, QApplication
from sessiondialog import SessionDialog

def main():
	os.system("./generate_weight_plot")
	app = QApplication( sys.argv )
	sdialog = SessionDialog()
	sdialog.show()

	sys.exit( app.exec_() )

if __name__ == "__main__":
	main()
