from PyQt4 import QtCore, QtGui, uic
from Network import sendData, dbData
from connectionHandler import createJSONFormat,postRequest
import time

#LIST OF TODO'S
#CHANGE COMMENTS TO REFLECT ACTUALL USAGE
#CLEAN THE CODE
#ADD USABILITY FEATURES.
#ADD TRY CATCH methods to the connectionHandler

class SimulationWidget(QtGui.QWidget):
    
    testMode = False
    Logged = False
    baseURL = 'http://193.10.30.129:8080/'

    def __init__(self, testMode = False):
        super(SimulationWidget, self).__init__()
        self.testMode = testMode
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
            JSONstring = createJSONFormat(data)
            URL = self.baseURL + 'login'
            if self.testMode == False:
                postRequest(URL,JSONstring)
            #sendData(data)
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
            JSONstring = createJSONFormat(data)
            URL = self.baseURL + 'logout'
            if self.testMode == False:
                postRequest(URL,JSONstring)
            #sendData(data)
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
            JSONstring = createJSONFormat(data)
            URL = self.baseURL + 'roleChange'
            if self.testMode == False:
                postRequest(URL,JSONstring)
            
            #sendData(data)
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
        else:
            self.error_lbl.setText(' ')
            return True


    def createData(self, eventType):
        """
        Input: value: eventType: String
        Output: Dictionairy
        Purpose: Collates all the data
        """
        data = []
        data.append(int(self.controllerID_line.text()))
        data.append(str(eventType))
        data.append(str(self.role_cmbox.currentText()))
        data.append(str(self.responsibility_cmbox.currentText()))
        data.append(str(self.operational_cmbox.currentText()))
        data.append(str(time.strftime('%Y-%m-%d %H:%M:%S')))
        data.append('None')
        data.append('None')
        data.append(str(self.facility_line.text()),)
        data.append('None')
        data.append(str(self.workstationID_line.text()))
        data.append(int(0))
        
        """"
        data = {
            dbData[0] : str(self.controllerID_line.text()),
            dbData[1] : str(eventType),
            dbData[2] : str(self.role_cmbox.currentText()),
            dbData[3] : str(self.responsibility_cmbox.currentText()),
            dbData[4] : str(self.operational_cmbox.currentText()),
            dbData[5] : str(time.strftime('%Y-%m-%d %H:%M:%S')),
            dbData[6] : 'None',
            dbData[7] : 'None',
            dbData[8] : str(self.facility_line.text()),
            dbData[9] : 'None',
            dbData[10] : str(self.workstationID_line.text()),
            dbData[11] : str(0)
        }
        """
        return data
