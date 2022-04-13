from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import sqlite3
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView
from connect import zero_init, create_db

class Ui_MainWindow(object):
    db_status = 0
    def __init__(self):
        self.row_count = 0
        self.db_status = 0
        self.selected_name = "None"
        self.selected_size = 0
        self.selected_tol = 0
        create_db(r".\ObjectDB.db")
        zero_init()


    def delete_from_db(self):
        sqlite_file = './ObjectDB.db'
        db = sqlite3.connect(sqlite_file)
        sql = db.cursor()
        spinBoxValue = self.ComSelectBox_2.value()
        if spinBoxValue == 0:
            pass
        elif spinBoxValue >= 1:
            sql.execute('SELECT Name FROM objects')
            self.db_names_delete = sql.fetchall()[spinBoxValue - 1][0]
            sql.execute(f'DELETE FROM objects WHERE Name = "{str(self.db_names_delete)}"')
            db.commit()
            self.textBrowser_2.setText(f'DB: Successfully removed: {self.db_names_delete}')
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

            i = 0
            while i != self.row_count:
                self.TableView.setItem(i, 0, QTableWidgetItem(f"{self.db_names[i][0]}"))
                self.TableView.setItem(i, 1, QTableWidgetItem(f"{self.db_size[i][0]}"))
                self.TableView.setItem(i, 2, QTableWidgetItem(f"{self.db_tol[i][0]}"))
                self.TableView.setItem(i, 3, QTableWidgetItem(f"{self.db_com[i][0]}"))
                i = i + 1
            db.close()
            self.__setattr__("db_status", 1)
        else:
            pass


    def discard(self):
        sqlite_file = './ObjectDB.db'
        db = sqlite3.connect(sqlite_file)
        sql = db.cursor()
        sql.execute(f'UPDATE current SET Ind = "0" WHERE status = {int(25)}')
        db.commit()
        db.close()
        self.textBrowser.setText('Ruller mode is now active.')

    def db_load(self):
        sqlite_file = './ObjectDB.db'
        spinBoxValue = self.ComSelectBox_2.value()
        if int(spinBoxValue) == 0:
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

            i = 0
            while i != self.row_count:
                self.TableView.setItem(i, 0, QTableWidgetItem(f"{self.db_names[i][0]}"))
                self.TableView.setItem(i, 1, QTableWidgetItem(f"{self.db_size[i][0]}"))
                self.TableView.setItem(i, 2, QTableWidgetItem(f"{self.db_tol[i][0]}"))
                self.TableView.setItem(i, 3, QTableWidgetItem(f"{self.db_com[i][0]}"))
                i = i + 1
            db.close()
            self.textBrowser_2.setText('DB: Successfully loaded.')
            self.__setattr__("db_status", 1)
        else:
            self.spinBoxValue = self.ComSelectBox_2.value()
            self.textBrowser_2.setText(f'{spinBoxValue}')
            if spinBoxValue <= self.row_count:
                ids = int(spinBoxValue) - 1
                self.textBrowser.setText(f'SELECT: {self.db_names[ids][0]} size: {self.db_size[ids][0]} with max tol: {self.db_tol[ids][0]}')
                db = sqlite3.connect(sqlite_file)
                sql = db.cursor()
                sql.execute(
                    f'UPDATE current SET Name = "{str(self.db_names[ids][0])}", Size = "{str(self.db_size[ids][0])}", Tol = "{str(self.db_tol[ids][0])}" WHERE status = {int(25)}')
                sql.execute(f'UPDATE current SET Ind = "1" WHERE status = {int(25)}')
                db.commit()
                db.close()
            else:
                self.textBrowser_2.setText('DB: Out of range.')


    def check_name(self):
        try:
            if self.db_status != 0:
                text_name = self.textEdit.toPlainText()
                text_size = self.textEdit_2.toPlainText()
                text_tol = self.textEdit_3.toPlainText()
                text_comm = self.textEdit_4.toPlainText()

                sqlite_file = './ObjectDB.db'
                db = sqlite3.connect(sqlite_file)
                sql = db.cursor()
                sql.execute(f'SELECT Name FROM objects WHERE Name = "{text_name}"')

                if sql.fetchone() is None:
                    sql.execute(f'INSERT INTO objects VALUES (?, ?, ?, ?, ?)', (0, text_name, text_size, text_tol,text_comm))
                    db.commit()
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

                    i = 0
                    while i != self.row_count:
                        self.TableView.setItem(i, 0, QTableWidgetItem(f"{self.db_names[i][0]}"))
                        self.TableView.setItem(i, 1, QTableWidgetItem(f"{self.db_size[i][0]}"))
                        self.TableView.setItem(i, 2, QTableWidgetItem(f"{self.db_tol[i][0]}"))
                        self.TableView.setItem(i, 3, QTableWidgetItem(f"{self.db_com[i][0]}"))
                        i = i + 1
                    db.close()
                else:
                    self.textBrowser_2.setText('DB: Object already exists')
            elif self.db_status == 0:
                self.textBrowser_2.setText("DB: Not loaded!")
        except:
            self.textBrowser_2.setText("DB: Load error!")

    def open_camera(self):
        import _openCV
        _openCV.Output().frame()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(440, 550)
        MainWindow.setMinimumSize(QtCore.QSize(440, 550))
        MainWindow.setMaximumSize(QtCore.QSize(440, 550))
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("QWidget{\n"
"background-color:#4D4D4D;\n"
"}")
        self.centralwidget.setObjectName("centralwidget")


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
        self.TableView.setGeometry(QtCore.QRect(20, 20, 400, 221))
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
        self.textEdit.setGeometry(QtCore.QRect(40, 320, 350, 25))
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
        self.textEdit_2.setGeometry(QtCore.QRect(40, 360, 170, 25))
        self.textEdit_2.setStyleSheet("QTextEdit{\n"
"background-color: #AFAFAF;\n"
"}")
        self.textEdit_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_3.setGeometry(QtCore.QRect(220, 360, 170, 25))
        self.textEdit_3.setStyleSheet("QTextEdit{\n"
"background-color: #AFAFAF;\n"
"}")
        self.textEdit_3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit_3.setObjectName("textEdit_3")
        self.textEdit_4 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_4.setGeometry(QtCore.QRect(40, 400, 350, 25))
        self.textEdit_4.setStyleSheet("QTextEdit{\n"
"background-color: #AFAFAF;\n"
"}")
        self.textEdit_4.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit_4.setDocumentTitle("")
        self.textEdit_4.setObjectName("textEdit_4")
        self.DataInputLabel = QtWidgets.QLabel(self.centralwidget)
        self.DataInputLabel.setGeometry(QtCore.QRect(20, 290, 400, 181))
        self.DataInputLabel.setStyleSheet("QLabel{\n"
"background-color: #343434;\n"
"border-radius: 5px;\n"
"}")
        self.DataInputLabel.setText("")
        self.DataInputLabel.setObjectName("DataInputLabel")
        self.SubmitButton = QtWidgets.QPushButton(self.centralwidget)
        self.SubmitButton.setGeometry(QtCore.QRect(40, 435, 175, 25))
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
        self.SubmitButton_open_camera = QtWidgets.QPushButton(self.centralwidget)
        self.SubmitButton_open_camera.setGeometry(QtCore.QRect(315, 435, 75, 25))
        self.SubmitButton_open_camera.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.SubmitButton_open_camera.setStyleSheet("QPushButton{\n"
                                        "color: #ff8243;\n"
                                        "background-color: #ff8243;\n"
                                        "border-color: #9FFF87;\n"
                                        "border-radius: 5px;\n"
                                        "color: black;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:hover{\n"
                                        "background-color: white;\n"
                                        "}\n"
                                        "")
        self.SubmitButton_open_camera.setObjectName("SubmitButton_open_camera")
        self.SubmitButton_delete_from_db = QtWidgets.QPushButton(self.centralwidget)
        self.SubmitButton_delete_from_db.setGeometry(QtCore.QRect(230, 435, 75, 25))
        self.SubmitButton_delete_from_db.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.SubmitButton_delete_from_db.setStyleSheet("QPushButton{\n"
                                                    "color: #BE1825;\n"
                                                    "background-color: #C42F3A;\n"
                                                    "border-color: #9FFF87;\n"
                                                    "border-radius: 5px;\n"
                                                    "color: black;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QPushButton:hover{\n"
                                                    "background-color: white;\n"
                                                    "}\n"
                                                    "")
        self.SubmitButton_delete_from_db.setObjectName("SubmitButton_open_camera")
        self.SubmitButton_ruller = QtWidgets.QPushButton(self.centralwidget)
        self.SubmitButton_ruller.setGeometry(QtCore.QRect(30, 482, 50, 20))
        self.SubmitButton_ruller.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.SubmitButton_ruller.setStyleSheet("QPushButton{\n"
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
        self.SubmitButton_ruller.setObjectName("RM")
        self.ComLabel = QtWidgets.QLabel(self.centralwidget)
        self.ComLabel.setGeometry(QtCore.QRect(20, 477, 400, 30))
        self.ComLabel.setStyleSheet("QLabel{\n"
"background-color: #343434;\n"
"border-radius: 5px;\n"
"}")
        self.ComLabel.setText("")
        self.ComLabel.setObjectName("ComLabel")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(90, 481, 315, 22))
        self.textBrowser.setStyleSheet("QTextBrowser{\n"
"background-color: #E5E5E5;\n"
"}")
        self.textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(340, 5, 100, 15))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel{\n"
" color: 343434;\n"
"}")
        self.label.setObjectName("label")
        self.ComLabel_2 = QtWidgets.QLabel(self.centralwidget)
        self.ComLabel_2.setGeometry(QtCore.QRect(20, 250, 400, 30))
        self.ComLabel_2.setStyleSheet("QLabel{\n"
"background-color: #343434;\n"
"border-radius: 5px;\n"
"}")
        self.ComLabel_2.setText("")
        self.ComLabel_2.setObjectName("ComLabel_2")
        self.ComSelectBox_2 = QtWidgets.QSpinBox(self.centralwidget)
        self.ComSelectBox_2.setGeometry(QtCore.QRect(30, 254, 42, 22))
        self.ComSelectBox_2.setStyleSheet("QSpinBox{\n"
"background-color: #E5E5E5;\n"
"}")
        self.ComSelectBox_2.setObjectName("ComSelectBox_2")
        self.SubmitButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.SubmitButton_2.setGeometry(QtCore.QRect(80, 254, 100, 20))
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
        self.textBrowser_2.setGeometry(QtCore.QRect(190, 254, 220, 22))
        self.textBrowser_2.setStyleSheet("QTextBrowser{\n"
"background-color: #E5E5E5;\n"
"}")
        self.textBrowser_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 20, 20, 501))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line2 = QtWidgets.QFrame(self.centralwidget)
        self.line2.setGeometry(QtCore.QRect(420, 20, 20, 501))
        self.line2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line2.setObjectName("line2")
        self.ComLabel.raise_()
        self.DataInputLabel.raise_()
        self.TableView.raise_()
        self.textEdit.raise_()
        self.textEdit_2.raise_()
        self.textEdit_3.raise_()
        self.textEdit_4.raise_()
        self.SubmitButton.raise_()
        self.SubmitButton_ruller.raise_()
        self.textBrowser.raise_()
        self.label.raise_()
        self.ComLabel_2.raise_()
        self.ComSelectBox_2.raise_()
        self.SubmitButton_2.raise_()
        self.SubmitButton_open_camera.raise_()
        self.SubmitButton_delete_from_db.raise_()
        self.textBrowser_2.raise_()
        self.line.raise_()
        self.line2.raise_()
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
        self.SubmitButton_ruller.clicked.connect(self.discard)
        self.SubmitButton_open_camera.clicked.connect(self.open_camera)
        self.SubmitButton_delete_from_db.clicked.connect(self.delete_from_db)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Measurement System"))
        self.textEdit.setAccessibleName(_translate("MainWindow", "Name"))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "Name"))
        self.textEdit_2.setPlaceholderText(_translate("MainWindow", "Size"))
        self.textEdit_3.setPlaceholderText(_translate("MainWindow", "Tolerance"))
        self.textEdit_4.setPlaceholderText(_translate("MainWindow", "Comment"))
        self.SubmitButton.setText(_translate("MainWindow", "🖊"))
        self.label.setText(_translate("MainWindow", "v1.0"))
        self.SubmitButton_2.setText(_translate("MainWindow", "✔"))
        self.SubmitButton_ruller.setText((_translate("MainWindow", "📏")))
        self.SubmitButton_open_camera.setText(_translate("MainWindow", "🎥"))
        self.SubmitButton_delete_from_db.setText(_translate("MainWindow", "🗑"))




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())



