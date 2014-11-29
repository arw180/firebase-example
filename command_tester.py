"""
command_tester.py
"""
import json
import threading
import time
from Queue import Queue

import constants
from rest_request import RestRequest

commands = []
cmd = RestRequest(constants.URL, 'PUT', {}, {"greeting": "hello"})
commands.append(cmd)


class CommandTester(threading.Thread):
    """
    Automatically sends events (REST requests to Firebase)

    All items in the queue must be RestRequest instances
    """

    def __init__(self, outbound_queue):
        self.outbound_queue = outbound_queue
        super(CommandTester, self).__init__()

    def run(self):
        time.sleep(10)
        while len(commands) > 0:
            command = commands.pop(0)
            print 'CommandTester sending command type %s with data %s' % (
                command.request_type, command.data)
            self.outbound_queue.put(command)
            time.sleep(10)

    def close(self):
        pass