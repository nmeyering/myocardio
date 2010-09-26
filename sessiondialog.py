# coding=utf-8
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QDialog, QTableWidget, QTableWidgetItem
from PyQt4.QtCore import QVariant, QDateTime
from ui_sessiondialog import Ui_Dialog
import sqlite3

class SessionDialog( QDialog ):
	def __init__( self ):
		QDialog.__init__( self )

		self.ui = Ui_Dialog()
		self.ui.setupUi( self )

		self.ui.cancelButton.clicked.connect( self.reject )
		self.ui.okButton.clicked.connect( self.commit )
		self.ui.addButton.clicked.connect( self.addExerciseItem )
		self.ui.deleteButton.clicked.connect( self.deleteItem )

		self.cb = self.ui.exerciseComboBox
		self.sb = self.ui.weightSpinBox
		self.table = self.ui.exerciseTable

		self.ui.dateTimeEdit.setDateTime( QDateTime.currentDateTime() )

		self.con = sqlite3.connect("data/db")
		self.con.row_factory = sqlite3.Row
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
		exes = self.cur.fetchall()
		for e in exes:
			self.cb.addItem( e['name'], e['id'] )
	
	def commit( self ):
		weight = self.ui.bodyweightSpinBox.value()
		date = str( self.ui.dateTimeEdit.dateTime().toString("yyyy-MM-dd hh:mm") )
		try:
			self.cur.execute("INSERT INTO 'session' ('weight', 'date') VALUES(?,?)", (weight, date))
			session_id = self.cur.lastrowid
			for row in range( self.table.rowCount() ):
				self.cur.execute("INSERT INTO 'completed_exercise' ('session_id', 'exercise_id', 'weight') VALUES(?,?,?)",
					(
						session_id,
						int( self.table.item(row, 0).text() ),
						float( self.table.item(row, 2).text() )
					)
				)
		except sqlite3.Error as e:
			print("An error occurred:", e.args[0])
		self.accept()
