# coding=utf-8
from PyQt4 import QtGui
from PyQt4.QtGui import QDialog
from ui_sessiondialog import Ui_Dialog

class SessionDialog( QDialog ):
	def __init__( self ):
		QDialog.__init__( self )

		self.ui = Ui_Dialog()
		self.ui.setupUi( self )

		self.ui.cancelButton.clicked.connect( self.reject )
		self.ui.okButton.clicked.connect( self.accept )

		self.ui.exerciseComboBox.addItems(
			[
				'Butterfly',
				'Liegestütz'
			]
		)

