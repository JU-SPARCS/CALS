import json
import requests

def createJSONFormat(d_list):
    """
    Input: d_list: List with strings
    Output: JSON formatted dictionairy
    Purpose: To create a JSON dictionairy (format) from a list.
    """
    json_format = {"id_controller": d_list[0], "event_type": d_list[1], "controller_role": d_list[2], "controller_responsability": d_list[3],"operational_status": d_list[4], "controller_time": d_list[5], "traffic": d_list[6],"weather": d_list[7]  ,"facility": d_list[8] ,"air_space_segment": d_list[9] ,"workstation": d_list[10] ,"send_to_narms": d_list[11]}
    return json_format

def postRequest(url,jsonString):
    """
    Input: url: String, jsonString: dictionairy
    Output: None
    Purpose: Sends the JSON dictionairy to the specified url via POST.
    """
    resp = requests.post(url, json=jsonString)
    if resp.status_code != 201:
        print('Code: {}'.format(resp.status_code))

