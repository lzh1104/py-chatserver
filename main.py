import ostBuffer
import ostServer
import ostPacketBuilder
import ostCallbacks
import random



#testing buffer
ostpb = ostPacketBuilder.ostPacketBuilder()
ostp = ostpb.buildPacket_MSG_S2C_HANDSHAKE_CHALLENGE(133773777)
print(ostp._data)
#print(ost.readByte())
#print(ost.readByte())


osrv = ostServer.ostServer('0.0.0.0',443)

# set callbacks
osrv.setCallbackClientConnect(ostCallbacks.ost_cb_client_connected)

osrv.bindServer()
osrv.startServerListen()


c = 0
cc = 0
while True:
    osrv.processConnections()
    c += 1
    cc += 1
    if c > 1000000:
        print ("[",cc, "] oserv state -> ", osrv.onlineClientCount() , " members online")
        c = 0
