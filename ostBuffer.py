import  struct


class ostBuffer:

    _data = None
    _data_pivot = 0

    def __init__(self):
        self._data = bytearray()
        self.clear()

    def clear(self):
        self._data = bytearray()
        self._data_pivot = 0

    def writeByte(self, val : int):
        #self._data.append(val)
        self._data.extend(int.to_bytes(val,1,"little"))
        self._data_pivot += 1

    def writeInt(self, val : int):
        self._data.append(val & 0xFF)
        self._data.append((val >> 8) & 0xFF)
        self._data.append((val >> 16) & 0xFF)
        self._data.append((val >> 24) & 0xFF)

        self._data_pivot += 4

    def readInt(self) -> int:

        the_int = int.from_bytes(self._data[self._data_pivot:], 'little')
        self._data_pivot += 4
        return the_int

    def patchByte(self,indx : int, value : int):
        try:
            self._data[indx] = value
        except IndexError:
            print("ostBuffer.patchByte() : Buffer offset is a failure in life")

    def getByte(self, indx : int) -> int:
        try:
            return self._data[indx]
        except IndexError:
            print("ostBuffer.getByte() : Attempting to get out of index byte")

    def patchInt(self,indx : int, value : int):
        try:
            self._data[indx] = value & 0xFF
            self._data[indx+1] = ((value >> 8) & 0xFF)
            self._data[indx+2] = ((value >> 16) & 0xFF)
            self._data[indx+3] = ((value >> 24) & 0xFF)
        except IndexError:
            print("ostBuffer.patchInt() : Buffer offset is a failure in life")


    def peekByte(self) -> int:
        try:
            return self._data[self._data_pivot-1]
        except IndexError:
            print("ostBuffer.peekByte() : Attempting to peek into an empty buffer")

    def readByte(self) -> int:
        try:
            if (self._data_pivot < 0):
                raise IndexError


            b = self._data[self._data_pivot]
            self._data_pivot += 1
            return b

        except IndexError:
            print("ostBuffer.readByte() : Attempting to read an empty buffer")


    def readString(self,plen):
        return "".join(map(chr, self._data[self._data_pivot:(self._data_pivot+plen)]))


    def getSize(self) -> int:
        return len(self._data)

    def toString(self):
        print(' '.join('{:02x}'.format(x) for x in self._data))



    def toByteArray(self) -> bytearray:
        ba = bytearray()
        ba[:] = self._data
        return ba

    def resetPivot(self):
        self._data_pivot = 0