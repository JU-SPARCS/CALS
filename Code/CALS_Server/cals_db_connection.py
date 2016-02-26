import pymysql

DB_HOST = '0.0.0.0'
DB_USER = ''
DB_PASSWORD = ''
DB_NAME = 'cals_sim'

def dbConnection():
    connection = pymysql.connect(host=DB_HOST,
                                 user=DB_USER,
                                 password=DB_PASSWORD,
                                 db=DB_NAME)
    return connection


connection = dbConnection()
