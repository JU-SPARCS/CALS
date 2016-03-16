import requests

# TODO : replace localhost:3000 with the adress of 
API_BASE_URL = "http://193.10.30.126/api/cals/"

def postRequest(url,jsonString):
    """
    Input: url: String, jsonString: dictionary
    Output: the body of the response or None if the status code is different than 200
    Purpose: Sends the JSON dictionairy to the specified url via POST.
    """
    global API_BASE_URL

    resp = requests.post(API_BASE_URL + url, jsonString)
    print(resp.status_code)
    if resp.status_code == 200:
        return resp.text
    return None