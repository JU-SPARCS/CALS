from PyQt4 import QtCore, QtGui, uic
from Network import sendData, dbData
import time

class SimulationWidget(QtGui.QWidget):
    def __init__(self):
        super(SimulationWidget, self).__init__()
        uic.loadUi('SimulationWidget.ui', self)
        self.loginButton.clicked.connect(self.login)
        self.logoutButton.clicked.connect(self.logout)

    def login(self):
        data = self.createFakeData('login')
        sendData(data)
        #sendData(int(self.idATCO.text()), "login", "Test", "Test", "Test", time.strftime('%Y-%m-%d %H:%M:%S'), True)
    def logout(self):
        data = self.createFakeData('logout')
        sendData(data)
        #sendData(int(self.idATCO.text()), "logout", "Test", "Test", "Test", time.strftime('%Y-%m-%d %H:%M:%S'), True)

    def createFakeData(self, eventType):
        data = {
            dbData[0] : self.idATCO.text(),
            dbData[1] : eventType,
            dbData[2] : 'RadarTerminal',
            dbData[3] : 'Planning',
            dbData[4] : 'SC',
            dbData[5] : time.strftime('%Y-%m-%d %H:%M:%S'),
            dbData[6] : 'H',
            dbData[7] : 'D',
            dbData[8] : 'Facility XX',
            dbData[9] : 'Airspace segment XX',
            dbData[10] : 'Workstation X'
        }
        return data
