from flask import Flask, make_response, render_template, request
import logging
import json
import requests
import StringIO
import config

app = Flask(__name__)

CONTENT_TYPE = {'Content-Type': 'application/json;charset=UTF-8'}
NEST_ENDPOINT = 'https://developer-api.nest.com'
THERMOSTAT_ID = 'YOUR_THERMOSTATS_ID'
TOKEN = 'YOUR_NEST_AUTH_TOKEN'

def generate_response(output_speech, card_title="", card_subtitle="", card_content="", session_attributes={}, should_end_session=True):
    response = {
        "version": "1.0",
        "sessionAttributes": {
            "user": {
                "name": "nelson"
            }
        },
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": output_speech
            },
            "card": {
                "type": "Simple",
                "title": card_title,
                "subtitle": card_subtitle,
                "content": card_content
            },
            "shouldEndSession": should_end_session
        }
    }
    return json.dumps(response)


@app.route('/', methods=['POST'])
def post():
    logging.info(json.dumps(request.json, indent=4, sort_keys=False))

    response = ""

    try:
        temperature = request.json["request"]["intent"]["slots"]["temperature"]["value"]
    except TypeError:
        response = generate_response("Temperature not found.")
        return response, 200, CONTENT_TYPE

    logging.info("Action: %s" % temperature)

    output = StringIO.StringIO()
    output.write('{"target_temperature_f": %s}' % temperature)

    response = requests.put(NEST_ENDPOINT + '/devices/thermostats/' + THERMOSTAT_ID + "?auth=" + TOKEN,
                data={"target_temperature_f": int(temperature)})

    if not response.ok:
        speech = "Error"
        response_json = generate_response(
            output_speech=speech,
            card_title=speech,
            card_subtitle=speech,
            card_content="")
        return response_json, response.status_code, CONTENT_TYPE

    speech = "Temperature set to {}".format(temperature)
    response = generate_response(
        output_speech=speech,
        card_title=speech,
        card_subtitle=speech,
        card_content="")

    logging.info(json.dumps(json.loads(response), indent=4, sort_keys=False))
    return response, 200, CONTENT_TYPE


if __name__ == '__main__':
    app.run()

