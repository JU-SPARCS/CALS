from PyQt4 import QtCore, QtGui, uic
from Network import sendData
import time

class SimulationWidget(QtGui.QWidget):
    def __init__(self):
        super(SimulationWidget, self).__init__()
        uic.loadUi('SimulationWidget.ui', self)
        self.loginButton.clicked.connect(self.login)
        self.logoutButton.clicked.connect(self.logout)

    def login(self):
        sendData(int(self.idATCO.text()), "login", "Test", "Test", "Test", time.strftime('%Y-%m-%d %H:%M:%S'), True)

    def logout(self):
        sendData(int(self.idATCO.text()), "logout", "Test", "Test", "Test", time.strftime('%Y-%m-%d %H:%M:%S'), True)
