from enum import Enum
import ostPacket
import queue

class ostClientConnectionState(Enum):
    # disconnected default state
    ostDisconnected = 0
    # connected, but not authed yet
    ostConnected = 1
    # connected and successfully authed, participating in chat
    ostAuthed = 2

class ostClientConnection:


    _recv_packet_queue = None
    _send_packet_queue = None

    _state = ostClientConnectionState.ostDisconnected

    def __init__(self, socket):
        self._socket = socket
        self._state = ostClientConnectionState.ostConnected
        self._recv_packet_queue = queue.Queue()
        self._send_packet_queue = queue.Queue()


    def getSocket(self):
        return self._socket

    def terminateConnection(self):
        if (self._socket is not None):
            self._socket.close()
        self.setState(ostClientConnectionState.ostDisconnected)


    def addRecvPacket(self,p : ostPacket.ostPacket):
        self._recv_packet_queue.put(p)


    def addSendPacket(self,p : ostPacket.ostPacket):
        self._send_packet_queue.put(p)


    def hasSendPacket(self):
        return not (self._send_packet_queue.empty())


    def getSendPacket(self) -> ostPacket.ostPacket:
        return self._send_packet_queue.get()

    def hasRecvPacket(self):
        return not (self._recv_packet_queue.empty())


    def getRecvPacket(self) -> ostPacket.ostPacket:
        return self._recv_packet_queue.get()


    def setState(self,state : ostClientConnectionState):
        self._state = state

    def getState(self) -> ostClientConnectionState:
        return self._state
