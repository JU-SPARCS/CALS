import pymysql.cursors

def sendData(id_controller, event_type, controller_role, controller_responsability, operational_status, controller_time, controller_state) :

    # Connection to the database
    connection = pymysql.connect(host='mysql-moncompte.alwaysdata.net',
                             user='jeyjey78',
                             password='131293jer',
                             db='jeyjey78_cals',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    # Request
    try:
        with connection.cursor() as cursor:
            # Push Log-Event
            sql = "INSERT INTO `cals_user` (`id_controller`, `event_type`, `controller_role`, `controller_responsability`, `operational_status`, `controller_time`, `controller_state` ) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (id_controller, event_type, controller_role, controller_responsability, operational_status, controller_time, controller_state))

        # Commit to save the changes
        connection.commit()

    except:
        print('ERROR : function sendData -> Network module')

    finally:
        connection.close()
