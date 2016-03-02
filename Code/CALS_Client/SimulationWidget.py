from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi   
from connectionHandler import createJSONFormat,postRequest
import time
import pymysql

""" db connection """
DB_HOST = '193.10.30.129'
DB_USER = 'root'
DB_PASSWORD = 'JTH123!'
DB_NAME = 'cals_sim'

def dbConnection():
    connection = pymysql.connect(host=DB_HOST,
                                 user=DB_USER,
                                 password=DB_PASSWORD,
                                 db=DB_NAME)
    return connection


connection = dbConnection()

class SimulationWidget(QDialog):

    def __init__(self):
        super(SimulationWidget, self).__init__()
        loadUi('select-facilities-workstations.ui', self)
        self.cur = connection.cursor(pymysql.cursors.DictCursor)
        self.cur.execute("SELECT * FROM facilities")
        self.listFacilities = self.cur.fetchall()
        self.cur.execute("SELECT * FROM workstations") 
        self.listWorkstations = self.cur.fetchall()
        self.facilities.clear()
        for facility in self.listFacilities:
            self.facilities.addItem(facility["name"])
        self.workstations.clear()
        for workstation in self.listWorkstations:
            self.workstations.addItem(workstation["name"])
        self.launch.clicked.connect(self.launchAction)
        self.log = None


    def launchAction(self):
        self.log = LogWidget(self.facilities.currentText(), self.workstations.currentText())
        self.log.show()

