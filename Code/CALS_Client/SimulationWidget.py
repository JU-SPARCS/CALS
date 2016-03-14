from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi   
import time
import pymysql
import json
import requests

API_BASE_URL = "http://190.10.30.126/api/cals/"

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

def sendLogEventNarms(d_list):
    """
    Input: d_list: List with strings
    """        
    json_format = {"worker_role": d_list[2], "worker_responsability": d_list[3], "operational_status": d_list[4],"happened_at": d_list[5], "user_id": d_list[6],"workstation_id": d_list[7], "token": d_list[8], "event_type": d_list[9] }
    url = str(d_list[0]) + "/log_events"
    postRequest(url, json_format)

def postRequest(url,jsonString):
    """
    Input: url: String, jsonString: dictionary
    Output: the body of the response or None if the status code is different than 200
    Purpose: Sends the JSON dictionairy to the specified url via POST.
    """
    global API_BASE_URL

    resp = requests.post(API_BASE_URL + url, jsonString)
    print(API_BASE_URL + url)
    print(resp)
    if resp.status_code == 200:
        return resp.text
    return None



class SimulationWidget(QDialog):

    def __init__(self):
        super(SimulationWidget, self).__init__()
        loadUi('select-facilities-workstations.ui', self)
        self.cur = connection.cursor(pymysql.cursors.DictCursor)
        self.cur.execute("SELECT * FROM facilities")
        self.listFacilities = self.cur.fetchall()
        self.facilities.clear()
        self.workstations.clear()
        key = 0
        for facility in self.listFacilities:
            if (key == 0):
                facilitiesId = facility["id"]
            self.facilities.addItem(facility["name"]) 
            key += 1
        self.cur.execute("SELECT * FROM workstations WHERE facilitiesid = %s", facilitiesId) 
        self.listWorkstations = self.cur.fetchall()
        for workstation in self.listWorkstations:
            self.workstations.addItem(workstation["name"])
        self.launch.clicked.connect(self.launchAction)
        self.log = None
        self.facilities.currentIndexChanged.connect(self.facilitiesAction)


    def facilitiesAction(self):
        facilitiesName = self.facilities.currentText()
        self.cur.execute("SELECT id FROM facilities f WHERE f.name LIKE %s", facilitiesName) 
        facilitiesId = self.cur.fetchone()
        self.cur.execute("SELECT * FROM workstations WHERE facilitiesid = %s", facilitiesId["id"]) 
        self.listWorkstations = self.cur.fetchall()
        self.workstations.clear()
        for workstation in self.listWorkstations:
            self.workstations.addItem(workstation["name"])

    def launchAction(self):
        self.log = LogWidget(self.facilities.currentText(), self.workstations.currentText())
        self.log.show()

