__author__ = 'Swoosh'

import ostClientConnection
import ostConst

class ostClient (ostClientConnection.ostClientConnection):

    _id = 0
    _nickname = ""
    _last_message_timestamp = 0
    _version = 0


    def __init__(self, socket):
        super().__init__(socket)


    def setId(self,id):
        self._id = id


    def getId(self):
        return self._id


    def setNickname(self,nick):
        self._nickname = nick


    def getNickname(self):
        return self._nickname


    def setMessageTimestamp(self,ts):
        self._last_message_timestamp = ts


    def getMessageTimestamp(self):
        return self._last_message_timestamp


    def setVersion(self,v):
        self._version = v


    def getVersion(self):
        return self._version


    def toString(self):
        return "ostClient" + " v=" + str(self._version) + ", id=" + str(self._id) + ", nick=" + str(self._nickname) + ", socket=" + str(self.getSocket()) + ", state=" + str(self.getState())