class LogWidget(QDialog):
    def __init__(self, facility, workstation):
        super(LogWidget, self).__init__()
        loadUi('field-workers.ui', self)
        self.facility = facility
        self.workstation = workstation
        self.operationalStatusList = [ self.operational_status.itemText(i) for i in range(self.operational_status.count())]
        self.cur = connection.cursor(pymysql.cursors.DictCursor)
        self.cur.execute("SELECT * FROM users u LEFT JOIN facilities f on u.facilitiesid = f.id where f.name LIKE %s ", facility)
        self.users = self.cur.fetchall()
        self.controller_id_1.clear()
        self.controller_id_1.addItem("choice")
        self.controller_id_2.addItem("choice")
        for user in self.users:
            self.controller_id_1.addItem(user["name"])
            self.controller_id_2.addItem(user["name"])
        self.controller_id_1.currentIndexChanged.connect(self.controller1Action)
        self.controller_id_2.currentIndexChanged.connect(self.controller2Action)
        self.login.clicked.connect(self.loginAction)
        self.change_role.clicked.connect(self.updateAction)
        self.logout.clicked.connect(self.logoutAction)

    def logoutAction(self):
        
        if (self.controller_id_1.currentText() == self.controller_id_2.currentText()):
            self.error.setText('The field controller Id 1 and controller Id 2 are same !')
        else:
            if (self.controller_id_1.currentText() != "choice"):
                self.cur.execute("SELECT * FROM users u WHERE u.name LIKE %s ", self.controller_id_1.currentText())
                userMysql = self.cur.fetchone()
                userId = userMysql["id"]
                self.cur.execute("SELECT * FROM facilities f WHERE f.name LIKE %s ", self.facility)
                facilityMysql = self.cur.fetchone()
                facilityId = facilityMysql["id"]
                self.cur.execute("SELECT * FROM workstations w WHERE w.name LIKE %s ", self.workstation)
                workstationMysql = self.cur.fetchone()
                workstationId = workstationMysql["id"]
                v = ("logout", self.role.currentText(), self.controller_responsability.currentText(), self.operational_status.currentText(), 0, int(userId), int(facilityId), int(workstationId))
                connect = connection.cursor()
                connect.execute("INSERT INTO log_events (event_type, controller_role, controller_responsability, operational_status, date, send_to_narms, usersid, facilitiesid, workstationsid) VALUES (%s, %s,%s,%s,NOW(),%s,%s,%s,%s)", v) 
                connection.commit()

            if (self.controller_id_2.currentText() != "choice"):
                self.cur.execute("SELECT * FROM users u WHERE u.name LIKE %s ", self.controller_id_2.currentText())
                userMysql = self.cur.fetchone()
                userId = userMysql["id"]
                self.cur.execute("SELECT * FROM facilities f WHERE f.name LIKE %s ", self.facility)
                facilityMysql = self.cur.fetchone()
                facilityId = facilityMysql["id"]
                self.cur.execute("SELECT * FROM workstations w WHERE w.name LIKE %s ", self.workstation)
                workstationMysql = self.cur.fetchone()
                workstationId = workstationMysql["id"]
                if (self.operational_status.currentText() == "MCU"):
                    v = ("logout", self.role.currentText(), self.controller_responsability.currentText(), "MCU", 0, int(userId), int(facilityId), int(workstationId))
                if (self.operational_status.currentText() == "MCM"):
                    v = ("logout", self.role.currentText(), self.controller_responsability.currentText(), "MCS", 0, int(userId), int(facilityId), int(workstationId))
                if (self.operational_status.currentText() == "MCI"):
                    v = ("logout", self.role.currentText(), self.controller_responsability.currentText(), "MCT", 0, int(userId), int(facilityId), int(workstationId))
                connect = connection.cursor()
                connect.execute("INSERT INTO log_events (event_type, controller_role, controller_responsability, operational_status, date, send_to_narms, usersid, facilitiesid, workstationsid) VALUES (%s, %s,%s,%s,NOW(),%s,%s,%s,%s)", v) 
                connection.commit()

    def updateAction(self):
        
        if (self.controller_id_1.currentText() == self.controller_id_2.currentText()):
            self.error.setText('The field controller Id 1 and controller Id 2 are same !')
        else:
            if (self.controller_id_1.currentText() != "choice"):
                self.cur.execute("SELECT * FROM users u WHERE u.name LIKE %s ", self.controller_id_1.currentText())
                userMysql = self.cur.fetchone()
                userId = userMysql["id"]
                self.cur.execute("SELECT * FROM facilities f WHERE f.name LIKE %s ", self.facility)
                facilityMysql = self.cur.fetchone()
                facilityId = facilityMysql["id"]
                self.cur.execute("SELECT * FROM workstations w WHERE w.name LIKE %s ", self.workstation)
                workstationMysql = self.cur.fetchone()
                workstationId = workstationMysql["id"]
                v = ("update", self.role.currentText(), self.controller_responsability.currentText(), self.operational_status.currentText(), 0, int(userId), int(facilityId), int(workstationId))
                connect = connection.cursor()
                connect.execute("INSERT INTO log_events (event_type, controller_role, controller_responsability, operational_status, date, send_to_narms, usersid, facilitiesid, workstationsid) VALUES (%s, %s,%s,%s,NOW(),%s,%s,%s,%s)", v) 
                connection.commit()

            if (self.controller_id_2.currentText() != "choice"):
                self.cur.execute("SELECT * FROM users u WHERE u.name LIKE %s ", self.controller_id_2.currentText())
                userMysql = self.cur.fetchone()
                userId = userMysql["id"]
                self.cur.execute("SELECT * FROM facilities f WHERE f.name LIKE %s ", self.facility)
                facilityMysql = self.cur.fetchone()
                facilityId = facilityMysql["id"]
                self.cur.execute("SELECT * FROM workstations w WHERE w.name LIKE %s ", self.workstation)
                workstationMysql = self.cur.fetchone()
                workstationId = workstationMysql["id"]
                if (self.operational_status.currentText() == "MCU"):
                    v = ("update", self.role.currentText(), self.controller_responsability.currentText(), "MCU", 0, int(userId), int(facilityId), int(workstationId))
                if (self.operational_status.currentText() == "MCM"):
                    v = ("update", self.role.currentText(), self.controller_responsability.currentText(), "MCS", 0, int(userId), int(facilityId), int(workstationId))
                if (self.operational_status.currentText() == "MCI"):
                    v = ("update", self.role.currentText(), self.controller_responsability.currentText(), "MCT", 0, int(userId), int(facilityId), int(workstationId))
                connect = connection.cursor()
                connect.execute("INSERT INTO log_events (event_type, controller_role, controller_responsability, operational_status, date, send_to_narms, usersid, facilitiesid, workstationsid) VALUES (%s, %s,%s,%s,NOW(),%s,%s,%s,%s)", v) 
                connection.commit()


    def loginAction(self):
        if (self.controller_id_1.currentText() == self.controller_id_2.currentText()):
            self.error.setText('The field controller Id 1 and controller Id 2 are same !')
        else:
            if (self.controller_id_1.currentText() != "choice"):
                self.cur.execute("SELECT * FROM users u WHERE u.name LIKE %s ", self.controller_id_1.currentText())
                userMysql = self.cur.fetchone()
                userId = userMysql["id"]
                self.cur.execute("SELECT * FROM facilities f WHERE f.name LIKE %s ", self.facility)
                facilityMysql = self.cur.fetchone()
                facilityId = facilityMysql["id"]
                self.cur.execute("SELECT * FROM workstations w WHERE w.name LIKE %s ", self.workstation)
                workstationMysql = self.cur.fetchone()
                workstationId = workstationMysql["id"]
                v = ("login", self.role.currentText(), self.controller_responsability.currentText(), self.operational_status.currentText(), 0, int(userId), int(facilityId), int(workstationId))
                connect = connection.cursor()
                connect.execute("INSERT INTO log_events (event_type, controller_role, controller_responsability, operational_status, date, send_to_narms, usersid, facilitiesid, workstationsid) VALUES (%s, %s,%s,%s,NOW(),%s,%s,%s,%s)", v) 
                connection.commit()

            if (self.controller_id_2.currentText() != "choice"):
                self.cur.execute("SELECT * FROM users u WHERE u.name LIKE %s ", self.controller_id_2.currentText())
                userMysql = self.cur.fetchone()
                userId = userMysql["id"]
                self.cur.execute("SELECT * FROM facilities f WHERE f.name LIKE %s ", self.facility)
                facilityMysql = self.cur.fetchone()
                facilityId = facilityMysql["id"]
                self.cur.execute("SELECT * FROM workstations w WHERE w.name LIKE %s ", self.workstation)
                workstationMysql = self.cur.fetchone()
                workstationId = workstationMysql["id"]
                if (self.operational_status.currentText() == "MCU"):
                    v = ("login", self.role.currentText(), self.controller_responsability.currentText(), "MCU", 0, int(userId), int(facilityId), int(workstationId))
                if (self.operational_status.currentText() == "MCM"):
                    v = ("login", self.role.currentText(), self.controller_responsability.currentText(), "MCS", 0, int(userId), int(facilityId), int(workstationId))
                if (self.operational_status.currentText() == "MCI"):
                    v = ("login", self.role.currentText(), self.controller_responsability.currentText(), "MCT", 0, int(userId), int(facilityId), int(workstationId))
                connect = connection.cursor()
                connect.execute("INSERT INTO log_events (event_type, controller_role, controller_responsability, operational_status, date, send_to_narms, usersid, facilitiesid, workstationsid) VALUES (%s, %s,%s,%s,NOW(),%s,%s,%s,%s)", v) 
                connection.commit()              

    def controller1Action(self):
        operationalStatus = [ self.operational_status.itemText(i) for i in range(self.operational_status.count())]
        if (self.controller_id_1.currentText() != "choice"):
            if (self.controller_id_2.currentText() != "choice"):
                    self.operational_status.clear()
                    for i in range(len(self.operationalStatusList)):
                        if (self.operationalStatusList[i] != "SC"):
                            self.operational_status.addItem(self.operationalStatusList[i])
                            self.operational_status.update()
            else:
                self.operational_status.clear()
                self.operational_status.addItem("SC")
                self.operational_status.update()

    def controller2Action(self):
        operationalStatus = [ self.operational_status.itemText(i) for i in range(self.operational_status.count())]
        if (self.controller_id_1.currentText() == "choice"):
            if (self.controller_id_2.currentText() != "choice"):
                self.operational_status.clear()
                self.operational_status.update()
        else:
            if (self.controller_id_2.currentText() != "choice"):
                self.operational_status.clear()
                for i in range(len(self.operationalStatusList)):
                    if (self.operationalStatusList[i] != "SC"):
                        self.operational_status.addItem(self.operationalStatusList[i])
                        self.operational_status.update()
            else:
                self.operational_status.clear()
                self.operational_status.addItem("SC")
                self.operational_status.update()
