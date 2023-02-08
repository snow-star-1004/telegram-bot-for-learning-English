import json

import apiai

from common import security


def call_small_talk(message):
    try:
        request = apiai.ApiAI(security.DIALOG_FLOW_TOKEN).text_request()
        request.lang = security.DIALOG_FLOW_LANGUAGE
        request.session_id = security.DIALOG_FLOW_NAME
        request.query = message
        response = json.loads(request.getresponse().read().decode('utf-8'))
        return response['result']['fulfillment']['speech']
    except Exception as e:
        raise Exception('Can not get information' + str(e))
