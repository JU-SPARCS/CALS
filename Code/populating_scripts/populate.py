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


# user1_id = insert_user("Alonso Balmasque", facility_id)
# user2_id = insert_user("Harry Cobeure", facility_id)
# insert_user("Kelly Diossi", facility_id)
# insert_user("Mark Assin", facility_id)
# insert_user("Yves Remord", facility_id)


# wk_id = insert_workstation("WK23", facility_id)
# insert_workstation("WK24", facility_id)

# To set a specific date:
# datetime.datetime(2006, 11, 21, 16, 30, 23).strftime("%Y-%m-%d %H-%M-%S") => 21-11-2006 16:30:23
user1_id = "7e59da37227"
wk_id = "96259b27a5d"

insert_log_event_pub("login", "PE", "Planning", "SC", datetime.datetime(2016, 3, 15, 8, 58, 23).strftime("%Y-%m-%d %H-%M-%S"), user1_id, wk_id, facility_id)

insert_log_event_pub("role_change", "RT", "Planning", "SC", datetime.datetime(2016, 3, 15, 9, 28, 42).strftime("%Y-%m-%d %H-%M-%S"), user1_id, wk_id, facility_id)

insert_log_event_pub("logout", "PE", "Planning", "SC", datetime.datetime(2016, 3, 15, 10, 00, 4).strftime("%Y-%m-%d %H-%M-%S"), user1_id, wk_id, facility_id)

insert_log_event_pub("login", "PE", "Planning", "SC", datetime.datetime(2016, 3, 16, 10, 30, 45).strftime("%Y-%m-%d %H-%M-%S"), user1_id, wk_id, facility_id)

insert_log_event_pub("role_change", "RT", "Planning", "MCI", datetime.datetime(2016, 3, 16, 10, 56, 52).strftime("%Y-%m-%d %H-%M-%S"), user1_id, wk_id, facility_id)

insert_log_event_pub("logout", "RT", "Planning", "MCI", datetime.datetime(2016, 3, 16, 11, 29, 50).strftime("%Y-%m-%d %H-%M-%S"), user1_id, wk_id, facility_id)

# close connection to the DB
close_connection()