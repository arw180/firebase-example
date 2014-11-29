"""
command_thread.py
"""
import json
import threading
from Queue import Queue

import requests

import constants
from rest_request import RestRequest


class CommandThread(threading.Thread):
    """
    Send REST request to Firebase

    All items in the queue must be RestRequest instances
    """

    def __init__(self, outbound_queue):
        self.outbound_queue = outbound_queue
        super(CommandThread, self).__init__()

    def run(self):
        while True:
            req = self.outbound_queue.get()
            if not req:
                break
            if req.request_type == 'GET':
                params = json.dumps(req.params)
                requests.get(req.url, params=params)
            elif req.request_type == 'POST':
                to_post = json.dumps(req.data)
                params = json.dumps(req.params)
                requests.post(req.url, params=params, data=to_post)
            elif req.request_type == 'PUT':
                to_put = json.dumps(req.data)
                params = json.dumps(req.params)
                requests.put(req.url, params=params, data=to_put)
            elif req.request_type == 'PATCH':
                to_patch = json.dumps(req.data)
                params = json.dumps(req.params)
                requests.patch(req.url, params=params, data=to_patch)
            elif req.request_type == 'DELETE':
                params = json.dumps(req.params)
                requests.delete(req.url, params=params)
            else:
                print 'Invalid request type: %s' % req.request_type

    def close(self):
        self.outbound_queue.put(False)