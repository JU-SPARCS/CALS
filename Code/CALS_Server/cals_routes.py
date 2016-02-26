import pymysql
import falcon
import json

from cals_db_connection import *

class apiResource:

    def on_post(self, req, resp):
        """Handles POST requests"""
        try:
            raw_json = req.stream.read()
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400,
                                   'Error',
                                   '{0}'.format(ex))
        
        try:
            result_json = json.loads(raw_json.decode('utf-8'))
        except ValueError as e:
            raise falcon.HTTPError(falcon.HTTP_400,
                                   'Malformed JSON',
                                   '{0}'.format(e))
        cur = connection.cursor()
        arg = "INSERT INTO `log_event` (`id_controller`, `event_type`, `controller_role`, `controller_responsability`, `operational_status`, `controller_time`, `traffic`, `weather`, `facility`, `air_space_segment`, `workstation`, `send_to_narms`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(arg, (int(result_json['id_controller']), result_json['event_type'], result_json['controller_role'], result_json['controller_responsability'], result_json['operational_status'], result_json['controller_time'], result_json['traffic'], result_json['weather'], result_json['facility'], result_json['air_space_segment'], result_json['workstation'], int(result_json['send_to_narms'])))
        connection.commit()
        resp.status = falcon.HTTP_202
        resp.body = json.dumps(result_json)
