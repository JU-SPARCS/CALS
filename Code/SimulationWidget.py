from PyQt4 import QtCore, QtGui, uic
from Network import sendData, dbData
import time

class SimulationWidget(QtGui.QWidget):
    def __init__(self):
        super(SimulationWidget, self).__init__()
        uic.loadUi('SimulationWidget.ui', self)

        self.login_btn.clicked.connect(self.login)
        self.logout_btn.clicked.connect(self.logout)
        self.role_change_btn.clicked.connect(self.rolechange)

    def login(self):
        if(self.check_values()):
            data = self.createData('login')
            sendData(data)
    def logout(self):
        if(self.check_values()):
            data = self.createData('logout')
            sendData(data)
    def rolechange(self):
        if(self.check_values()):
            data = self.createData('role change')
            sendData(data)

    def check_integer(self,value):
        """Checks if value is a number and not under zero"""
        try:
            int(value)
        except ValueError:
            return False
        if (int(value) < 0):
            return False
        else:
            return True

    def check_values(self):
        """ Check if the controller id and workstation id is correct """
        if( not self.check_integer(self.controllerID_line.text())):
            self.error_lbl.setText('Controller ID has to be a number and not less than zero')
            return False
        elif(not self.check_integer(self.workstationID_line.text())):
            self.error_lbl.setText('Workstation ID has to be a number and not less than zero')
            return False
        else:
            self.error_lbl.setText(' ')
            return True


    def createData(self, eventType):
        data = {
            dbData[0] : self.controllerID_line.text(),
            dbData[1] : eventType,
            dbData[2] : str(self.role_cmbox.currentText()),
            dbData[3] : str(self.responsibility_cmbox.currentText()),
            dbData[4] : str(self.operational_cmbox.currentText()),
            dbData[5] : time.strftime('%Y-%m-%d %H:%M:%S'),
            dbData[6] : 'None',
            dbData[7] : 'None',
            dbData[8] : self.facility_line.text(),
            dbData[9] : 'None',
            dbData[10] : self.workstationID_line.text()
        }
        return data
