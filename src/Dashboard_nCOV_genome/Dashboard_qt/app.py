from PySide2 import QtWidgets, QtCore, QtWebEngineWidgets


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QWidget{background-color: #f8f9fa;}")

        self.main_layout = QtWidgets.QGridLayout(self)

        self.spin = QtWidgets.QSpinBox()
        self.spin.setValue(30)
        self.spin.setRange(7,1200)

        self.btn_refresh = QtWidgets.QPushButton('Refresh')
        self.btn_refresh.clicked.connect(self.refresh)

        self.view = QtWebEngineWidgets.QWebEngineView()
        self.view.load(QtCore.QUrl("http:127.0.0.1:8000"))
        self.setWindowTitle("Dashboard title")
        self.main_layout.addWidget(self.spin, 0,0,1,1)
        self.main_layout.addWidget(self.btn_refresh, 0, 1, 1, 1)
        self.main_layout.addWidget(self.view,1,0,1,2)

    def refresh(self):
        days = self.spin.value()
        self.view.load(QtCore.QUrl(f"http:127.0.0.1:8000/days={days}"))


app = QtWidgets.QApplication([])
win = Window()
win.showFullScreen()
app.exec_()
