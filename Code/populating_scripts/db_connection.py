import pymysql
from connection_handler import *

DB_HOST = '193.10.30.129'
DB_USER = 'root'
DB_PASSWORD = 'JTH123!'
DB_NAME = 'cals_sim'

connection = None

def start_connection():
    global connection
    connection = pymysql.connect(host=DB_HOST,
                                 user=DB_USER,
                                 password=DB_PASSWORD,
                                 db=DB_NAME)

def close_connection():
    if connection != None:
        connection.close()


def insert_user(name, facility_id):
    """
    Send a new user to NARMS and store it in the database
    WARNING => 'name' parameter must be a two word string.
    """
    ## Store user in CALS DB
    v = (name, facility_id)
    connect = connection.cursor()
    connect.execute("INSERT INTO users (name, \
                                        facilitiesid) \
                        VALUES (%s,%s)", v) 
    user_id = connect.lastrowid
    connection.commit()

    ## Send new user to NARMS
    # Create the json input of the request
    token = get_facility_token(facility_id)
    json = {
        "token" : token,
        "first_name" : name.split(" ")[0],
        "name" : name.split(" ")[1],
        "date_of_birth" : ""
    }
    # send the request and retrieve the public ID
    pub_id = postRequest(get_facility_pub_id(facility_id) + "/" + "users", json)
    if pub_id == None:
        return None

    ## Store user in CALS DB
    v = (pub_id, user_id)
    connect = connection.cursor()
    connect.execute("UPDATE users SET pub_id = %s \
                        WHERE id = %s", v) 
    connection.commit()

    ## Return public ID
    return user_id


def insert_workstation(name, facility_id):
    """
    Send a new workstation to NARMS and store it in the database
    """
    ## Store workstation in CALS DB
    v = (name, facility_id)
    connect = connection.cursor()
    connect.execute("INSERT INTO workstations (name, \
                                                facilitiesid) \
                        VALUES (%s,%s)", v) 
    wk_id = connect.lastrowid
    connection.commit()


    ## Send new workstation to NARMS
    # Create the json input of the request
    token = get_facility_token(facility_id)
    json = {
        "token" : token,
        "name" : name
    }
    # send the request and retrieve the public ID
    pub_id = postRequest(get_facility_pub_id(facility_id) + "/" + "workstations", json)
    if pub_id == None:
        return None

    ## Update public ID of the workstation
    v = (pub_id, wk_id)
    connect = connection.cursor()
    connect.execute("UPDATE workstations SET pub_id = %s \
                        WHERE id = %s", v) 
    connection.commit()

    ## Return public ID
    return wk_id

def insert_log_event(event_type, controller_role, controller_responsability,
                     operational_status, date, user_id, workstation_id, facility_id):
    """
    Send a new log_event to NARMS and store it in the database
    The IDs passed as parameters are the IDs in the CALS DB, not the public IDs
    """
    ## Store the log event in CALS
    v = (event_type, controller_role, controller_responsability,
         operational_status, date, 0, user_id, facility_id, workstation_id)                 
    connect = connection.cursor()
    connect.execute("INSERT INTO log_events (event_type, \
                                            controller_role, \
                                            controller_responsability, \
                                            operational_status, \
                                            date, \
                                            send_to_narms, \
                                            usersid, \
                                            facilitiesid, \
                                            workstationsid) \
                        VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s)", v)
    log_event_id = connect.lastrowid
    connection.commit()

    ## Send the log event to NARMS
    # Create the json input of the request
    token = get_facility_token(facility_id)
    json = {
        "token" : token,
        "event_type" : event_type,
        "worker_role" : controller_role,
        "worker_responsability" : controller_responsability,
        "operational_status" : operational_status,
        "happened_at" : date,
        "user_id" : get_user_pub_id(user_id),
        "workstation_id" : get_workstation_pub_id(workstation_id)
    }
    # send the request
    resp = postRequest(get_facility_pub_id(facility_id) + "/" + "log_events", json)
    if resp == None:
        return None

    ## Store that the log event has been received
    connect = connection.cursor()
    connect.execute("UPDATE log_events SET send_to_narms = 1 \
                            WHERE id = %s", (log_event_id))
    connection.commit()


def insert_log_event_pub(event_type, controller_role, controller_responsability,
                        operational_status, date, user_pub_id, workstation_pub_id, facility_id):
    """
    Send a new log_event to NARMS and store it in the database
    The IDs passed as parameters are the IDs in the CALS DB, not the public IDs
    """
    ## Send the log event to NARMS
    # Create the json input of the request
    token = get_facility_token(facility_id)
    json = {
        "token" : token,
        "event_type" : event_type,
        "worker_role" : controller_role,
        "worker_responsability" : controller_responsability,
        "operational_status" : operational_status,
        "happened_at" : date,
        "user_id" : user_pub_id,
        "workstation_id" : workstation_pub_id
    }
    # send the request
    resp = postRequest(get_facility_pub_id(facility_id) + "/" + "log_events", json)
    if resp == None:
        return None

def get_facility_token(facility_id):
    connect = connection.cursor()
    connect.execute("SELECT api_key FROM facilities \
                        WHERE id = %s", (facility_id))
    token = connect.fetchone()[0]
    connection.commit()

    return str(token)

def get_user_pub_id(user_id):
    connect = connection.cursor()
    connect.execute("SELECT pub_id FROM users \
                        WHERE id = %s", (user_id))
    pub_id = connect.fetchone()[0]
    connection.commit()

    return str(pub_id)

def get_workstation_pub_id(workstation_id):
    connect = connection.cursor()
    connect.execute("SELECT pub_id FROM workstations \
                        WHERE id = %s", (workstation_id))
    pub_id = connect.fetchone()[0]
    connection.commit()

    return str(pub_id)

def get_facility_pub_id(facility_id):
    connect = connection.cursor()
    connect.execute("SELECT pub_id FROM facilities \
                        WHERE id = %s", (facility_id))
    pub_id = connect.fetchone()[0]
    connection.commit()

    return str(pub_id)