# coding=utf-8
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QDialog, QTableWidget, QTableWidgetItem, QImage, QPixmap, QLabel, QVBoxLayout
from PyQt4.QtCore import QVariant, QDateTime
from ui_sessiondialog import Ui_Dialog
import sqlite3

class SessionDialog( QDialog ):
	def __init__( self ):
		QDialog.__init__( self )

		self.ui = Ui_Dialog()
		self.ui.setupUi( self )

		self.cb = self.ui.exerciseComboBox
		self.sb = self.ui.weightSpinBox
		self.table = self.ui.exerciseTable
		self.splitbox = self.ui.splitplanComboBox

		self.ui.cancelButton.clicked.connect( self.reject )
		self.ui.okButton.clicked.connect( self.commit )
		self.ui.addButton.clicked.connect( self.addExerciseItem )
		self.ui.deleteButton.clicked.connect( self.deleteItem )
		self.splitbox.currentIndexChanged.connect( self.fillSplitTable )
		self.ui.updateButton.clicked.connect( self.fillSplitTable )

		self.ui.dateTimeEdit.setDateTime( QDateTime.currentDateTime() )

		self.weightPlot = QImage( "data/weight_plot.png" )
		self.ui.imageLabel = QLabel()
		self.ui.imageLabel.setPixmap( QPixmap.fromImage( self.weightPlot ) )
		self.ui.scrollArea.setWidget( self.ui.imageLabel )

		self.con = sqlite3.connect( "data/db" )
		self.con.row_factory = sqlite3.Row
		self.con.isolation_level = None
		self.cur = self.con.cursor()

		self.dbExercises()
		self.dbSplit()

		layout = QVBoxLayout(self)
		layout.addWidget(self.ui.tabWidget)

	def insertItem( self, table, item ):
		row = table.rowCount()
		table.insertRow( row )

		for i in range( len( item ) ):
			table.setItem(
				row,
				i,
				QTableWidgetItem( item[i] )
			)

	def addExerciseItem( self ):
		res = []
		res.append( str( self.cb.itemData( self.cb.currentIndex() ) ) )
		res.append( self.cb.currentText() )
		res.append( str( self.sb.value() ) )
		self.insertItem( self.table, res )

	def deleteItem( self ):
		row = self.table.currentRow()
		self.table.removeRow( row )
			
	def clearTable( self, table ):
		for i in range( table.rowCount() ):
			table.removeRow( 0 )
	
	def dbSplit( self ):
		self.cur.execute("SELECT * FROM 'split';")
		split = self.cur.fetchall()
		for s in split:
			self.splitbox.addItem( s['description'], s['id'] )

	def fillSplitTable( self ):
		split_id = self.splitbox.itemData( self.splitbox.currentIndex() )
		try:
			self.cur.execute(
				"SELECT exercise.name, MAX(completed_exercise.weight) maxweight, MAX(session.date) maxdate FROM completed_exercise LEFT JOIN exercise ON exercise.id = completed_exercise.exercise_id LEFT JOIN session ON session.id = completed_exercise.session_id WHERE (exercise.split_id = ? OR exercise.split_id is null) GROUP BY exercise.name ORDER BY maxdate ASC;",
				(split_id,)
			)
			rows = self.cur.fetchall()
		except sqlite3.Error as e:
			print("An error occurred:", e.args[0])

		splitTable = self.ui.splitplanTable

		self.clearTable( splitTable )

		for r in rows:
			self.insertItem( splitTable, [ str(i) for i in list(r) ] )

	def dbExercises( self ):
		self.cur.execute("SELECT * FROM 'exercise' ORDER BY name;")
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
			self.clearTable( self.table )
		except sqlite3.Error as e:
			print("An error occurred:", e.args[0])
