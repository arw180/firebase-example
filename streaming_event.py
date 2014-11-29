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

    Data (JSON-encoded) data. For put and patch events, this data will be a
    dict with two keys: "path" and "data"
    """
    def __init__(self, event, data):
        self.event = event
        self.data = data
