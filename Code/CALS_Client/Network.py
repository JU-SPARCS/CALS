import pymysql.cursors

dbData = ['id_controller', 'event_type', 'controller_role', 'controller_responsability', 'operational_status', 'controller_time', 'traffic', 'weather', 'facility', 'air_space_segment', 'workstation']

def sendData(data) :
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
            sql = "INSERT INTO `log_event` (`id_controller`, `event_type`, `controller_role`, `controller_responsability`, `operational_status`, `controller_time`, `traffic`, `weather`, `facility`, `air_space_segment`, `workstation`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (int(data[dbData[0]]), data[dbData[1]], data[dbData[2]], data[dbData[3]], data[dbData[4]], data[dbData[5]], data[dbData[6]], data[dbData[7]], data[dbData[8]], data[dbData[9]], data[dbData[10]]))

        # Commit to save the changes
        connection.commit()

    except Exception as e:
        print(e)

    finally:
        connection.close()
