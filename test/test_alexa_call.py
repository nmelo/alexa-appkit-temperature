import logging
import unittest
from test import BaseTestCase

class TestPostFromAlexa(BaseTestCase):
    def test_set_to_70(self):
        request_body = {
            "session": {
                "new": True,
                "sessionId": "amzn1.echo-api.session.ec9a2aa7-5c42-48f2-a189-87edc9ae1bed",
                "user": {
                    "userId": "amzn1.account.AHSMN72XJPRTGNUUYRUDD7EINGYQ"
                }
            },
            "version": "1.0",
            "request": {
                "intent": {
                    "slots": {
                        "temperature": {
                            "name": "temperature",
                            "value": "70"
                        }
                    },
                    "name": "set"
                },
                "type": "IntentRequest",
                "requestId": "amzn1.echo-api.request.7aedb25c-afd9-4ea6-aa38-42cd85d7357a"
            }
        }

        response = self.app.post_json('/', request_body)
        self.assertEqual(response.status, "200 OK")
        self.assertNotEqual(response.json_body, None)
        self.assertNotEqual(response.json_body["response"]["outputSpeech"]["text"], "")

