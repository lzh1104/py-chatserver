import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect(('164.132.96.222',443))
s.connect(('127.0.0.1',443))
ba = s.recv(100)

print(ba)

my_bytes = bytearray()

my_bytes.append(0x02) #opcode
my_bytes.append(0x07) #data length
my_bytes.append(0x00)
my_bytes.append(0x00)
my_bytes.append(0x00)

my_bytes.append(0x01) #client version
my_bytes.append(0x05) #nick_len
my_bytes.append(0x65)
my_bytes.append(0x66)
my_bytes.append(0x67)
my_bytes.append(0x68)
my_bytes.append(0x69)
s.send(my_bytes)

ba = s.recv(100)
print("handshake_state=", ba)
#c = 0
#while(True):
#	c = 0
s.close()