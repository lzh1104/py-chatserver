import ostPacket
import ostConst

class ostPacketBuilder():


    #def __init__(self):

    def createContainer(self, opcode):
        p = ostPacket.ostPacket()
        p.setOpcode(opcode)
        return p

    def finalizeContainer(self, packet : ostPacket.ostPacket) -> ostPacket.ostPacket:
        #c = 0
        #for b in range(0,packet.getSize()):
        #    packet.patchByte(c,packet.getByte(c) ^ 0x42)
        #    c =+ 1
        return packet


    def buildPacket_MSG_S2C_HANDSHAKE_CHALLENGE(self,session_key):
        p = self.createContainer(ostConst.OST_OPCODE_MSG_S2C_HANDSHAKE_CHALLENGE)
        p.writeByte(ostConst.OST_SERVER_VERSION)
        p.writeInt(session_key)
        p = self.finalizeContainer(p)
        return p

    def buildPacket_MSG_S2C_NEWCLIENT_BROADCAST(self,member_id, member_name):
        p = self.createContainer(ostConst.OST_OPCODE_MSG_S2C_NEWCLIENT_BROADCAST)
        p.writeInt(member_id)
        p.writeByte(len(member_name))
        for c in member_name:
            p.writeByte(ord(c))
        p = self.finalizeContainer(p)
        return p


    def buildPacket_MSG_S2C_CHAT_MESSAGE(self,member_id,msg):
        p = self.createContainer(ostConst.OST_OPCODE_MSG_S2C_CHAT_MESSAGE)
        p.writeInt(member_id)
        p.writeInt(len(msg))
        for c in msg:
            p.writeByte(ord(c))
        p = self.finalizeContainer(p)
        return p

    def buildPacket_MSG_S2C_ONLINE_LIST(self,members):
        p = self.createContainer(ostConst.OST_OPCODE_MSG_S2C_ONLINE_LIST)
        p.writeInt(len(members))
        for m in members:
            p.writeInt(m.getId())
            n = m.getNickname()
            p.writeByte(len(n))
            for c in n:
                p.writeByte(ord(c))

        p = self.finalizeContainer(p)
        return p

    def buildPacket_MSG_S2C_MEMBER_DISCONNECT(self,member_id):
        p = self.createContainer(ostConst.OST_OPCODE_MSG_S2C_MEMBER_DISCONNECT)
        p.writeInt(member_id)
        p = self.finalizeContainer(p)
        return p

    def buildPacket_MSG_S2C_HANDSHAKE_STATE(self,h_state):
        p = self.createContainer(ostConst.OST_OPCODE_MSG_S2C_HANDSHAKE_STATE)
        p.writeByte(h_state)
        p = self.finalizeContainer(p)
        return p


    def buildPacket_MSG_S2C_MEMBER_TYPING(self,member_id):
        p = self.createContainer(ostConst.OST_OPCODE_MSG_S2C_MEMBER_TYPING)
        p.writeInt(member_id)
        p = self.finalizeContainer(p)
        return p