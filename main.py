from _openCV import Output
from multiprocessing import Process
from GUI import *

def detection():
    screen = Output().frame()

def gui():
    while True:
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    Process(target=detection()).start()
    Process(target=gui()).start()


