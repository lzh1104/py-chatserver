__author__ = 'Swoosh'

import ostClient

class ostChatMessage:

    _timestamp = 0
    _msg = ""
    _sender = None


    def __init__(self, ts, msg, sender):
        self._sender = sender
        self._msg = msg
        self._timestamp = ts


    def setSender(self,sender : ostClient.ostClient):
        self._sender = sender

    def getSender(self) -> ostClient.ostClient:
        return self._sender

    def getMessage(self):
        return self._msg

    def getTimestamp(self):
        return self._timestamp

