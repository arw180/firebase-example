"""
rest_request.py
"""


class RestRequest():
    """
    A REST request to send to Firebase

    Valid params: https://www.firebase.com/docs/rest/api/#section-query-parameters
        * auth
        * shallow
        * print
        * format
        * orderBy

    Valid request_types:
        * GET
        * POST
        * PUT
        * PATCH
        * DELETE

    data must be valid json

    """
    def __init__(self, url, request_type, params={}, data={}):
        self.url = url
        self.params = params
        self.request_type = request_type
        self.data = data