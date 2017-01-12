__author__ = 'Swoosh'

import ostServer
import ostClientConnection
import ostClient
import ostPacketBuilder


def ost_cb_null(self):
    print("NULL callback")


def ost_cb_client_connected(client : ostClient.ostClient):
    o = ostPacketBuilder.ostPacketBuilder()
    client.addSendPacket(o.buildPacket_MSG_S2C_HANDSHAKE_CHALLENGE(1337))

