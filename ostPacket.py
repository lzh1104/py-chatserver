__author__ = 'Swoosh'

import ostBuffer

class ostPacket(ostBuffer.ostBuffer):

    _opcode = 0x0

    def __init__(self):
        super().__init__()
        super().clear()
        self._opcode = 0x0


    def setOpcode(self,opcode : int):
        self._opcode = opcode


    def getOpcode(self) -> int:
        return self._opcode

    def toString(self):
        ba = self.toByteArray()
        print(' '.join('{:02x}'.format(x) for x in ba))

    def toByteArray(self) -> bytearray:
        ba = ostBuffer.ostBuffer()
        ba.clear()
        ba.writeByte(self.getOpcode())
        ba.writeInt(self.getSize())
        payload = super().toByteArray()
        for b in payload:
            ba.writeByte(b)

        return ba.toByteArray()
