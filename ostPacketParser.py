__author__ = 'Swoosh'


import ostPacket
import ostConst

class ostPacketparser:



#    def __init__(self):
        #ddd

    def parsePacket_MSG_C2S_HANDSHAKE_RESPONSE(self,packet : ostPacket.ostPacket):
        #assert (packet.getSize() == 1)
        print("parsePacket_MSG_C2S_HANDSHAKE_RESPONSE -> bin : ",packet._data, " dc : ", packet._data_pivot)

        client_version = packet.readByte()
        nickname_len = packet.readByte()
        nickname = packet.readString(nickname_len)
        print("parsePacket_MSG_C2S_HANDSHAKE_RESPONSE : ", nickname, " : ", str(nickname_len))
        return client_version,nickname

    def parsePacket_MSG_MSG_C2S_CHAT_MESSAGE(self,packet : ostPacket.ostPacket):
        msg_len = packet.readInt()
        #assert (packet.getSize() == msg_len + 4)
        msg = packet.readString(msg_len)
        return msg_len,msg

    #empty payload
    def parsePacket_MSG_C2S_MEMBER_TYPING(self,packet : ostPacket.ostPacket):
        assert (packet.getSize() == 0)
        return 0