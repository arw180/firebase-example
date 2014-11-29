"""
streaming_event.py

An event from Firebase (uses the EventSource/Server-sent events protocol)
"""


class StreamingEvent():
    """
    A streaming event from Firebase

    https://www.firebase.com/docs/rest/api/#section-streaming

    Streaming events have a name and data

    Valid events
        * put
        * patch
        * keep-alive
        * cancel
        * auth_revoked

    Data (JSON-encoded)
    """
    def __init__(self, event, data):
        self.event = event
        self.data = data
