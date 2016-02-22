from PyQt4 import QtCore, QtGui, uic
from Network import sendData, dbData
import time

class SimulationWidget(QtGui.QWidget):
    
    Logged = False

    def __init__(self):
        super(SimulationWidget, self).__init__()
        uic.loadUi('SimulationWidget.ui', self)
        self.login_btn.clicked.connect(self.login)
        self.logout_btn.clicked.connect(self.logout)
        self.role_change_btn.clicked.connect(self.rolechange)
            
    def setLogged(self, isLogged):
        """
        Input: isLogged: Boolean
        Output: None
        Purpose: To set the Logged variable with the desired status(Boolean)
        """
        self.Logged = isLogged
    def isLogged(self):
        """
        Input: None
        Output: Boolean
        Purpose: Returns the Logged Variable
        """
        return self.Logged
    
    def login(self):
        """
        Input: None
        Output: Boolean
        Purpose: Handles the login function for the application and returns a boolean whenever its succesfull or not
        """
        if(self.Logged == False and self.check_values()):
            data = self.createData('login')
            sendData(data)
            self.Logged = 1
            return True
        else:
            if(self.Logged == True):
                self.error_lbl.setText('You need to log out to log in')
            return False
    def logout(self):
        """
        Input: None
        Output: Boolean
        Purpose: Handles the logout function for the application and returns a boolean whenever its succesfull or not
        """
        if(self.Logged == True and self.check_values()):
            data = self.createData('logout')
            sendData(data)
            self.Logged = 0
            return True
        else:
            if(self.Logged == False):
                self.error_lbl.setText('You need to be logged in to log out')
            return False

    def rolechange(self):
        """
        Input: None
        Output: Boolean
        Purpose: Handles the role change function for the application and returns a boolean whenever its succesfull or not
        """
        if(self.Logged == True and self.check_values()):
            data = self.createData('role change')
            sendData(data)
            return True
        else:
            if(self.Logged == False):
                self.error_lbl.setText('You need to be logged in to change role')
            return False

    def check_integer(self,value):
        """
        Input: value: Integer
        Output: Boolean
        Purpose: Checks if value is a valid integer and not less than 0
        """
        try:
            int(value)
        except ValueError:
            return False
        if (int(value) < 0):
            return False
        else:
            return True

    def check_values(self):
        """
        Input: None
        Output: Boolean
        Purpose: Checks the ID's for invalidness and if so prints a error message to the error label then returns false, else it will return true
        """
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
        """
        Input: value: eventType: String
        Output: Dictionairy
        Purpose: Collates all the data
        """
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
