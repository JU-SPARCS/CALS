import pymysql.cursors

def sendData(id_controller, event_type, controller_role, controller_responsability, operational_status, controller_time, controller_state) :
    # Request
    try:
        # Connection to the database
        connection = pymysql.connect(host='mysql-moncompte.alwaysdata.net',
                                 user='cals',
                                 password='cals1',
                                 db='cals_sim',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

        with connection.cursor() as cursor:
            # Push Log-Event
            sql = "INSERT INTO `logs_event` (`id_controller`, `event_type`, `controller_role`, `controller_responsability`, `operational_status`, `controller_time`, `controller_state` ) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (id_controller, event_type, controller_role, controller_responsability, operational_status, controller_time, controller_state))

        # Commit to save the changes
        connection.commit()

    except Exception as e:
        print(e)

    finally:
        connection.close()
