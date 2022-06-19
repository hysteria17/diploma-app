import requests
from config import METEO_CLIENT_ID
from app import app

client_id = METEO_CLIENT_ID


def request_api(endpoint, parameters):

    r = requests.get(endpoint, parameters, auth=(client_id, ''))
    json = r.json()

    data = None

    if r.status_code == 200:
        data = json['data']
        app.logger.info("Data retrieved from frost.met.no!")
    else:
        app.logger.error('Error! Returned status code %s' % r.status_code)
        app.logger.error('Message: %s' % json['error']['message'])
        app.logger.error('Reason: %s' % json['error']['reason'])

    return data