class LogWidget(QDialog):
    
    def __init__(self, facility, workstation):
        self.slot_1 = 0
        self.slot_2 = 0
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
        self.logout.clicked.connect(self.logoutAction)
        self.facilityText.setText(facility)
        self.workstationText.setText(workstation)
        self.destroyed.connect(self.on_destroyed)

    def on_destroyed(self, *args):
        print("destroying dialog")

    def on_accept(self):
        print("accepting")
        self.done(42)

    def closeEvent(self, event):
        print("close")
        if (self.slot_1 != 0):
            self.logoutAction(1)
        if (self.slot_2 != 0):
            self.logoutAction(2) 
        return QDialog.closeEvent(self, event)


    def logoutAction(self, userId = ""):
        
        if (self.controller_id_1.currentText() == self.controller_id_2.currentText()):
            self.error.setText('The field controller Id 1 and controller Id 2 are same !')
        else:
            
            if (userId == 1):
                    userId = self.slot_1
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
                    self.slot_1 = 0
                    d_list = [facilityMysql["pub_id"], facilityMysql["api_key"], self.role.currentText(), self.controller_responsability.currentText(), self.operational_status.currentText(), time.strftime('%Y-%m-%d %H:%M:%S'), int(userId), int(workstationId), facilityMysql["api_key"], "logout"]
                    sendLogEventNarms(d_list)
                    self.error.setText("Logout Succes")
            elif(userId == 2):
                    userId = self.slot_2
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
                    self.slot_2 = 0
                    d_list = [facilityMysql["pub_id"], facilityMysql["api_key"], self.role.currentText(), self.controller_responsability.currentText(), self.operational_status.currentText(), time.strftime('%Y-%m-%d %H:%M:%S'), int(userId), int(workstationId), facilityMysql["api_key"], "logout"]
                    sendLogEventNarms(d_list)
                    self.error.setText("Logout Succes")
            else:
                if (self.slot_1 == 0 or self.slot_2 == 0):
                    self.error.setText('You are not login !')
                if (self.slot_1 != 0):
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
                    self.slot_1 = 0
                    d_list = [facilityMysql["pub_id"], facilityMysql["api_key"], self.role.currentText(), self.controller_responsability.currentText(), self.operational_status.currentText(), time.strftime('%Y-%m-%d %H:%M:%S'), int(userId), int(workstationId), facilityMysql["api_key"], "logout"]
                    sendLogEventNarms(d_list)
                    self.error.setText("Logout Succes")

                if (self.slot_2 != 0):
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
                    self.slot_2 = 0 
                    connection.commit()
                    d_list = [facilityMysql["pub_id"], facilityMysql["api_key"], self.role.currentText(), self.controller_responsability.currentText(), self.operational_status.currentText(), time.strftime('%Y-%m-%d %H:%M:%S'), int(userId), int(workstationId), facilityMysql["api_key"], "logout"]
                    sendLogEventNarms(d_list)
                    self.error.setText("Logout Succes")
                    

    def updateAction(self, userId = ""):
        
        if (self.controller_id_1.currentText() == self.controller_id_2.currentText()):
            self.error.setText('The field controller Id 1 and controller Id 2 are same !')
        else:
            if (userId == 1):
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
                    d_list = [facilityMysql["pub_id"], facilityMysql["api_key"], self.role.currentText(), self.controller_responsability.currentText(), self.operational_status.currentText(), time.strftime('%Y-%m-%d %H:%M:%S'), int(userId), int(workstationId), facilityMysql["api_key"], "update"]
                    sendLogEventNarms(d_list)
            elif (userId == 2):
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
                    d_list = [facilityMysql["pub_id"], facilityMysql["api_key"], self.role.currentText(), self.controller_responsability.currentText(), self.operational_status.currentText(), time.strftime('%Y-%m-%d %H:%M:%S'), int(userId), int(workstationId), facilityMysql["api_key"], "update"]
                    sendLogEventNarms(d_list)

    def loginAction(self):
        if (self.controller_id_1.currentText() == self.controller_id_2.currentText()):
            self.error.setText('The field controller Id 1 and controller Id 2 are same !')
        else:
            if (self.controller_id_1.currentText() != "choice"):
                self.cur.execute("SELECT * FROM users u WHERE u.name LIKE %s ", self.controller_id_1.currentText())
                userMysql = self.cur.fetchone()
                userId = userMysql["id"]
                if (self.slot_1 == userId):
                    self.updateAction(1)
                else:
                    if ((self.slot_1 != 0)  and (self.slot_1 != userId)):
                        self.logoutAction(1)
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
                    self.slot_1 = userId
                    d_list = [facilityMysql["pub_id"], facilityMysql["api_key"], self.role.currentText(), self.controller_responsability.currentText(), self.operational_status.currentText(), time.strftime('%Y-%m-%d %H:%M:%S'), int(userId), int(workstationId), facilityMysql["api_key"], "login"]
                    sendLogEventNarms(d_list)
                    self.error.setText("Login Succes")
            if (self.controller_id_2.currentText() != "choice"):
                self.cur.execute("SELECT * FROM users u WHERE u.name LIKE %s ", self.controller_id_2.currentText())
                userMysql = self.cur.fetchone()
                userId = userMysql["id"]
                if (self.slot_2 == userId):
                    self.updateAction(2)
                else:
                    if ((self.slot_2  != 0) and (self.slot_2 != userId)):
                        self.logoutAction(2)
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
                    d_list = [facilityMysql["pub_id"], facilityMysql["api_key"], self.role.currentText(), self.controller_responsability.currentText(), self.operational_status.currentText(), time.strftime('%Y-%m-%d %H:%M:%S'), int(userId), int(workstationId), facilityMysql["api_key"], "login"]
                    sendLogEventNarms(d_list)
                    self.slot_2 = userId
                    self.error.setText("Login Succes")
            else:
                if (self.slot_2 != 0):
                    self.logoutAction(2)

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
