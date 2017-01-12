__author__ = 'Swoosh'

import ostClientConnection
import ostClient
import ostChatMessage
import ostPacket

class ostClientManager:

    _clients = []
    _messages = []

    def addClient(self,client : ostClientConnection.ostClientConnection):
        self._clients.append(client)


    def getClients(self):
        return self._clients


    def removeClient(self,client : ostClientConnection.ostClientConnection):
        self._clients.remove(client)


    def broadcastPacket(self,packet : ostPacket.ostPacket ):
        if (len(self._clients) > 0):
            for (client) in self._clients:
                client.addSendPacket(packet)


#    def relayChatMessage(self,msg : ostChatMessage.ostChatMessage,sender : ostClient.ostClient):



#        if (len(self._clients) > 0):
#            for client in self._clients:
#                if (client.getId() != msg.getSender().getId()):


