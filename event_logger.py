"""
event_logger.py
"""
import json
import threading
from Queue import Queue

import constants


class EventLogger(threading.Thread):
    """
    Log streaming events received from Firebase

    events are of type StreamingEvent
    """

    def __init__(self, inbound_queue):
        self.inbound_queue = inbound_queue
        super(EventLogger, self).__init__()

    def run(self):
        while True:
            event = self.inbound_queue.get()
            if not event:
                break
            try:
                print 'Received event: %s' % json.dumps(event.data)
            except Exception:
                print 'Failed to decode json object: %s' % str(event.data)

    def close(self):
        pass