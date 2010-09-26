# coding=utf-8
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QDialog, QTableWidget, QTableWidgetItem
from PyQt4.QtCore import QVariant
from ui_sessiondialog import Ui_Dialog
import sqlite3

class SessionDialog( QDialog ):
	def __init__( self ):
		QDialog.__init__( self )

		self.ui = Ui_Dialog()
		self.ui.setupUi( self )

		self.ui.cancelButton.clicked.connect( self.reject )
		self.ui.okButton.clicked.connect( self.accept )
		self.ui.addButton.clicked.connect( self.addExerciseItem )
		self.ui.deleteButton.clicked.connect( self.deleteItem )

		self.cb = self.ui.exerciseComboBox
		self.sb = self.ui.weightSpinBox

		self.table = self.ui.exerciseTable

		self.con = sqlite3.connect("data/db")
		self.con.isolation_level = None
		self.cur = self.con.cursor()

		self.dbExercises()

	def insertItem( self, item ):
		row = self.table.rowCount()
		self.table.insertRow( row )

		for i in range( len( item ) ):
			self.table.setItem(
				row,
				i,
				QTableWidgetItem( item[i] )
			)

	def addExerciseItem( self ):
		res = []
		res.append( self.cb.itemData( self.cb.currentIndex() ).toString() )
		res.append( self.cb.currentText() )
		res.append( str( self.sb.value() ) )
		self.insertItem( res )

	def deleteItem( self ):
		pass
	
	def dbExercises( self ):
		self.cur.execute("SELECT * FROM 'exercise' ORDER BY 'name';")
		exercises = self.cur.fetchall()
		for e in exercises:
			self.cb.addItem( e[1], e[0] )
