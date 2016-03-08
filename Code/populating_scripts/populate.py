#!/usr/bin/python3

# Required complementary modules
#  - requests
#  - pymysql
# use $> pip install [module_name] to install a module


from db_connection import *
import datetime

# initiate the connection to the db
start_connection()

facility_id = 1


user1_id = insert_user("Alonso Balmasque", facility_id)
user2_id = insert_user("Harry Cobeure", facility_id)
insert_user("Kelly Diossi", facility_id)
insert_user("Mark Assin", facility_id)
insert_user("Yves Remord", facility_id)


wk_id = insert_workstation("WK23", facility_id)
insert_workstation("WK24", facility_id)

insert_log_event("login", "PE", "Planning", "SC", datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"), user1_id, wk_id, facility_id)
insert_log_event("role_change", "RT", "Planning", "SC", datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"), user1_id, wk_id, facility_id)
insert_log_event("logout", "PE", "Planning", "SC", datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"), user1_id, wk_id, facility_id)
insert_log_event("login", "PE", "Planning", "SC", datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"), user1_id, wk_id, facility_id)
insert_log_event("login", "PE", "Planning", "SC", datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"), user1_id, wk_id, facility_id)
insert_log_event("role_change", "RT", "Planning", "MCU", datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"), user1_id, wk_id, facility_id)
insert_log_event("login", "RT", "Planning", "MCU", datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"), user2_id, wk_id, facility_id)
insert_log_event("logout", "RT", "Planning", "MCU", datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"), user1_id, wk_id, facility_id)
insert_log_event("logout", "RT", "Planning", "MCU", datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"), user2_id, wk_id, facility_id)

# close connection to the DB
close_connection()