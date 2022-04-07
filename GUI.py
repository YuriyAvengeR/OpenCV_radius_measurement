# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yura0\Desktop\measurement_system\GUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import sqlite3
from multiprocessing import Process


from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView


class Ui_MainWindow(object):
    db_status = 0
    def __init__(self):
        self.row_count = 0
        self.db_status = 0


    def db_load(self):
        spinBoxValue = self.ComSelectBox_2.value()
        if int(spinBoxValue) is 0:
            sqlite_file = 'C:\\Users\\yura0\\Desktop\\measurement_system\\ObjectDB.db'
            db = sqlite3.connect(sqlite_file)
            sql = db.cursor()
            sql.execute('SELECT COUNT(*) FROM objects')
            self.row_count = sql.fetchone()[0]
            self.TableView.setRowCount(int(self.row_count))

            sql.execute('SELECT Name FROM objects')
            self.db_names = sql.fetchall()
            sql.execute('SELECT Size FROM objects')
            self.db_size = sql.fetchall()
            sql.execute('SELECT Tol FROM objects')
            self.db_tol = sql.fetchall()
            sql.execute('SELECT Comment FROM objects')
            self.db_com = sql.fetchall()
            print(self.db_names)

            i = 0
            while i != self.row_count:
                self.TableView.setItem(i, 0, QTableWidgetItem(f"{self.db_names[i][0]}"))
                self.TableView.setItem(i, 1, QTableWidgetItem(f"{self.db_size[i][0]}"))
                self.TableView.setItem(i, 2, QTableWidgetItem(f"{self.db_tol[i][0]}"))
                self.TableView.setItem(i, 3, QTableWidgetItem(f"{self.db_com[i][0]}"))
                i = i + 1
            db.close()
            self.textBrowser_2.setText('База завантажена успішно!')
            self.__setattr__("db_status", 1)
        else:
            self.spinBoxValue = self.ComSelectBox_2.value()
            self.textBrowser_2.setText(f'{spinBoxValue}')
            if spinBoxValue <= self.row_count:
                ids = int(spinBoxValue) - 1
                self.textBrowser.setText(f'{self.db_names[ids][0]} розміром: {self.db_size[ids][0]} з макс.похибкою: {self.db_tol[ids][0]}')
                print(f"{self.spinBoxValue} {self.row_count}")
            else:
                self.textBrowser_2.setText('Вихід за границі таблиці.')


    def check_name(self):
        try:
            if self.db_status is not 0:
                text_name = self.textEdit.toPlainText()
                text_size = self.textEdit_2.toPlainText()
                text_tol = self.textEdit_3.toPlainText()
                text_comm = self.textEdit_4.toPlainText()
                self.textBrowser_2.setText(f"{text_name} з розміром: {text_size}, макс.похибкою {text_tol}. Коментар: {text_comm}")

                sqlite_file = 'C:\\Users\\yura0\\Desktop\\measurement_system\\ObjectDB.db'
                db = sqlite3.connect(sqlite_file)
                sql = db.cursor()
                sql.execute(f'SELECT Name FROM objects WHERE Name = "{text_name}"')

                if sql.fetchone() is None:
                    sql.execute(f'INSERT INTO objects VALUES (?, ?, ?, ?, ?)', (0, text_name, text_size, text_tol,text_comm))
                    db.commit()
                    print(f"{text_name} з розміром: {text_size}, макс.похибкою {text_tol}. Коментар: {text_comm}")
                    sql.execute('SELECT COUNT(*) FROM objects')
                    self.row_count = sql.fetchone()[0]
                    self.TableView.setRowCount(int(self.row_count))

                    sql.execute('SELECT Name FROM objects')
                    self.db_names = sql.fetchall()
                    sql.execute('SELECT Size FROM objects')
                    self.db_size = sql.fetchall()
                    sql.execute('SELECT Tol FROM objects')
                    self.db_tol = sql.fetchall()
                    sql.execute('SELECT Comment FROM objects')
                    self.db_com = sql.fetchall()
                    print(self.db_names)

                    i = 0
                    while i != self.row_count:
                        self.TableView.setItem(i, 0, QTableWidgetItem(f"{self.db_names[i][0]}"))
                        self.TableView.setItem(i, 1, QTableWidgetItem(f"{self.db_size[i][0]}"))
                        self.TableView.setItem(i, 2, QTableWidgetItem(f"{self.db_tol[i][0]}"))
                        self.TableView.setItem(i, 3, QTableWidgetItem(f"{self.db_com[i][0]}"))
                        i = i + 1
                    db.close()
                else:
                    self.textBrowser_2.setText('Такий виріб уже існує!')
                    print('Такий виріб уже існує!')
            elif self.db_status is 0:
                self.textBrowser_2.setText("База не завантажена!")
        except:
            self.textBrowser_2.setText("DB load error!")






    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 600))
        MainWindow.setMaximumSize(QtCore.QSize(1000, 600))
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("QWidget{\n"
"background-color:#4D4D4D;\n"
"}")
        self.centralwidget.setObjectName("centralwidget")
        self.CameraLabel = QtWidgets.QLabel(self.centralwidget)
        self.CameraLabel.setGeometry(QtCore.QRect(40, 30, 500, 500))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CameraLabel.sizePolicy().hasHeightForWidth())
        self.CameraLabel.setSizePolicy(sizePolicy)
        self.CameraLabel.setStyleSheet("QLabel{\n"
"background-color: black;\n"
"border-radius: 5px;\n"
"}")
        self.CameraLabel.setText("")
        self.CameraLabel.setPixmap(QtGui.QPixmap("C:\\Users\\yura0\\Desktop\\output.jpg"))
        self.CameraLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.CameraLabel.setObjectName("CameraLabel")

        #TABLE
        self.TableView = QtWidgets.QTableWidget(self.centralwidget)
        self.TableView.setColumnCount(4)
        self.TableView.setRowCount(int(self.row_count))
        self.column_name = ['Name', "Size", "Tol.", "Comm", ]
        self.TableView.setHorizontalHeaderLabels(self.column_name)
        #DISABLE EDIT
        self.TableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        #ALIGN
        self.TableView.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.TableView.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.TableView.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.TableView.horizontalHeaderItem(0).setTextAlignment(QtCore.Qt.AlignLeft)
        self.TableView.horizontalHeaderItem(1).setTextAlignment(QtCore.Qt.AlignLeft)
        self.TableView.horizontalHeaderItem(2).setTextAlignment(QtCore.Qt.AlignLeft)
        self.TableView.horizontalHeaderItem(3).setTextAlignment(QtCore.Qt.AlignLeft)
        self.TableView.setGeometry(QtCore.QRect(570, 30, 400, 221))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.TableView.setFont(font)
        self.TableView.setStyleSheet("QTableView{\n"
"background-color: #343434;\n"
"color: white;\n"
"border: 5px;\n"
"border-color: red;\n"
"border-radius:5px;\n"
"}")
        self.TableView.setObjectName("TableView")



        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setEnabled(True)
        self.textEdit.setGeometry(QtCore.QRect(590, 330, 350, 25))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.textEdit.setFont(font)
        self.textEdit.setAcceptDrops(True)
        self.textEdit.setAutoFillBackground(False)
        self.textEdit.setStyleSheet("QTextEdit{\n"
"background-color: #AFAFAF;\n"
"}")
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setDocumentTitle("")
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(590, 370, 170, 25))
        self.textEdit_2.setStyleSheet("QTextEdit{\n"
"background-color: #AFAFAF;\n"
"}")
        self.textEdit_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_3.setGeometry(QtCore.QRect(770, 370, 170, 25))
        self.textEdit_3.setStyleSheet("QTextEdit{\n"
"background-color: #AFAFAF;\n"
"}")
        self.textEdit_3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit_3.setObjectName("textEdit_3")
        self.textEdit_4 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_4.setGeometry(QtCore.QRect(590, 410, 350, 25))
        self.textEdit_4.setStyleSheet("QTextEdit{\n"
"background-color: #AFAFAF;\n"
"}")
        self.textEdit_4.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit_4.setDocumentTitle("")
        self.textEdit_4.setObjectName("textEdit_4")
        self.DataInputLabel = QtWidgets.QLabel(self.centralwidget)
        self.DataInputLabel.setGeometry(QtCore.QRect(570, 300, 400, 181))
        self.DataInputLabel.setStyleSheet("QLabel{\n"
"background-color: #343434;\n"
"border-radius: 5px;\n"
"}")
        self.DataInputLabel.setText("")
        self.DataInputLabel.setObjectName("DataInputLabel")
        self.SubmitButton = QtWidgets.QPushButton(self.centralwidget)
        self.SubmitButton.setGeometry(QtCore.QRect(720, 445, 100, 25))
        self.SubmitButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.SubmitButton.setStyleSheet("QPushButton{\n"
"color: #343434;\n"
"background-color: #9FFF87;\n"
"border-color: #9FFF87;\n"
"border-radius: 5px;\n"
"color: black;\n"                                        
"}\n"
"\n"
"QPushButton:hover{\n"
"background-color: white;\n"
"}\n"
"")
        self.SubmitButton.setObjectName("SubmitButton")
        self.ComLabel = QtWidgets.QLabel(self.centralwidget)
        self.ComLabel.setGeometry(QtCore.QRect(570, 496, 400, 30))
        self.ComLabel.setStyleSheet("QLabel{\n"
"background-color: #343434;\n"
"border-radius: 5px;\n"
"}")
        self.ComLabel.setText("")
        self.ComLabel.setObjectName("ComLabel")
        self.ComSelectBox = QtWidgets.QSpinBox(self.centralwidget)
        self.ComSelectBox.setGeometry(QtCore.QRect(585, 500, 42, 22))
        self.ComSelectBox.setStyleSheet("QSpinBox{\n"
"background-color: #E5E5E5;\n"
"}")

        self.ComSelectBox.setObjectName("ComSelectBox")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(640, 500, 315, 22))
        self.textBrowser.setStyleSheet("QTextBrowser{\n"
"background-color: #E5E5E5;\n"
"}")
        self.textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(870, 550, 121, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel{\n"
" color: white;\n"
"}")
        self.label.setObjectName("label")
        self.ComLabel_2 = QtWidgets.QLabel(self.centralwidget)
        self.ComLabel_2.setGeometry(QtCore.QRect(570, 260, 400, 30))
        self.ComLabel_2.setStyleSheet("QLabel{\n"
"background-color: #343434;\n"
"border-radius: 5px;\n"
"}")
        self.ComLabel_2.setText("")
        self.ComLabel_2.setObjectName("ComLabel_2")
        self.ComSelectBox_2 = QtWidgets.QSpinBox(self.centralwidget)
        self.ComSelectBox_2.setGeometry(QtCore.QRect(580, 264, 42, 22))
        self.ComSelectBox_2.setStyleSheet("QSpinBox{\n"
"background-color: #E5E5E5;\n"
"}")
        self.ComSelectBox_2.setObjectName("ComSelectBox_2")
        self.SubmitButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.SubmitButton_2.setGeometry(QtCore.QRect(630, 264, 100, 20))
        self.SubmitButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.SubmitButton_2.setStyleSheet("QPushButton{\n"
"background-color: #9FFF87;\n"
"border-color: #9FFF87;\n"
"border-radius: 5px;\n"
"color: black;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background-color: white;\n"
"}\n"
"")
        self.SubmitButton_2.setObjectName("SubmitButton_2")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(740, 264, 220, 22))
        self.textBrowser_2.setStyleSheet("QTextBrowser{\n"
"background-color: #E5E5E5;\n"
"}")
        self.textBrowser_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(550, 30, 20, 501))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.ComLabel.raise_()
        self.DataInputLabel.raise_()
        self.CameraLabel.raise_()
        self.TableView.raise_()
        self.textEdit.raise_()
        self.textEdit_2.raise_()
        self.textEdit_3.raise_()
        self.textEdit_4.raise_()
        self.SubmitButton.raise_()
        self.ComSelectBox.raise_()
        self.textBrowser.raise_()
        self.label.raise_()
        self.ComLabel_2.raise_()
        self.ComSelectBox_2.raise_()
        self.SubmitButton_2.raise_()
        self.textBrowser_2.raise_()
        self.line.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        #BUTTON CLICKS
        self.SubmitButton.clicked.connect(self.check_name)
        self.SubmitButton_2.clicked.connect(self.db_load)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Measurement System"))
        self.textEdit.setAccessibleName(_translate("MainWindow", "Name"))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "Name"))
        self.textEdit_2.setPlaceholderText(_translate("MainWindow", "Size"))
        self.textEdit_3.setPlaceholderText(_translate("MainWindow", "Tolerance"))
        self.textEdit_4.setPlaceholderText(_translate("MainWindow", "Comment"))
        self.SubmitButton.setText(_translate("MainWindow", "Submit"))
        self.label.setText(_translate("MainWindow", "Designed by Yurii Moroz"))
        self.SubmitButton_2.setText(_translate("MainWindow", "Load"))




if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())

