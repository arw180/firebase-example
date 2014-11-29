"""
event_receiver_thread.py
"""

from sseclient import SSEClient
import json
import threading
import socket
from Queue import Queue

import constants
from streaming_event import StreamingEvent


class ClosableSSEClient(SSEClient):
    """
    Hack in some closing functionality on top of the SSEClient
    """

    def __init__(self, *args, **kwargs):
        self.should_connect = True
        super(ClosableSSEClient, self).__init__(*args, **kwargs)

    def _connect(self):
        if self.should_connect:
            super(ClosableSSEClient, self)._connect()
        else:
            raise StopIteration()

    def close(self):
        self.should_connect = False
        self.retry = 0
        # HACK: dig through the sseclient library to the requests library down
        # to the underlying socket.
        # then close that to raise an exception to get out of streaming.
        # I should probably file an issue w/ the
        # requests library to make this easier
        self.resp.raw._fp.fp._sock.shutdown(socket.SHUT_RDWR)
        self.resp.raw._fp.fp._sock.close()


class EventReceiverThread(threading.Thread):
    """
    Receive streaming events from Firebase

    All elements in the message queue will be StreamingEvent instances
    """

    def __init__(self, message_queue):
        self.message_queue = message_queue
        super(EventReceiverThread, self).__init__()

    def run(self):
        try:
            self.sse = ClosableSSEClient(constants.URL)
            for msg in self.sse:
                msg_data = json.loads(msg.data)
                if msg_data is None:    # keep-alive, cancel events
                    continue
                if type(msg_data) is str:   # auth_revoked
                    continue
                # TODO: msg doesn't contain event type - how to tell put vs patch?
                event = StreamingEvent('put', msg_data)
                self.message_queue.put(event)
        except socket.error:
            pass    # this can happen when we close the stream

    def close(self):
        if self.sse:
            self.sse.close()