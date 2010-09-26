all: ui_sessiondialog.py

clean:
	rm *.pyc ui_*.py

ui_sessiondialog.py : sessiondialog.ui
	pyuic4 sessiondialog.ui > ui_sessiondialog.py 
