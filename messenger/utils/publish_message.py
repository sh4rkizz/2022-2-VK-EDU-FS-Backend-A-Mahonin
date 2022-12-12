import json
import requests
from application.settings import CENTRIFUGO_API_KEY

#
# def publish_message(message, channel='chat'):
#     command = {
#         'method': 'publish',
#         'params': {
#             'channel': channel,
#             'data': message
#         }
#     }
#
#     headers = {'Content-type': 'application/json', 'Authorization': 'apikey ' + CENTRIFUGO_API_KEY}
#     requests.post('http://localhost:8000/api', data=json.dumps(command), headers=headers)
